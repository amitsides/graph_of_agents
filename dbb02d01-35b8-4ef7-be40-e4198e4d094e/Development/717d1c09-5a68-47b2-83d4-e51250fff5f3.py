from typing import List, Dict, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GraphNode:
    """Represents a node (agent) in the collaboration graph."""
    node_id: str
    agent_id: str
    label: str
    metadata: Optional[Dict[str, Any]] = None
    
@dataclass
class GraphEdge:
    """Represents an edge (relationship) between agents in the graph."""
    edge_id: str
    from_node_id: str
    to_node_id: str
    edge_type: str  # e.g., "handoff", "collaboration", "escalation"
    weight: float = 1.0
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class CollaborationGraph:
    """Represents a graph of agent collaborations."""
    graph_id: str
    nodes: List[GraphNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph."""
        if any(n.node_id == node.node_id for n in self.nodes):
            raise ValueError(f"Node with id {node.node_id} already exists")
        self.nodes.append(node)
    
    def add_edge(self, edge: GraphEdge) -> None:
        """Add an edge to the graph."""
        # Validate nodes exist
        node_ids = {n.node_id for n in self.nodes}
        if edge.from_node_id not in node_ids:
            raise ValueError(f"Source node {edge.from_node_id} not found in graph")
        if edge.to_node_id not in node_ids:
            raise ValueError(f"Target node {edge.to_node_id} not found in graph")
        self.edges.append(edge)
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get all neighbor node IDs for a given node."""
        return [e.to_node_id for e in self.edges if e.from_node_id == node_id]
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by its ID."""
        return next((n for n in self.nodes if n.node_id == node_id), None)

class GraphBuilder:
    """Service for building and managing agent collaboration graphs."""
    
    def __init__(self):
        self._graphs: Dict[str, CollaborationGraph] = {}
    
    def create_graph(self, graph_id: str, metadata: Optional[Dict[str, Any]] = None) -> CollaborationGraph:
        """Create a new collaboration graph."""
        if graph_id in self._graphs:
            raise ValueError(f"Graph with id {graph_id} already exists")
        
        _graph = CollaborationGraph(graph_id=graph_id, metadata=metadata)
        self._graphs[graph_id] = _graph
        return _graph
    
    def get_graph(self, graph_id: str) -> Optional[CollaborationGraph]:
        """Retrieve a graph by its ID."""
        return self._graphs.get(graph_id)
    
    def add_agent_node(self, graph_id: str, agent_id: str, label: str, 
                      metadata: Optional[Dict[str, Any]] = None) -> GraphNode:
        """Add an agent node to a graph."""
        _graph = self.get_graph(graph_id)
        if not _graph:
            raise ValueError(f"Graph {graph_id} not found")
        
        _node_id = f"node_{agent_id}"
        _node = GraphNode(node_id=_node_id, agent_id=agent_id, label=label, metadata=metadata)
        _graph.add_node(_node)
        return _node
    
    def add_relationship(self, graph_id: str, from_agent_id: str, to_agent_id: str,
                        edge_type: str, weight: float = 1.0,
                        metadata: Optional[Dict[str, Any]] = None) -> GraphEdge:
        """Add a relationship (edge) between two agents in a graph."""
        _graph = self.get_graph(graph_id)
        if not _graph:
            raise ValueError(f"Graph {graph_id} not found")
        
        _from_node_id = f"node_{from_agent_id}"
        _to_node_id = f"node_{to_agent_id}"
        _edge_id = f"edge_{from_agent_id}_to_{to_agent_id}_{edge_type}"
        
        _edge = GraphEdge(
            edge_id=_edge_id,
            from_node_id=_from_node_id,
            to_node_id=_to_node_id,
            edge_type=edge_type,
            weight=weight,
            metadata=metadata
        )
        _graph.add_edge(_edge)
        return _edge
    
    def get_agent_connections(self, graph_id: str, agent_id: str) -> List[Tuple[str, str]]:
        """Get all connections for an agent (returns list of (connected_agent_id, edge_type))."""
        _graph = self.get_graph(graph_id)
        if not _graph:
            raise ValueError(f"Graph {graph_id} not found")
        
        _node_id = f"node_{agent_id}"
        _connections = []
        
        for _edge in _graph.edges:
            if _edge.from_node_id == _node_id:
                _target_node = _graph.get_node(_edge.to_node_id)
                if _target_node:
                    _connections.append((_target_node.agent_id, _edge.edge_type))
        
        return _connections
    
    def validate_graph(self, graph_id: str) -> Tuple[bool, List[str]]:
        """Validate a graph structure and return validation status and errors."""
        _graph = self.get_graph(graph_id)
        if not _graph:
            return False, [f"Graph {graph_id} not found"]
        
        _errors = []
        
        # Check for isolated nodes
        _connected_nodes = set()
        for _edge in _graph.edges:
            _connected_nodes.add(_edge.from_node_id)
            _connected_nodes.add(_edge.to_node_id)
        
        _all_node_ids = {n.node_id for n in _graph.nodes}
        _isolated = _all_node_ids - _connected_nodes
        if _isolated:
            _errors.append(f"Isolated nodes found: {_isolated}")
        
        # Check for cycles (simple detection)
        _has_cycle = self._detect_cycle(_graph)
        if _has_cycle:
            _errors.append("Graph contains cycles")
        
        return len(_errors) == 0, _errors
    
    def _detect_cycle(self, graph: CollaborationGraph) -> bool:
        """Simple cycle detection using DFS."""
        _visited = set()
        _rec_stack = set()
        
        def _dfs(_node_id: str) -> bool:
            _visited.add(_node_id)
            _rec_stack.add(_node_id)
            
            for _neighbor_id in graph.get_neighbors(_node_id):
                if _neighbor_id not in _visited:
                    if _dfs(_neighbor_id):
                        return True
                elif _neighbor_id in _rec_stack:
                    return True
            
            _rec_stack.remove(_node_id)
            return False
        
        for _node in graph.nodes:
            if _node.node_id not in _visited:
                if _dfs(_node.node_id):
                    return True
        
        return False

print("GraphBuilder service created successfully")
print("  - Classes: GraphNode, GraphEdge, CollaborationGraph")
print("  - Service: GraphBuilder")
print("  - Key methods: create_graph(), add_agent_node(), add_relationship()")
print("  - Validation: validate_graph() with cycle detection")