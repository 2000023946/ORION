# runs the test coverage and pulls open html file 
# run chmod +x run_test.sh before runnign 
# then run ./run_test.sh to run this file 

PYTHONPATH=. pytest --cov=. --cov-report=html && open htmlcov/index.html