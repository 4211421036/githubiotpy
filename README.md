# GitHubIoT Documentation

<p align="center">
  <img src="https://4211421036.github.io/githubiotpy/img/GitHub%20IoT%20Logo.png" alt="GitHubIoT Logo">
</p>

Before Started Develoment this Application. Please Readme Wiki repository GitHub IoT for Arduino IDE Application at [https://github.com/4211421036/githubiot/wiki](https://github.com/4211421036/githubiot/wiki), following step by step. And The last, your can develoment webApp with GA  [https://github.com/marketplace/actions/generate-iot-dashboard](https://github.com/marketplace/actions/generate-iot-dashboard) automation step by step. Thank You!

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Using as a Module](#using-as-a-module)
- [Application Structure](#application-structure)
  - [Core Components](#core-components)
  - [User Interface](#user-interface)
  - [Data Handling](#data-handling)
- [Configuration](#configuration)
  - [Configuration File](#configuration-file)
  - [Runtime Configuration](#runtime-configuration)
- [Customization](#customization)
  - [Themes](#themes)
  - [Chart Types](#chart-types)
  - [Animation Settings](#animation-settings)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Debug Mode](#debug-mode)
- [API Reference](#api-reference)
  - [Main Methods](#main-methods)
  - [Data Processing Functions](#data-processing-functions)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)

## Introduction

GitHubIoT is a comprehensive toolkit designed to simplify the visualization of IoT (Internet of Things) data with seamless GitHub integration. The application provides an intuitive graphical interface for real-time data monitoring, analysis, and configuration, making it ideal for both beginners and experienced developers working with IoT devices.

> [!Note]
> GitHubIoT is designed to work with JSON data feeds, making it compatible with most IoT platforms and REST APIs.

## Installation

You can install GitHubIoT using pip:

```bash
pip install githubiot
```

or using Docker command line:
```bash
docker pull galihridhoutomo/githubiot
```

### Prerequisites

- Python 3.7 or higher
- Required dependencies:
  - Matplotlib
  - NumPy
  - Requests
  - TkInter

> [!Important]
> Make sure you have the latest version of pip to avoid compatibility issues.

## Quick Start

After installation, you can quickly start the application with default settings:

```bash
githubiot --create-app
```

This will launch the application with default configurations. For a customized setup:

```bash
githubiot --name "My IoT Dashboard" --json-url "https://my-iot-api.com/data"
```

and the last step

```bash
githubiot --run
```

if you build this app to .exe application Desktop. Can be interact CLI githubiot below

```bash
githubiot --build
```

## Features

- **Real-time Data Visualization**: Monitor IoT data streams in real-time
- **Multiple Chart Types**: Support for various visualization methods
- **Customizable Themes**: Choose from multiple built-in themes or create your own
- **Animation Control**: Enable/disable animations for performance optimization
- **Graph Export**: Save visualizations in various formats (PNG, PDF, etc.)
- **Responsive Interface**: Adapts to different screen sizes
- **JSON Data Integration**: Connect to any JSON data source
- **Configurable Settings**: Customize application behavior through configuration files

## Usage

### Command Line Interface

GitHubIoT provides a comprehensive command line interface for various operations:

| Command | Description |
|---------|-------------|
| `githubiot --create-app` | Create a new application template |
| `githubiot --build` | Build the application to an executable |
| `githubiot --run` | Run the application |
| `githubiot --json-url URL` | Set custom JSON URL |
| `githubiot --name NAME` | Set custom application name |
| `githubiot -v, --version` | Show version information |

### Using as a Module

You can also integrate GitHubIoT into your own Python projects:

```python
import githubiot

# Start with custom parameters
githubiot.start(
    name="My IoT Dashboard",
    url_json="https://api.example.com/data",
    icon="https://example.com/icon.ico",
    status="build"  # or "run"
)
```

## Application Structure

### Core Components

The application is built around the `JSONGraphApp` class, which manages the following key aspects:

1. **Configuration Management**: Loads and applies settings from a configuration file
2. **UI Construction**: Creates the menu system and UI widgets
3. **Data Handling**: Fetches and processes data from JSON sources
4. **Graph Rendering**: Visualizes data using Matplotlib
5. **Animation Control**: Manages real-time animation of data

### User Interface

The UI consists of:

- Main visualization area
- Toolbar for common actions
- Menu system with File, Options, and Help menus
- Theme selection and customization options

### Data Handling

The application can:

- Connect to remote JSON data sources
- Generate sample data when connection fails
- Process and transform data for visualization
- Refresh data on demand

## Configuration

### Configuration File

GitHubIoT uses a `config.json` file for persistent settings:

```json
{
  "url": "https://api.example.com/data",
  "app_name": "GitHubIoT App"
}
```

> [!Warning]
> Do not manually edit the configuration file while the application is running. Use the application interface or CLI commands to modify settings.

### Runtime Configuration

The application can detect and apply configuration changes at runtime. When you modify settings externally, the application will update automatically.

## Customization

### Themes

GitHubIoT supports multiple visualization themes:

- Default
- Classic
- Dark Background
- GGPlot
- Seaborn
- Solarize Light
- BMH
- Tableau Colorblind-friendly
- FiveThirtyEight
- Custom themes

To cycle through themes, use the "Change Theme" option in the File menu.

### Chart Types

While the current implementation focuses on line charts for EM wave visualization, the architecture supports extending to other chart types:

- Line charts
- Bar charts
- Scatter plots
- Area charts

### Animation Settings

Animation can be toggled on/off from the Options menu. This is particularly useful when:

- Working with very large datasets
- Running on resource-constrained devices
- Generating static exports

## Troubleshooting

### Common Issues

1. **Data Not Loading**
   - Verify your internet connection
   - Check that the JSON URL is correct and accessible
   - Ensure the JSON format matches the expected structure

2. **Application Crashes**
   - Update to the latest version
   - Check for conflicting Python packages
   - Verify that all dependencies are installed correctly

3. **Visualization Issues**
   - Try changing the theme
   - Restart the application
   - Verify your data structure

### Debug Mode

For advanced troubleshooting, you can run the application in debug mode:

```bash
githubiot --debug
```

This will provide additional console output to help diagnose issues.

## API Reference

### Main Methods

| Method | Description |
|--------|-------------|
| `githubiot.start()` | Initializes and starts the application |
| `githubiot.load_config()` | Loads configuration from file |
| `githubiot.update_config()` | Updates configuration settings |
| `githubiot.build()` | Builds executable version |

### Data Processing Functions

| Function | Description |
|----------|-------------|
| `load_data()` | Fetches data from JSON source |
| `refresh_data()` | Updates data from source |
| `generate_sample_data()` | Creates sample data for testing |
| `create_graph()` | Renders visualization from data |

## Contributing

Contributions to GitHubIoT are welcome! Please follow these steps:

1. [Fork](https://github.com/4211421036/githubiotpy/fork) the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT LICENCE [https://github.com/4211421036/githubiotpy/LICENCE](https://github.com/4211421036/githubiotpy/LICENCE) - see the LICENSE file for details.

## Authors

1. GALIH RIDHO UTOMO
2. Fionita Fahra Azzahra

## Cite
Please cite this respotory, if your use in the publication

```bibtex
@misc{githubiot,
author = {Utomo, Galih Ridho, Fionita Fahra Azzahra},
title = {GitHub IoT a comprehensive toolkit designed to simplify the visualization of IoT (Internet of Things) data with seamless GitHub integration. The application provides an intuitive graphical interface for real-time data monitoring, analysis, and configuration, making it ideal for both beginners and experienced developers working with IoT devices microcontroler (ESP32 or ESP8266) realtime},
year = {2025},
howpublished = {\url{https://hub.docker.com/r/galihridhoutomo/githubiot}},
note = {GitHub repository},
}
```

---

<p align="center">
  <strong>GitHubIoT - Building the Future with Integrated Microcontroller Solutions</strong>
</p>
