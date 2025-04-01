import unittest
import os
import io
import sys
if os.path.exists(os.path.abspath(os.path.dirname(__file__))):
      os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Running all the unit tests
if __name__ == "__main__":
      
      #This supresses the print outputs
      suppress_text = io.StringIO()
      sys.stdout = suppress_text 
      
      test_loader = unittest.TestLoader()
      test_suite = test_loader.discover("Unit_tests")
      
      test_runner = unittest.TextTestRunner()
      result = test_runner.run(test_suite)
      
      #This release the supression on the print outputs
      sys.stdout = sys.__stdout__
      
      #This prints the test summary
      print("\nTest Summary:")
      print(f"Total tests run: {result.testsRun}")
      print(f"Tests passed: {result.testsRun - len(result.failures) - len(result.errors)}")
      print(f"Tests failed: {len(result.failures)}")
      print(f"Tests errored: {len(result.errors)}")  