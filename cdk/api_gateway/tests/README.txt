To run test scripts:

PYTHONPATH=/path/to/cdk/api_gateway python[3] -m pytest [[-v] [-s]] /path/to/api_gateway/tests --import-mode=importlib

What this does:
  - PYTHONPATH sets the python environment to be in the api_gateway directory
    (import for package locating)
  - Runs the pytest module
  - Optionally run with verbose output (-v) and/or print any output
    from any test, regardless of pass/fail (-s)
  - /path/to/api_gateway/tests specifies the path of the test scripts directory
  - --import-mode=importlib allows pytest to locate packages in the same python
    environment (e.g., allows tests to find the lambda code)
