# Step 1: Run Milvus Using Docker

We use the **official Milvus standalone Docker setup**.

## Start Milvus

```bash
docker compose up -d
```

Milvus will be available at:

* **Host:** `localhost`
* **Port:** `19530`

> This setup uses the latest stable Milvus version and avoids deprecated APIs.
