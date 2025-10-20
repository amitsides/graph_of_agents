# Development Flow: LLM-Assisted Graph of Agents Design

## Overview

This document outlines the two-phase development workflow for creating Hierarchical Multi-Agent Systems (HMAS) using the Graph of Agents framework.

**Workflow Phases:**
1. **Design Phase:** Use an LLM with specialized prompts to design the agent graph
2. **Implementation Phase:** Convert the LLM-generated graph into executable ADK/A2A code

## Phase 1: Design with LLM

### Objective

Leverage an LLM to architect a multi-agent system as a directed graph, identifying:
- Required agent types and their specializations
- Hierarchical relationships between agents
- Control flow patterns (sequential, parallel, iterative)
- State management requirements
- Task decomposition strategy

### Process

#### Step 1: Prepare the Design Prompt

Use a structured prompt that includes:

```markdown
You are an expert in multi-agent system design. Design a Graph of Agents 
architecture for the following problem:

[PROBLEM DESCRIPTION]

Your design should specify:
1. **Agent Nodes:** List each agent with its:
   - Name and role
   - Type (LLM Agent, Custom Agent, or Distributed Node)
   - Specialization and responsibilities
   - Required capabilities/tools

2. **Graph Structure:** Define the hierarchy:
   - Parent-child relationships
   - Sub-agent groupings
   - Delegation pathways

3. **Control Flow:** Specify orchestration patterns:
   - Sequential pipelines (use SequentialAgent)
   - Parallel execution (use ParallelAgent)
   - Iterative refinement (use LoopAgent)
   - Dynamic delegation points

4. **State Management:**
   - Key state variables to track
   - How state flows between agents
   - Output keys for each agent

5. **Termination Conditions:**
   - Success criteria for loops
   - Escalation conditions
   - Failure handling

Provide the design in a structured format ready for code implementation.
```

#### Step 2: Refine the Design

Iterate with the LLM to:
- Clarify ambiguous responsibilities
- Optimize the graph structure for efficiency
- Identify potential bottlenecks or failure points
- Ensure proper error handling and fallback strategies

#### Step 3: Document the Graph

Request a visual representation:
- Mermaid diagram of the agent hierarchy
- ASCII tree structure
- Table of agent specifications

### Example Design Output

The LLM should produce output similar to:

```
Graph Structure:
================

RootAgent (SequentialAgent)
├── PlannerAgent (LLM)
├── ExecutionLoop (LoopAgent)
│   ├── TaskExecutor (LLM)
│   ├── TestRunner (Custom)
│   └── QualityEvaluator (LLM) [escalates on success]
└── ReportGenerator (LLM)

State Flow:
- PlannerAgent writes to: session.state['plan']
- TaskExecutor reads: session.state['plan'], writes: session.state['implementation']
- TestRunner reads: session.state['implementation'], writes: session.state['test_results']
- QualityEvaluator reads: session.state['test_results'], escalates if pass_rate > 0.95
```

## Phase 2: Convert to ADK/A2A Code

### Objective

Transform the LLM-designed graph into working Python code using the ADK/A2A framework.

### Implementation Guidelines

#### 1. Define Individual Agents

Start from the leaf nodes (agents with no sub-agents) and work upward:

```python
from adk import LlmAgent, BaseAgent
from typing import Dict, Any

# Leaf agent example
planner_agent = LlmAgent(
    name="planner",
    model="gpt-4",
    instructions="""You are a planning specialist...
    Output your plan to session.state['plan'].""",
    output_key="plan"  # Automatically saves to session.state
)

# Custom agent example
class TestRunner(BaseAgent):
    async def run(self, ctx: InvocationContext) -> Event:
        implementation = ctx.session.state.get('implementation')
        # Run tests on implementation
        test_results = await self._execute_tests(implementation)
        ctx.session.state['test_results'] = test_results
        return Event(message="Tests completed")
```

#### 2. Build Workflow Agents

Compose agents according to the designed control flow:

```python
from adk import SequentialAgent, LoopAgent, ParallelAgent

# Sequential pipeline
sequential_flow = SequentialAgent(
    name="sequential_flow",
    sub_agents=[agent1, agent2, agent3]
)

# Iterative refinement with termination
iterative_flow = LoopAgent(
    name="execution_loop",
    sub_agents=[executor, tester, evaluator],
    max_iterations=20
)

# Parallel execution
parallel_flow = ParallelAgent(
    name="parallel_research",
    sub_agents=[web_search, db_query, api_call]
)
```

#### 3. Implement Termination Logic

Ensure evaluator agents can signal completion:

```python
class QualityEvaluator(LlmAgent):
    async def run(self, ctx: InvocationContext) -> Event:
        test_results = ctx.session.state.get('test_results')
        
        # Use LLM to evaluate quality
        evaluation = await self._evaluate(test_results)
        
        if evaluation['pass_rate'] > 0.95:
            return Event(
                message="Quality standards met",
                actions=EventActions(escalate=True)  # Terminates LoopAgent
            )
        else:
            return Event(
                message=f"Quality insufficient: {evaluation['feedback']}"
            )
```

#### 4. Assemble the Complete Graph

Build the hierarchy from bottom-up:

```python
# Assemble the full graph
root_agent = SequentialAgent(
    name="root_workflow",
    sub_agents=[
        planner_agent,
        LoopAgent(
            name="execution_loop",
            sub_agents=[task_executor, test_runner, quality_evaluator],
            max_iterations=20
        ),
        report_generator
    ]
)
```

#### 5. Configure Ray for Distribution (Optional)

For distributed execution:

```python
import ray
from adk.ray import RayActorAgent

ray.init()

# Convert agents to Ray Actors for stateful, distributed execution
distributed_executor = RayActorAgent(
    agent=task_executor,
    max_restarts=3,
    max_task_retries=2
)
```

### Code Organization

Structure your implementation:

```
project/
├── agents/
│   ├── __init__.py
│   ├── planner.py          # PlannerAgent definition
│   ├── executor.py         # TaskExecutor definition
│   ├── evaluator.py        # QualityEvaluator definition
│   └── custom_agents.py    # Custom BaseAgent implementations
├── workflows/
│   ├── __init__.py
│   └── main_workflow.py    # Root graph assembly
├── config/
│   ├── prompts.py          # Agent instruction templates
│   └── models.py           # Model configurations
└── main.py                 # Entry point
```

## Validation Checklist

After implementation, verify:

- [ ] All agents from the design are implemented
- [ ] Hierarchical relationships match the designed graph
- [ ] State keys are consistently named and accessed
- [ ] Termination conditions are properly implemented
- [ ] Error handling covers failure scenarios
- [ ] Output keys are configured for pipeline agents
- [ ] Loop agents have reasonable max_iterations
- [ ] Distributed agents have fault tolerance configured
- [ ] Integration tests cover the full workflow

## Best Practices

### During Design Phase

1. **Be Specific:** Provide detailed problem context to the LLM
2. **Iterate:** Refine the design through multiple rounds
3. **Visualize:** Always request a graph diagram
4. **Document Assumptions:** Capture any assumptions made during design

### During Implementation Phase

1. **Start Simple:** Implement a minimal version first
2. **Test Incrementally:** Verify each agent independently before composition
3. **Use Type Hints:** Leverage Python typing for better code quality
4. **Log State Changes:** Add logging for debugging state flow
5. **Handle Edge Cases:** Consider failure modes and add fallbacks

## Example: End-to-End Workflow

```python
# 1. Design with LLM (get the graph structure)
# 2. Implement agents
from agents import PlannerAgent, TaskExecutor, QualityEvaluator, ReportGenerator

# 3. Assemble workflow
workflow = SequentialAgent(
    name="code_generation_workflow",
    sub_agents=[
        PlannerAgent(name="planner"),
        LoopAgent(
            name="dev_loop",
            sub_agents=[
                TaskExecutor(name="executor"),
                QualityEvaluator(name="evaluator")
            ],
            max_iterations=10
        ),
        ReportGenerator(name="reporter")
    ]
)

# 4. Execute
result = await workflow.invoke(
    context={"task": "Build a REST API for user management"}
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Loop never terminates | Verify evaluator returns `escalate=True` on success |
| State not flowing | Check `output_key` configuration and state key names |
| Agents executing in wrong order | Review SequentialAgent sub_agents list order |
| Parallel agents conflicting | Ensure agents write to distinct state keys |
| Ray actors failing | Check `max_restarts` and `max_task_retries` configuration |

## Next Steps

- Review [Graph of Agents README](./README.md) for architectural concepts
- Explore example implementations in `/examples`
- Join discussions on design patterns and best practices
- Contribute your graph designs to the community repository

---

**Remember:** The LLM is your design partner, but you are the engineer who ensures correctness, efficiency, and maintainability of the implementation.