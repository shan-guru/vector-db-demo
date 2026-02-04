"""
Milvus Connection Utility Module

This module provides reusable functions for connecting to Milvus
and can be imported by other scripts.
"""

from pymilvus import connections, utility
from typing import Optional, Tuple


def connect(
    host: str = "localhost",
    port: str = "19530",
    alias: str = "default"
) -> bool:
    """
    Connect to Milvus instance.
    
    Args:
        host (str): Milvus server host. Default: "localhost"
        port (str): Milvus server port. Default: "19530"
        alias (str): Connection alias name. Default: "default"
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Check if already connected
        if connections.has_connection(alias):
            print(f"ℹ️  Already connected to Milvus (alias: {alias})")
            return True
        
        # Connect to Milvus
        connections.connect(
            alias=alias,
            host=host,
            port=port
        )
        
        print(f"✅ Connected to Milvus at {host}:{port}")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Milvus: {e}")
        return False


def disconnect(alias: str = "default") -> None:
    """
    Disconnect from Milvus instance.
    
    Args:
        alias (str): Connection alias name. Default: "default"
    """
    try:
        if connections.has_connection(alias):
            connections.disconnect(alias)
            print(f"🔌 Disconnected from Milvus (alias: {alias})")
    except Exception as e:
        print(f"⚠️  Error disconnecting: {e}")


def get_connection_info(alias: str = "default") -> Optional[Tuple[str, str]]:
    """
    Get connection information.
    
    Args:
        alias (str): Connection alias name. Default: "default"
        
    Returns:
        Optional[Tuple[str, str]]: (host, port) if connected, None otherwise
    """
    try:
        if connections.has_connection(alias):
            # Get connection details
            # Note: pymilvus doesn't expose connection details directly
            # This is a placeholder for future enhancement
            return ("localhost", "19530")
        return None
    except Exception:
        return None


def verify_connection(alias: str = "default") -> bool:
    """
    Verify the Milvus connection is working.
    
    Args:
        alias (str): Connection alias name. Default: "default"
        
    Returns:
        bool: True if connection is valid, False otherwise
    """
    try:
        if not connections.has_connection(alias):
            return False
        
        # Try to get server version to verify connection
        server_version = utility.get_server_version()
        print(f"📊 Milvus Server Version: {server_version}")
        return True
        
    except Exception as e:
        print(f"❌ Connection verification failed: {e}")
        return False


def list_collections() -> list:
    """
    List all collections in Milvus.
    
    Returns:
        list: List of collection names
    """
    try:
        collections = utility.list_collections()
        return collections
    except Exception as e:
        print(f"❌ Error listing collections: {e}")
        return []
