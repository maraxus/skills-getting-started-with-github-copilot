# Tests

This directory contains comprehensive tests for the Mergington High School Activities API.

## Test Structure

- `test_app.py`: Main test file containing all API endpoint tests
- `conftest.py`: Pytest configuration and shared fixtures
- `__init__.py`: Makes tests a proper Python package

## Running Tests

### Prerequisites

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Basic Test Execution

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test file:
```bash
python -m pytest tests/test_app.py -v
```

### Coverage Reports

Run tests with coverage:
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing -v
```

Generate HTML coverage report:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## Test Categories

### 1. Root Endpoint Tests (`TestRootEndpoint`)
- Tests the root path `/` redirect functionality

### 2. Activities Endpoint Tests (`TestActivitiesEndpoint`)
- Tests `GET /activities` endpoint
- Validates response format and structure
- Ensures all activities are returned

### 3. Signup Endpoint Tests (`TestSignupEndpoint`)
- Tests `POST /activities/{activity_name}/signup`
- Valid signup scenarios
- Error cases (non-existent activity, duplicate signup)
- URL encoding handling

### 4. Unregister Endpoint Tests (`TestUnregisterEndpoint`)
- Tests `DELETE /activities/{activity_name}/unregister`
- Valid unregistration scenarios
- Error cases (non-existent activity, not registered)
- URL encoding handling

### 5. Integration Tests (`TestIntegrationScenarios`)
- Complete signup and unregister workflows
- Multiple students per activity
- Single student multiple activities

### 6. Edge Cases (`TestEdgeCases`)
- Special characters in emails
- Empty email handling
- Case sensitivity testing

## Test Features

- **Automatic data reset**: Each test starts with clean activity data
- **100% code coverage**: All API endpoints and error paths are tested
- **Comprehensive error testing**: Tests both success and failure scenarios
- **URL encoding support**: Tests special characters and spaces in parameters
- **Integration scenarios**: Tests realistic user workflows

## Current Test Coverage

The test suite achieves **100% code coverage** of the `src/app.py` file, testing all endpoints, error conditions, and business logic.

## Adding New Tests

When adding new tests:

1. Add them to the appropriate test class in `test_app.py`
2. Use descriptive test names starting with `test_`
3. Include docstrings explaining what the test validates
4. Ensure tests are independent and can run in any order
5. Use the `client` fixture for making API calls