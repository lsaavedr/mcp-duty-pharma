# MCP Duty Pharma

MCP Duty Pharma helps you locate pharmacies legally required to stay open during nights, weekends, and holidays. Whether it's an emergency or just a late-night need, this tool ensures you always know where to go.

## 📋 System Requirements

- Python 3.10+

## 📦 Dependencies

Install all required dependencies:

```bash
# Using uv
uv sync
```

### Required Packages

- **fastmcp**: Framework for building Model Context Protocol servers
- **geoPy**: Python library for accessing and geocoding/reverse geocoding locations.
- **httpx**: HTTP client for Python, which provides a simple and intuitive API for making HTTP requests.

All dependencies are specified in `pyproject.toml`.

## 📑 Table of Contents

- [System Requirements](#-system-requirements)
- [Dependencies](#-dependencies)
- [MCP Tools](#%EF%B8%8F-mcp-tools)
- [Getting Started](#-getting-started)
- [Installation](#-installation)
- [Safety Features](#-safety-features)
- [Development Documentation](#-development-documentation)

## 🛠️ MCP Tools

This MCP server provides the following tools to Large Language Models (LLMs):

### get_nearby_duty_pharmacies

- Get ten closest pharmacies on duty today, sorted by distance to the given address.

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/lsaavedr/mcp-duty-pharma.git
cd mcp-duty-pharma
```

## 📦 Installation

You can install this MCP server in either Claude Desktop or elsewhere. To use this server, add the following configuration to the settings file:

- in json format

```json
{
  "MCP Duty Pharma": {
    "command": "uv",
    "args": ["tool", "run", "mcp_duty_pharma"]
  }
}
```

- in yaml format

```yaml
mcpServers:
  - name: MCP Duty Pharma
    command: uv
    args:
      - tool
      - run
      - mcp_duty_pharma
```

🔒 Safety Features

- Rate Limiting: Each geocoding call is rate-limited (e.g., 1-second delay) to avoid excessive requests that violate usage limits.
- Error Handling: Catches geopy exceptions (timeouts, service errors) and returns safe [] results instead of crashing.

📚 Development Documentation

If you’d like to extend or modify this server:

- Check duty-pharma.py for how each tool is implemented and how duty-pharma is integrated.
- Look at geopy’s official docs for advanced usage like bounding boxes, language settings, or advanced data extraction.
- Look at regional government APIs for more data sources.
