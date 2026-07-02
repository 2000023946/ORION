# Install pip -r install requirements.txt first
echo "Running Unit Tests..."
PYTHONPATH=. pytest tests/unit --cov=src --cov-report=term-missing --cov-report=html
echo "Opening Cov Html..."
open htmlcov/index.html