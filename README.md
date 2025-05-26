# Journey Search Service

A FastAPI-based service for searching flight journeys, deployed on AWS Lambda using the Serverless Framework.

## Development

The service is built using:
- FastAPI for the web framework
- Mangum for AWS Lambda integration
- Pydantic for data validation
- Serverless Framework for deployment

## Prerequisites

- Python 3.12.6 or higher
- Node.js and npm (for Serverless Framework)
- AWS CLI configured with appropriate credentials
- Docker (for local development and deployment)


## Project Structure

```
.
├── src/                    # Source code
├── tests/                  # Unit tests
├── deploy/                 # Deployment related code
├── serverless.yml         # Serverless Framework configuration
├── pyproject.toml         # Python project configuration
└── requirements.txt       # Python dependencies
```

## Code Quality

The project uses several tools to maintain code quality:

- Ruff for linting
- Pre-commit hooks for automated checks
- Pytest for testing
- Coverage for test coverage reporting

## Environment Setup

1. Create and activate a virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Linux/Mac
   # or
   .venv\Scripts\activate  # On Windows
   ```

2. Install Python dependencies:
   ```bash
   uv pip sync pyproject.toml
   ```

3. Install Serverless Framework and plugins:
   ```bash
   npm install
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
FLIGHT_EVENTS_API_URL=<your-api-url>
MAX_CONNECTIONS=<max-connections>
MAX_JOURNEY_DURATION_HOURS=<max-journey-duration>
MAX_CONNEXTION_DURATION_HOURS=<max-connection-duration>
```

## Running Tests

Run the test suite with coverage:

```bash
pytest --cov=src tests/
```


## Deployment

1. Ensure you have AWS credentials configured:
   ```bash
   aws configure
   ```

2. Generate `requirements.txt`, it is used in deployment by the `serverless-python-requirements` plugin
    ```bash
    uv pip compile pyproject.toml -o requirements.txt
    ```

3. Deploy to AWS Lambda:
   ```bash
   serverless deploy
   ```

4. To remove the deployed service:
   ```bash
   serverless remove
   ```
