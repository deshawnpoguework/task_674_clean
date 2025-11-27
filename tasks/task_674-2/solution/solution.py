import json
import random

def predict(text: str):
    words = text.split()
    first_word = words[0] if words else "empty"
    prediction = f"processed_{first_word.lower()}"
    confidence = round(random.uniform(0.5, 1.0), 3)
    return {"prediction": prediction, "confidence": confidence}

if __name__ == "__main__":
    with open("input/input.txt", "r") as f:
        text = f.read().strip()

    result = predict(text)
    print(json.dumps(predict(text)))


