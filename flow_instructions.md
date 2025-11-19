# Development Flow: Spanner-Hosted Graph of Agents

## Overview

This document outlines the two-phase development workflow for creating Hierarchical Multi-Agent Systems (HMAS) where the agent graph is hosted and managed in Google Cloud Spanner.

**Workflow Phases:**
1.  **Design Phase:** Use an LLM with specialized prompts to design the agent graph.
2.  **Implementation Phase:** Model and implement the LLM-generated graph in Spanner, with a central orchestrator to drive execution.

## Phase 1: Design with LLM

### Objective

Leverage an LLM to architect a multi-agent system as a directed graph, identifying:
- Required agent types and their specializations
- Hierarchical relationships and delegation pathways
- Control flow patterns (sequential, parallel, iterative)
- State management requirements
- Task decomposition strategy

### Process

#### Step 1: Prepare the Design Prompt

Use a structured prompt that includes:

```markdown
You are an expert in distributed, database-driven multi-agent system design. Design a Graph of Agents architecture for the following problem, assuming the graph will be stored and orchestrated from a Spanner database:

[PROBLEM DESCRIPTION]

Your design should specify:
1.  **Agent Nodes:** List each agent with its:
    -   `agent_id` (a unique identifier)
    -   Name and role
    -   Type (e.g., LLM-based, Tool-based, Human-in-the-loop)
    -   Specialization and responsibilities (which can be used as instructions/prompts)

2.  **Graph Structure:** Define the hierarchy and data flow:
    -   Parent-child relationships (e.g., `agent_A` delegates to `agent_B` and `agent_C`)
    -   Control flow (e.g., `agent_B` must complete before `agent_C` starts)

3.  **State Management:**
    -   Key state variables to track per session
    -   How state is passed between agents (e.g., which outputs from one agent become inputs for another)

4.  **Termination Conditions:**
    -   Success criteria for the overall graph
    -   Conditions for retries or escalations

Provide the design in a structured format ready for database schema implementation.
```

#### Step 2: Refine the Design

Iterate with the LLM to:
- Clarify ambiguous responsibilities.
- Optimize the graph for efficient database-driven execution.
- Identify potential race conditions or deadlocks.
- Ensure robust error handling and fallback strategies.

#### Step 3: Document the Graph

Request a visual representation and a data-oriented summary:
- Mermaid diagram of the agent hierarchy.
- A list of agents and their relationships in a format that maps directly to database tables.

### Example Design Output

The LLM should produce output similar to:

```
Agent Definitions:
==================
- agent_id: 'planner_001', role: 'Plan generation agent'
- agent_id: 'executor_001', role: 'Executes a single step of a plan'
- agent_id: 'evaluator_001', role: 'Evaluates the output of the executor'
- agent_id: 'reporter_001', role: 'Generates the final report'

Graph Relationships (Parent, Child, Type):
=========================================
- ('root', 'planner_001', 'SEQUENTIAL_NEXT')
- ('planner_001', 'executor_001', 'ITERATIVE_START')
- ('executor_001', 'evaluator_001', 'SEQUENTIAL_NEXT')
- ('evaluator_001', 'executor_001', 'ITERATIVE_LOOP')
- ('evaluator_001', 'reporter_001', 'ITERATIVE_EXIT')

State Flow:
- `planner_001` writes to: `session.state['plan']`
- `executor_001` reads: `session.state['plan']`, writes: `session.state['implementation_step']`
- `evaluator_001` reads: `session.state['implementation_step']`, decides whether to loop back to `executor_001` or exit to `reporter_001`.
```

## Phase 2: Implement with Spanner

### Objective

Transform the LLM-designed graph into a robust, scalable system using Spanner as the backend for storing the graph, tasks, and state.

### Spanner Schema Design

Define Spanner tables to represent the system.

**1. `Agents` Table:** Stores the definition of each agent node.
```sql
CREATE TABLE Agents (
    AgentId        STRING(36) NOT NULL,
    Name           STRING(1024),
    Role           STRING(MAX),
    Instructions   STRING(MAX), -- The agent's system prompt or operational instructions
    AgentType      STRING(100), -- e.g., 'LLM', 'TOOL'
    -- Other metadata
) PRIMARY KEY (AgentId);
```

**2. `AgentRelationships` Table:** Defines the graph edges and control flow.
```sql
CREATE TABLE AgentRelationships (
    ParentAgentId  STRING(36) NOT NULL,
    ChildAgentId   STRING(36) NOT NULL,
    RelationshipType STRING(100), -- e.g., 'SEQUENTIAL', 'PARALLEL', 'ITERATIVE_LOOP'
    ExecutionOrder INT64,       -- For ordering sequential/parallel tasks
) PRIMARY KEY (ParentAgentId, ChildAgentId);
```

**3. `Tasks` Table:** Manages the lifecycle of tasks executed by agents.
```sql
CREATE TABLE Tasks (
    TaskId         STRING(36) NOT NULL,
    SessionId      STRING(36) NOT NULL,
    AssignedAgentId STRING(36) NOT NULL,
    Status         STRING(50) NOT NULL, -- e.g., 'PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED'
    InputPayload   JSON,
    OutputResult   JSON,
    CreatedAt      TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
    UpdatedAt      TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
) PRIMARY KEY (SessionId, TaskId);
```

**4. `SessionState` Table:** Holds the shared state for a given execution graph.
```sql
CREATE TABLE SessionState (
    SessionId      STRING(36) NOT NULL,
    StateKey       STRING(256) NOT NULL,
    StateValue     JSON,
    UpdatedAt      TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
) PRIMARY KEY (SessionId, StateKey);
```

### Implementation Guidelines

#### 1. The Orchestrator

The core of the system is an orchestrator service that drives the execution.
- **Starts a Session:** Creates a new `SessionId`.
- **Reads the Graph:** Queries `AgentRelationships` to understand the workflow.
- **Manages Tasks:**
    - Creates the initial task(s) in the `Tasks` table for the root agent(s).
    - Continuously polls the `Tasks` table for `COMPLETED` tasks.
    - When a task is complete, it determines the next agent(s) from `AgentRelationships`.
    - It prepares the `InputPayload` for the next tasks using data from `SessionState` or the previous task's `OutputResult`.
    - It creates new `PENDING` tasks for the next agent(s).
- **Manages State:** Reads and writes to the `SessionState` table as needed.

#### 2. The Agent Workers

Each agent is an independent, stateless worker process/service.
- **Polls for Tasks:** Periodically queries the `Tasks` table for `PENDING` tasks with its `AgentId`.
- **Executes Work:**
    - On finding a task, it updates the status to `IN_PROGRESS`.
    - It performs its function (e.g., calls an LLM, runs a tool) using the `InputPayload`.
    - It updates the task in Spanner with the `OutputResult` and sets the status to `COMPLETED` or `FAILED`.
- **Is Stateless:** All necessary information comes from the task's `InputPayload`. All results are written back. This allows for easy scaling and fault tolerance.

### Code Example (Python with `google-cloud-spanner`)

**Agent Worker Logic:**
```python
from google.cloud import spanner
import time
import json

AGENT_ID = "executor_001"

def process_task(task_data):
    # Business logic for the agent
    print(f"Executing task: {task_data['TaskId']}")
    # ... call LLM, run tool, etc. ...
    input_payload = json.loads(task_data['InputPayload'])
    result = {"status": "success", "detail": f"Processed plan: {input_payload.get('plan')}"}
    return json.dumps(result)

def agent_worker_loop():
    spanner_client = spanner.Client()
    instance = spanner_client.instance("my-instance")
    database = instance.database("my-database")

    while True:
        with database.snapshot() as snapshot:
            # Find a pending task
            results = snapshot.execute_sql(
                "SELECT * FROM Tasks WHERE AssignedAgentId = @agent_id AND Status = 'PENDING' LIMIT 1",
                params={"agent_id": AGENT_ID},
                param_types={"agent_id": spanner.param_types.STRING},
            )
            task = next(results, None)

        if task:
            session_id, task_id = task.SessionId, task.TaskId
            
            def update_task_transaction(transaction):
                # Set to IN_PROGRESS
                transaction.update(
                    table="Tasks",
                    columns=["SessionId", "TaskId", "Status"],
                    values=[[session_id, task_id, "IN_PROGRESS"]],
                )
            database.run_in_transaction(update_task_transaction)

            # Execute and save result
            output_result = process_task(task)
            
            def finalize_task_transaction(transaction):
                transaction.update(
                    table="Tasks",
                    columns=["SessionId", "TaskId", "Status", "OutputResult"],
                    values=[[session_id, task_id, "COMPLETED", output_result]],
                )
            database.run_in_transaction(finalize_task_transaction)
        else:
            time.sleep(5) # Wait before polling again
```

### Code Organization

```
project/
├── schemas/
│   └── spanner_schema.sql  # DDL for Spanner tables
├── orchestrator/
│   └── main.py             # Main orchestrator service logic
├── agents/
│   ├── __init__.py
│   ├── planner_agent.py    # Worker for the planner agent
│   └── executor_agent.py   # Worker for the executor agent
├── common/
│   └── db.py               # Spanner client and helper functions
└── main.py                 # Entry point to start services
```

## Validation Checklist

- [ ] Spanner schema is created and indexes are in place for performance.
- [ ] All agents from the design have a corresponding worker implementation.
- [ ] The orchestrator correctly traverses the graph based on `AgentRelationships`.
- [ ] State is correctly passed between tasks via `SessionState` and `InputPayload`/`OutputResult`.
- [ ] Termination and loop conditions are correctly handled by the orchestrator.
- [ ] Agent workers are fault-tolerant and can recover from transient errors.
- [ ] Integration tests verify a full session runs from start to finish.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Orchestrator doesn't create next task | Check the `RelationshipType` logic and ensure the previous task status is `COMPLETED`. |
| Agent processes the same task twice | Ensure the agent's transaction correctly sets the task status to `IN_PROGRESS` immediately after selection. Use Spanner's strong consistency. |
| State not flowing correctly | Verify the orchestrator is correctly mapping `OutputResult` and `SessionState` to the next task's `InputPayload`. Check for JSON serialization issues. |
| Deadlock in database | Analyze transactions for long-running operations. Ensure workers only hold locks for short periods when updating task status. |

---

**Remember:** This paradigm shifts complexity from a stateful application framework to a stateless, database-driven architecture. The LLM is your design partner, and you are the engineer who ensures the data models, transactions, and services are correct, scalable, and maintainable.
