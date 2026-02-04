# Step 2: Python Environment Setup

We use Python's built-in `venv` and the **latest official Milvus Python SDK**.

## Prerequisites

* Python **3.9+** installed
* Access to the `doc-expert/` directory

## Automated Setup (Recommended)

The application includes setup scripts in the `doc-expert/` directory for easy environment management.

### Step 1: Run Setup Script

Navigate to the `doc-expert/` directory and run the setup script:

```bash
cd doc-expert
./setup.sh
```

This script will:
- Check Python version
- Create a virtual environment (`venv/`)
- Install all dependencies from `requirements.txt`
- Set up the application environment

### Step 2: Start Application Environment

After setup, activate the environment using the start script:

**Option A: Source the script (recommended - activation persists):**
```bash
source start.sh
```

**Option B: Run the script (for status check):**
```bash
./start.sh
```

This script will:
- Activate the virtual environment
- Verify dependencies are installed
- Display environment information
- Prepare the environment for running scripts

**Note:** When you `source` the script, the virtual environment activation will persist in your current shell session. When you run it with `./start.sh`, it only shows status.

### Step 3: Stop Application Environment

When done, deactivate the environment:

```bash
./stop.sh
```

## Manual Setup (Alternative)

If you prefer to set up manually:

### Create Virtual Environment

```bash
cd doc-expert
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install pymilvus
pip install numpy
```

## Verify Installation

Check that everything is installed correctly:

```bash
python -c "import pymilvus; print('pymilvus version:', pymilvus.__version__)"
python -c "import numpy; print('numpy version:', numpy.__version__)"
```

## Dependencies

The `requirements.txt` file includes:

* `pymilvus>=2.3.0` - Official Milvus Python SDK
* `numpy>=1.24.0` - NumPy for vector operations

> `pymilvus` is the **official and actively maintained** Milvus Python client.

## Next Steps

Once the environment is set up and activated, proceed to [Step 3: Connect to Milvus from Python](step-3-connect-milvus.md).
