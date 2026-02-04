# Step 3: Connect to Milvus from Python

This step establishes a connection to the Milvus Docker instance created in Step 1.

## Prerequisites

* Milvus Docker containers running (see [Step 1](step-1-run-milvus-docker.md))
* Python environment set up and activated (see [Step 2](step-2-python-environment-setup.md))
* Virtual environment activated with dependencies installed

## Quick Start

### Run the Connection Script

Navigate to the `doc-expert/` directory and run the connection script:

```bash
cd doc-expert
python step3_connect.py
```

Or make it executable and run directly:

```bash
chmod +x step3_connect.py
./step3_connect.py
```

The script will:
- Connect to Milvus at `localhost:19530`
- Verify the connection is working
- Display server version and existing collections
- Provide troubleshooting tips if connection fails

## Connection Code

### Basic Connection

```python
from pymilvus import connections

connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)
```

### Connection with Verification

The `step3_connect.py` script includes:

```python
from pymilvus import connections, utility

# Connect
connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)

# Verify connection
server_version = utility.get_server_version()
print(f"Milvus Server Version: {server_version}")

# List collections
collections = utility.list_collections()
print(f"Collections: {collections}")
```

## Connection Parameters

* **Host:** `localhost` (default)
* **Port:** `19530` (default gRPC port)
* **Alias:** `default` (connection alias name)

## Verify Connection

After connecting, you can verify the connection:

```python
from pymilvus import connections, utility

# Check if connection exists
if connections.has_connection("default"):
    print("Connected!")
    
    # Get server version
    version = utility.get_server_version()
    print(f"Server version: {version}")
```

## Troubleshooting

### Connection Failed

If you get a connection error:

1. **Check if Milvus is running:**
   ```bash
   cd docker-setup
   docker compose ps
   ```

2. **Start Milvus if not running:**
   ```bash
   cd docker-setup
   ./start.sh
   ```

3. **Check Milvus health:**
   ```bash
   curl http://localhost:9091/healthz
   ```

4. **Verify port is correct:**
   - Default port: `19530`
   - Check `docker-setup/docker-compose.yml` for port mapping

### Common Errors

- **Connection refused:** Milvus is not running or not accessible
- **Timeout:** Milvus is starting up (wait a few seconds and retry)
- **Authentication error:** Check if authentication is required (not needed for default setup)

## Disconnect

To disconnect from Milvus:

```python
from pymilvus import connections

connections.disconnect("default")
```

## Next Steps

Once connected, proceed to [Step 4: Create Collection & Insert Data](step-4-create-collection-insert-data.md).
