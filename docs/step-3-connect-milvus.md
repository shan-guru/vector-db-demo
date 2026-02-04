# Step 3: Connect to Milvus from Python

Example connection:

```python
from pymilvus import connections

connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)
```

This establishes a connection to the Milvus Docker instance created in Step 1.
