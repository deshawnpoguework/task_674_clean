import json
import os
import subprocess
import unittest
from jsonschema import validate


class TestModelOutputs(unittest.TestCase):
    """
    Runs the real solution, validates JSON structure and schema compliance,
    ensures single-line output, and confirms prediction depends on input.
    """

    def setUp(self):
        self.task_root = os.path.dirname(os.path.dirname(__file__))

        # Load input
        self.input_path = os.path.join(self.task_root, "input", "input.txt")
        self.assertTrue(os.path.exists(self.input_path), "Input file missing.")

        with open(self.input_path, "r", encoding="utf-8") as f:
            self.original_input_text = f.read().strip()

        self.assertGreater(len(self.original_input_text), 0, "Input is empty.")
        self.original_first_word = self.original_input_text.split()[0]

        # Load schema.json
        schema_path = os.path.join(self.task_root, "schema.json")
        self.assertTrue(os.path.exists(schema_path), "schema.json missing.")
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def run_solution(self):
        proc = subprocess.run(
            ["python", "solution/solution.py"],
            cwd=self.task_root,
            capture_output=True,
            text=True
        )
        self.assertEqual(proc.returncode, 0, f"Solution crashed: {proc.stderr}")
        return proc.stdout.strip()

    def test_output_schema_and_input_usage(self):
        """Validate JSON schema and ensure prediction includes first word."""
        output = self.run_solution()

        # JSON must be valid
        try:
            data = json.loads(output)
        except Exception as e:
            self.fail(f"Invalid JSON output: {e}")

        # Schema validation
        try:
            validate(instance=data, schema=self.schema)
        except Exception as e:
            self.fail(f"Output does not match schema.json: {e}")

        # First word must appear in prediction
        self.assertIn(
            self.original_first_word.lower(),
            data["prediction"].lower(),
            "Prediction must include the first word of the input."
        )

    def test_output_is_single_line(self):
        """Output JSON must be single-line."""
        output = self.run_solution()
        self.assertNotIn("\n", output, "JSON output must be a single line")

    def test_input_affects_output(self):
        """
        Modified input must:
        1. Change prediction
        2. Include the NEW first word
        """
        temp_text = "DIFFERENTINPUTTEXT content"
        new_first_word = temp_text.split()[0]

        try:
            # Write modified input
            with open(self.input_path, "w", encoding="utf-8") as f:
                f.write(temp_text)

            modified_output = json.loads(self.run_solution())

            # Restore original input
            with open(self.input_path, "w", encoding="utf-8") as f:
                f.write(self.original_input_text)

            original_output = json.loads(self.run_solution())

            # Prediction MUST change
            self.assertNotEqual(
                modified_output["prediction"],
                original_output["prediction"],
                "Prediction did not change when input changed."
            )

            # Prediction MUST include new first word
            self.assertIn(
                new_first_word.lower(),
                modified_output["prediction"].lower(),
                "Modified input's first word not found in prediction."
            )

        finally:
            with open(self.input_path, "w", encoding="utf-8") as f:
                f.write(self.original_input_text)


if __name__ == "__main__":
    unittest.main()
