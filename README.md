# Global Alcohol Consumption Dashboard

This project is a Dash-based interactive dashboard for analyzing global alcohol consumption trends.

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/ntr7an/plotly-DASHboard.git
cd plotly-DASHboard
```

## Deployment Options

### Option 1: Using Docker

#### Prerequisites
- Docker installed on your system
- Docker Compose (optional)

#### Running with Docker

1. Build the Docker image:
```bash
docker build -t vdi_project .
```

2. Run the container:
```bash
docker run -p 8050:8050 vdi_project
```

3. Access the dashboard:
Open your web browser and navigate to:
```
http://localhost:8050/
```

### Option 2: Using uv (Python Package Manager)

#### Prerequisites
- Install uv package manager:

For macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
or using wget:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

For Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Running with uv

1. Navigate to the project directory:
```bash
cd plotly-DASHboard
```

2. Run the application:
```bash
uv run main.py
```

The dashboard will be available at `http://localhost:8050/` and you can start exploring the global alcohol consumption data.
