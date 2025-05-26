"""Handler module.

This module is used to create a lambda handler for the FastAPI application.
and be able to deploy the application to AWS Lambda.
"""

from mangum import Mangum

from src.main import app

handler = Mangum(app)
