# Spectrum API

A FastAPI service for frequency spectrum analysis that converts time-domain signals to frequency domain using
Fast Fourier Transform (FFT) and returns the FFT results.

## Application Scope

The Spectrum API is designed to:
- Perform signal spectrum analysis using FFT
- Process time-domain signals and extract frequency components
- Return frequency, magnitude and phase information
- Provide a RESTful interface with authentication
- Optimize performance using PyFFTW with caching capabilities

## Dependencies and Tools

This project uses Poetry for dependency management with production, test and development requirements groups.
See [pyproject.toml](pyproject.toml) to review requirements.

## Version Management

The project version can be bumped using the provided `bump-version.sh` script. Use one of the following commands:
```
./bump.sh patch # Increment patch version (e.g., 1.0.0 -> 1.0.1)
./bump.sh minor # Increment minor version (e.g., 1.0.0 -> 1.1.0)
./bump.sh major # Increment major version (e.g., 1.0.0 -> 2.0.0)
```



## API Endpoints

### POST /analyze_spectrum

Analyzes the frequency components of a time-domain signal.

**Input:**
```
json
{
  "time_interval": 0.001,  // Time between samples in seconds (must be > 0)
  "data": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1]  // Signal data points
}
```
**Output:**
```
json
{
  "result": [
    {
      "frequency": 0.0,     // Frequency in Hz
      "module": 2.5,        // Magnitude of the frequency component
      "phase": 0.0          // Phase in radians
    },
    {
      "frequency": 10.0,
      "module": 1.6,
      "phase": -1.57
    }
    // Additional frequency bins...
  ]
}
```
## Important Signal Data Requirements
⚠️ **Note on Signal Data Quality:**
This service performs **no sanitization** on the input signal data. It expects:
- A list of valid numbers (float or int)
- No `NaN` values
- No values `None`
- No missing data points or gaps
- Evenly spaced time samples (as specified by ) `time_interval`

Invalid data will result in processing errors or potentially incorrect results. Always ensure your input data is properly preprocessed before sending it to the API.

## Installation with Docker
Build the Docker image:
```
docker build -t spectrum-api .
```
## Running with Docker

The application can be run in three different modes:

### Production Mode
Run the API server
```
docker run -p 8000:8000 \
  -e API_KEY_NAME=your-api-key-header-name \
  -e API_KEY_VALUE=your-api-key \
  spectrum-api app
```
or passing the .env file:
```
docker run -p 8000:8000 --env-file .env spectrum-api app
```
### Test Mode
Run tests to verify your build functionality:
```
docker run spectrum-api test
```
**Note:** Test modes are useful before deployment to ensure code quality and correctness.
Running tests verifies that all functionality works as expected.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| API_KEY_NAME | Name of the API key header | Yes |
| API_KEY_VALUE | Value of the API key for authentication | Yes |

## Testing the API

Here's a minimal Python snippet to test the API:
```
import requests
import json

# API endpoint and authentication
url = "http://localhost:8000/analyze_spectrum"
headers = {"your-api-key-name": "your-secret-key"}

# Example signal data
data = {
    "time_interval": 0.001,
    "data": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1]
}

# Make the API request
response = requests.post(url, headers=headers, json=data)

```
## License

MIT License
