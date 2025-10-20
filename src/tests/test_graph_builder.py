# Test GraphBuilder service - need to import dependencies
from typing import List, Dict, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime

# Re-import the classes to ensure they're available in this block
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
    edge_type: str
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
        _node_ids = {n.node_id for n in self.nodes}
        if edge.from_node_id not in _node_ids:
            raise ValueError(f"Source node {edge.from_node_id} not found in graph")
        if edge.to_node_id not in _node_ids:
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
        """Get all connections for an agent."""
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
        """Validate a graph structure."""
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
            _errors.append(f"Isolated nodes: {_isolated}")
        
        return len(_errors) == 0, _errors

# Test GraphBuilder service
test_graph_builder = GraphBuilder()

# Test 1: Create a new graph
print("Test 1: Create collaboration graph")
test_collab_graph = test_graph_builder.create_graph(
    graph_id="test_graph_001",
    metadata={"project": "agent_collaboration", "version": "1.0"}
)
print(f"  ✓ Created: {test_collab_graph.graph_id}")

# Test 2: Add agent nodes
print("\nTest 2: Add agent nodes")
test_node1 = test_graph_builder.add_agent_node(
    graph_id="test_graph_001",
    agent_id="agent_001",
    label="Data Analyst"
)
print(f"  ✓ Node 1: {test_node1.label}")

test_node2 = test_graph_builder.add_agent_node(
    graph_id="test_graph_001",
    agent_id="agent_002",
    label="ML Engineer"
)
print(f"  ✓ Node 2: {test_node2.label}")

# Test 3: Add relationships
print("\nTest 3: Add relationships")
test_edge1 = test_graph_builder.add_relationship(
    graph_id="test_graph_001",
    from_agent_id="agent_001",
    to_agent_id="agent_002",
    edge_type="handoff"
)
print(f"  ✓ Edge: {test_edge1.edge_type}")

# Test 4: Validate
print("\nTest 4: Validate graph")
test_valid, test_errors = test_graph_builder.validate_graph("test_graph_001")
print(f"  Valid: {test_valid}")

print("\n✓ GraphBuilder tests completed")