# Doc-Expert Application

This directory contains the application code for the Milvus Vector DB experiment.

## Quick Start

### 1. Setup Environment

Run the setup script to create the virtual environment and install dependencies:

```bash
./setup.sh
```

### 2. Start Application Environment

Activate the virtual environment and prepare the application:

**Option A: Source the script (recommended - activation persists):**
```bash
source start.sh
```

**Option B: Run the script (for status check):**
```bash
./start.sh
```

**Note:** When you `source` the script, the virtual environment activation will persist in your current shell session. When you run it with `./start.sh`, it only shows status.

### 3. Stop Application Environment

Deactivate the virtual environment:

```bash
./stop.sh
```

## Structure

The application code is organized by steps:

- **Step 2**: Python environment setup ✅
- **Step 3**: Connect to Milvus ✅
  - `step3_connect.py` - Connection script
  - `milvus_connection.py` - Reusable connection utility
- **Step 4**: Create collection and insert data ✅
  - `step4_create_collection.py` - Collection creation with recommended schema
- **Step 5**: Similarity search
- **Step 6**: LLM integration
- **Step 7**: Batch processing

## Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Files

- `setup.sh` - Initial setup script (creates venv, installs dependencies)
- `start.sh` - Start script (activates venv, checks dependencies)
- `stop.sh` - Stop script (deactivates venv)
- `requirements.txt` - Python dependencies

## Usage

After running `./start.sh`, you can run application scripts for each step. Each step will have corresponding Python scripts that can be run independently or as part of the complete workflow.
