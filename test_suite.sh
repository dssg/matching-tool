echo "STEP 1: Python webapp tests"
PYTHONPATH='.' py.test tests/ --cov=webapp
echo "STEP 2: JS Tests"
cd frontend
npm run test
cd -
echo "Test suite done"
