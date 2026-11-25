from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any, LiteralString, Optional

from blarify.repositories.graph_db_manager.graph_queries import (
    detach_delete_nodes_by_diff_identifier_query,
    detach_delete_nodes_by_node_ids_query,
    detach_delete_nodes_by_paths_query,
    match_empty_folders_query,
)
from blarify.repositories.graph_db_manager.dtos.node_search_result_dto import ReferenceSearchResultDTO


class ENVIRONMENT(Enum):
    MAIN = "main"
    DEV = "dev"


class AbstractDbManager(ABC):
    @abstractmethod
    def close(self):
        """Close the connection to the database."""
        raise NotImplementedError

    @abstractmethod
    def save_graph(self, nodes: List[Any], edges: List[Any]) -> None:
        """Save nodes and edges to the database."""
        raise NotImplementedError

    @abstractmethod
    def create_nodes(self, nodeList: List[Any]) -> None:
        """Create nodes in the database."""
        raise NotImplementedError

    @abstractmethod
    def create_edges(self, edgesList: List[Any]) -> None:
        """Create edges between nodes in the database."""
        raise NotImplementedError

    def detatch_delete_nodes_with_path(self, path: str) -> None:
        """Backward-compatible spelling used by earlier clients."""
        return self.detach_delete_nodes_with_path(path)

    def detach_delete_nodes_by_paths(self, file_paths: list[str]) -> None:
        self.query(detach_delete_nodes_by_paths_query(), {"file_paths": file_paths}, transaction=True)

    def detach_delete_nodes_by_diff_identifier(self, diff_identifier: str) -> None:
        self.query(detach_delete_nodes_by_diff_identifier_query(), {"diff_identifier": diff_identifier}, transaction=True)

    def detach_delete_nodes_by_node_ids(self, node_ids: list[str]) -> None:
        self.query(detach_delete_nodes_by_node_ids_query(), {"node_ids": node_ids}, transaction=True)

    def match_empty_folders(self) -> list[dict]:
        return self.query(match_empty_folders_query(), {})

    @abstractmethod
    def detach_delete_nodes_with_path(self, path: str) -> None:
        """Detach and delete nodes matching the given path."""
        raise NotImplementedError

    @abstractmethod
    def query(
        self, cypher_query: LiteralString, parameters: Optional[Dict[str, Any]] = None, transaction: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return the results.

        Args:
            cypher_query: The Cypher query string to execute
            parameters: Optional dictionary of parameters for the query

        Returns:
            List of dictionaries containing the query results
        """
        raise NotImplementedError

    def get_node_by_id(
        self,
        node_id: str,
    ) -> ReferenceSearchResultDTO:
        """
        Retrieve a node from the database by its ID.

        Args:
            node_id: The ID of the node to retrieve.

        Returns:
            A dictionary representing the node, or None if not found.
        """
        raise NotImplementedError

    def get_node_by_name_and_type(
        self,
        name: str,
        node_type: str,
    ):
        """
        Retrieve nodes by name and type from the database.

        Args:
            name: Name of the node to search for
            node_type: Type/label of the node to search for

        Returns:
            List of node data transfer objects

        Note:
            entity_id (mandatory) and repo_id (optional) are injected from manager instance.
            If repo_id is None, searches across all repos for the entity.
        """
        raise NotImplementedError

    def get_nodes_by_name_type_and_path(
        self,
        node_type: str,
        name: Optional[str] = None,
        path_contains: Optional[str] = None,
    ):
        """
        Retrieve nodes by type with optional name and path filtering.

        Args:
            node_type: Type/label of the node to search for
            name: Optional exact name match
            path_contains: Optional path substring to filter by

        Returns:
            List of node data transfer objects

        Note:
            At least one of name or path_contains should be provided.
        """
        raise NotImplementedError
