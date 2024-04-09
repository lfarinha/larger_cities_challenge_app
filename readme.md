# Suggestions API Challenge

## Description

FastAPI application to find suggestions for nearby large cities

## API Documentation

The API documentation can be found navigating to the following url: http://localhost:5000/docs

## Installation

1. Decompress the larger_cities_challenge_app.zip file:
2. Navigate to the project's root folder:
    ```bash
      cd larger_cities_challenge_app
    ```
3. Open a terminal or powershell and create a virtual environment:
   ### Windows Powershell
    ```bash
    python -m venv venv
    cd .venv/bin/
    activate.ps1
    ```
   ### Mac/Linux
    ```bash
    python3 -m venv venv
    source .venv/bin/activate
    ```
4. Install the requirements:
   ```bash
    pip install -r requirements.txt
    ```

## Running the application:

1. Navigate to the main project folder larger_fields, In a terminal or powershell:
    ```bash
      cd larger_files
   ```
2. Run the uvicorn application:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 5000
   ```

## Testing the application

1. Navigate to the main project test folder, In a terminal or powershell:
    ```bash
      cd test
   ```
2. Run the tests:
   ```bash
   pytest
   ```
