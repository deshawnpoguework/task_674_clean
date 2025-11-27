FROM python:3.10-slim

# Install ONLY runtime dependencies
RUN pip install --no-cache-dir torch==2.3.1

WORKDIR /workspace

# No COPY of solution, tests, or input allowed
# The harness mounts them at runtime.

CMD ["python", "/workspace/solution/solution.py"]


