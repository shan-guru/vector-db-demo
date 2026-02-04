#!/usr/bin/env python3
"""
Step 3: Connect to Milvus from Python

This script establishes a connection to the Milvus Docker instance
and verifies the connection is working.
"""

import sys
from pymilvus import connections, utility


def connect_to_milvus(host="localhost", port="19530", alias="default"):
    """
    Connect to Milvus instance.
    
    Args:
        host (str): Milvus server host
        port (str): Milvus server port
        alias (str): Connection alias name
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        print(f"🔌 Connecting to Milvus at {host}:{port}...")
        
        # Connect to Milvus
        connections.connect(
            alias=alias,
            host=host,
            port=port
        )
        
        print("✅ Successfully connected to Milvus!")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Milvus: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure Milvus Docker containers are running:")
        print("      cd ../docker-setup && ./start.sh")
        print("   2. Check if Milvus is accessible:")
        print("      curl http://localhost:9091/healthz")
        print("   3. Verify the host and port are correct")
        return False


def verify_connection(alias="default"):
    """
    Verify the Milvus connection by checking server status.
    
    Args:
        alias (str): Connection alias name
        
    Returns:
        bool: True if connection is valid, False otherwise
    """
    try:
        # Check if connection exists
        if not connections.has_connection(alias):
            print("❌ No active connection found")
            return False
        
        # Get server version to verify connection
        server_version = utility.get_server_version()
        print(f"📊 Milvus Server Version: {server_version}")
        
        # List existing collections (if any)
        collections = utility.list_collections()
        if collections:
            print(f"📁 Existing collections: {', '.join(collections)}")
        else:
            print("📁 No collections found (this is expected for a new setup)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying connection: {e}")
        return False


def disconnect_from_milvus(alias="default"):
    """
    Disconnect from Milvus instance.
    
    Args:
        alias (str): Connection alias name
    """
    try:
        if connections.has_connection(alias):
            connections.disconnect(alias)
            print(f"🔌 Disconnected from Milvus (alias: {alias})")
    except Exception as e:
        print(f"⚠️  Error disconnecting: {e}")


def main():
    """Main function to run the connection script."""
    print("=" * 50)
    print("Step 3: Connect to Milvus from Python")
    print("=" * 50)
    print()
    
    # Connection parameters
    HOST = "localhost"
    PORT = "19530"
    ALIAS = "default"
    
    # Connect to Milvus
    if not connect_to_milvus(host=HOST, port=PORT, alias=ALIAS):
        print("\n❌ Failed to connect to Milvus. Please check the error messages above.")
        sys.exit(1)
    
    print()
    
    # Verify connection
    if not verify_connection(alias=ALIAS):
        print("\n❌ Connection verification failed.")
        disconnect_from_milvus(alias=ALIAS)
        sys.exit(1)
    
    print()
    print("✅ Connection test completed successfully!")
    print()
    print("💡 The connection is now active and ready to use.")
    print("💡 You can proceed to Step 4: Create Collection & Insert Data")
    print()
    
    # Note: We keep the connection active for subsequent operations
    # To disconnect manually, you can call: disconnect_from_milvus(ALIAS)


if __name__ == "__main__":
    main()
