# Graph of Agents: Hierarchical Multi-Agent System (HMAS)

[![Status](https://img.shields.io/badge/status-proof--of--concept-yellow)](https://github.com/yourusername/graph-of-agents)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> A structured, graph-based architecture for defining and executing Hierarchical Multi-Agent Systems with composable, specialized agents.

## Overview

Graph of Agents (GoA) provides a framework for building complex AI applications through hierarchical multi-agent orchestration. By representing agentic workflows as directed graphs, GoA enables modular design where specialized agents collaborate to achieve sophisticated, long-term goals.

This architecture leverages proven multi-agent patterns including task decomposition, iterative refinement, and hierarchical delegation to ensure modularity, specialization, and resilience.

## Key Concepts

### Agent Hierarchy as Graph Structure

The system defines agent hierarchies by passing agent instances to the `sub_agents` argument during parent agent initialization, creating a tree structure where:

- **Nodes** represent specialized agents with distinct capabilities
- **Edges** define control flow and communication pathways
- **State** flows through the graph via shared session context

## Architecture

### 1. Agent Nodes

Each node represents a specialized component with specific responsibilities:

| Node Type | Role | Implementation |
|-----------|------|----------------|
| **LLM Agents** | Reasoning, planning, and content generation | ADK `LlmAgent` |
| **Custom Agents** | Specialized non-LLM logic (code execution, testing, validation) | ADK `BaseAgent` |
| **Distributed Nodes** | Stateful workers for parallel and shared-state operations | Ray Actors / Tasks |

This modular structure mirrors cognitive architectures like ACT-R, where specialized modules handle distinct cognitive functions.

### 2. Graph Edges (Orchestration)

Control flow is managed through ADK Workflow Agents, enabling various execution patterns:

| Pattern | Agent Type | Description | State Management |
|---------|-----------|-------------|------------------|
| **Sequential Pipeline** | `SequentialAgent` | Execute sub-agents in fixed order | Output of one feeds into next |
| **Parallel Execution** | `ParallelAgent` | Run sub-agents concurrently | Concurrent writes to distinct state keys |
| **Iterative Refinement** | `LoopAgent` | Repeat execution until condition met | State persists across iterations |
| **Dynamic Delegation** | Parent-Child | Route tasks to specialist agents | LLM-driven (`transfer_to_agent`) or explicit (`AgentTool`) |

## Core Features

### State Management

Agents communicate through **Shared Session State** accessed via `InvocationContext`. This passive communication pattern enables:

- Pipeline composition where agent outputs become inputs for downstream agents
- Coordinated multi-agent collaboration
- Traceable data flow through the execution graph

### Iterative Refinement Pattern

The `LoopAgent` enables persistent goal pursuit through continuous iteration:

```python
# Loop continues until evaluator signals completion
loop_agent = LoopAgent(
    sub_agents=[worker_agent, critic_agent],
    max_iterations=100
)
```

**Termination mechanism:**
- Evaluator/Critic agent assesses task completion
- Success signaled via `Event` with `escalate=True` in `EventActions`
- Forces loop termination and returns control to parent

**Fault tolerance:** When using Ray runtime, configure `max_restarts` and `max_task_retries` on Actors for automatic recovery from crashes.

### Hierarchical Task Decomposition

Complex problems are solved through recursive task breakdown:

```
ReportWriter (high-level)
    ├── ResearchAssistant (mid-level)
    │   ├── WebSearchTool
    │   └── DataAnalyzer
    └── ContentGenerator (mid-level)
        ├── OutlineCreator
        └── SectionWriter
```

This mirrors problem-solving approaches in Soar, where complex goals trigger substates for specialized processing.

### Distributed Execution

Ray integration enables scalable, distributed computing:

- **Stateful Services:** Ray Actors provide dedicated worker processes
- **Parallelism:** Methods on different Actors execute concurrently
- **Cognitive DAGs:** Orchestration as compiled graphs linking Perception → Planning → Action → Evaluation

## Theoretical Foundations

GoA draws inspiration from cognitive architecture research:

### ACT-R (Adaptive Control of Thought—Rational)

ACT-R organizes cognition through specialized modules (declarative/procedural memory, perception, motor control) that communicate via buffers. GoA mirrors this with:

- Specialized agent modules for distinct functions
- Controlled information flow between agents
- Separation of knowledge representation and processing

### Soar (State, Operator, And Result)

Soar's Problem Space Hypothesis views problem-solving as search through states via operator application. GoA implements this through:

- State-driven workflow execution (`LoopAgent`, `SequentialAgent`)
- Operator decomposition via hierarchical agents
- Subgoal creation through agent delegation

## Getting Started

```python
from adk import LlmAgent, SequentialAgent, LoopAgent

# Define specialized agents
planner = LlmAgent(name="planner", model="gpt-4")
executor = LlmAgent(name="executor", model="gpt-4")
critic = LlmAgent(name="critic", model="gpt-4")

# Create iterative workflow
workflow = LoopAgent(
    name="iterative_solver",
    sub_agents=[planner, executor, critic],
    max_iterations=10
)

# Execute
result = workflow.invoke(task="Solve complex problem")
```

## Use Cases

- **Autonomous Research Systems:** Multi-stage research with iterative refinement
- **Code Generation Pipelines:** Planning → Implementation → Testing → Refinement
- **Content Creation Workflows:** Research → Outline → Draft → Review → Polish
- **Decision Support Systems:** Data gathering → Analysis → Recommendation → Validation

## Project Status

This project is currently in **proof-of-concept** stage, exploring patterns for distributed multi-agent orchestration. Contributions and feedback welcome!

## Acknowledgments

Inspired by research in cognitive architectures (ACT-R, Soar) and modern multi-agent systems design patterns.