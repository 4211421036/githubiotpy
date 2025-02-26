# GitHubIoT

[Logo GitHubIoT](https://4211421036.github.io/githubiotpy/img/GitHub%20IoT%20Logo.png)

A toolkit for IoT data visualization with GitHub integration.

## Installation

```bash
pip install githubiot
```

## Usage
After installation, you can run the CLI tool:

```bash
githubiot
```

### Available Commands

- `githubiot` --create-app: Create a new application template
- `githubiot` --build: Build the application to an executable
- `githubiot` --run: Run the application
- `githubiot` --json-url: Set custom JSON URL
- `githubiot` --name: Set custom application name
- `githubiot` -v, --version: Show version

### Using as a Module
You can also use GitHubIoT as a Python module:

```py
import githubiot

# Start with custom parameters
githubiot.start(
    name="My IoT App",
    url_json="https://api.example.com/data",
    icon="https://example.com/icon.ico",
    status="build"  # or "run"
)
```

## Author
1. GALIH RIDHO UTOMO
2. Fionita Fahra Azzahra
