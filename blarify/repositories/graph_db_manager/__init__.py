"""Graph database manager implementations."""

from blarify.repositories.graph_db_manager.db_manager import AbstractDbManager, ENVIRONMENT
from blarify.repositories.graph_db_manager.neo4j_manager import Neo4jManager
from blarify.repositories.graph_db_manager.falkordb_manager import FalkorDBManager

def create_db_manager(db_type: str = "neo4j", **connection) -> AbstractDbManager:
    if db_type == "neo4j":
        return Neo4jManager(**connection)
    if db_type in {"falkordb", "falkor_db"}:
        return FalkorDBManager(**connection)
    raise ValueError(f"Unsupported database type: {db_type}")


__all__ = ["AbstractDbManager", "Neo4jManager", "FalkorDBManager", "ENVIRONMENT", "create_db_manager"]
