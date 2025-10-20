# GraphBuilder and CardBuilder Services

## Overview
This implementation provides two core services for managing agent collaboration graphs and entity cards in the A2A protocol:

## 1. GraphBuilder Service
**Location:** `services.graph_builder`

### Purpose
Manages agent collaboration graphs with nodes (agents) and edges (relationships).

### Key Classes
- **GraphNode**: Represents an agent node in the graph
  - `node_id`, `agent_id`, `label`, `metadata`
- **GraphEdge**: Represents a relationship between agents
  - `edge_id`, `from_node_id`, `to_node_id`, `edge_type`, `weight`, `metadata`
- **CollaborationGraph**: The graph structure
  - `graph_id`, `nodes`, `edges`, `metadata`, `created_at`
  - Methods: `add_node()`, `add_edge()`, `get_neighbors()`, `get_node()`

### GraphBuilder Methods
- `create_graph(graph_id, metadata)` - Create new collaboration graph
- `get_graph(graph_id)` - Retrieve graph by ID
- `add_agent_node(graph_id, agent_id, label, metadata)` - Add agent to graph
- `add_relationship(graph_id, from_agent_id, to_agent_id, edge_type, weight, metadata)` - Create edge
- `get_agent_connections(graph_id, agent_id)` - Get agent's connections
- `validate_graph(graph_id)` - Validate graph structure (checks for isolated nodes and cycles)

### Test Results
✓ Graph creation with metadata
✓ Node addition (3 agents added)
✓ Edge creation (2 relationships)
✓ Connection retrieval
✓ Graph validation

---

## 2. CardBuilder Service
**Location:** `services.card_builder`

### Purpose
Creates and manages entity cards for agents, tasks, and skills with validation and relationship linking.

### Key Classes
- **EntityCard**: Base card structure
  - `card_id`, `card_type`, `created_at`, `updated_at`, `metadata`
  - Method: `to_dict()` - Convert to dictionary

### CardBuilder Methods
- `create_agent_card(agent_id, name, description, skills, version, metadata)` - Create agent card
- `create_task_card(task_id, title, description, required_skills, status, priority, assigned_agent_id, context)` - Create task card
- `create_skill_card(skill_name, description, parameters, examples)` - Create skill card
- `get_card(card_id)` - Retrieve card by ID
- `update_card(card_id, updates)` - Update existing card
- `link_cards(source_card_id, target_card_id, relationship_type)` - Link two cards
- `validate_card(card_id)` - Validate card structure (type-specific validation)
- `list_cards_by_type(card_type)` - Get all cards of a type

### Test Results
✓ Agent card creation with validation
✓ Task card creation with validation
✓ Skill card creation with validation
✓ Card validation (agent and task cards)
✓ Card linking with relationships

---

## Integration
Both services are designed to work together:
- **Agent cards** contain agent metadata (ID, name, description, skills)
- **Graph nodes** reference agents and can include card IDs in metadata
- **Graph edges** represent handoffs, collaborations, and escalations between agents
- **Card relationships** can mirror or complement graph edges

## Success Criteria Met
✅ GraphBuilder creates valid collaboration graphs
✅ Graphs support nodes (agents) and edges (relationships)
✅ Graph validation includes cycle detection and isolated node checks
✅ CardBuilder creates entity cards for agents, tasks, and skills
✅ Cards include proper validation for required fields
✅ Cards can be linked with relationships
✅ Both services properly manage entities with CRUD operations

## Usage Example
```python
# Create services
graph_builder = GraphBuilder()
card_builder = CardBuilder()

# Create agent card
agent_card = card_builder.create_agent_card(
    agent_id="agent_001",
    name="Data Analyst",
    description="Analyzes data",
    skills=["data_analysis", "sql"]
)

# Create graph and add agent
graph = graph_builder.create_graph("team_graph")
node = graph_builder.add_agent_node(
    graph_id="team_graph",
    agent_id="agent_001",
    label="Data Analyst",
    metadata={"card_id": agent_card['card_id']}
)

# Add relationships
edge = graph_builder.add_relationship(
    graph_id="team_graph",
    from_agent_id="agent_001",
    to_agent_id="agent_002",
    edge_type="handoff"
)

# Validate
is_valid, errors = graph_builder.validate_graph("team_graph")
```