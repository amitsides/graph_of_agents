import uuid
from datetime import datetime

# Create specialized agents with skills
print("=== Setting up Demo Agents ===\n")

# Create skills for different agents using available classes
demo_skill_discovery = AgentSkill(
    name="capability_discovery",
    description="Discover and analyze agent capabilities",
    parameters={"discovery_depth": "full", "include_metadata": True},
    examples=["Discover all available agents", "Analyze skill coverage"]
)

demo_skill_orchestration = AgentSkill(
    name="task_orchestration",
    description="Orchestrate and coordinate multi-agent workflows",
    parameters={"max_parallel_tasks": 10, "coordination_strategy": "adaptive"},
    examples=["Coordinate data pipeline", "Manage agent handoffs"]
)

demo_skill_execution = AgentSkill(
    name="task_execution",
    description="Execute assigned tasks and generate results",
    parameters={"execution_mode": "async", "retry_limit": 3},
    examples=["Process data analysis", "Generate reports"]
)

# Initialize agents with proper lifecycle
demo_discovery_agent = LlmAgent(
    agent_id="discovery_001",
    name="DiscoveryAgent",
    description="Discovers available agents and their capabilities",
    model_name="gpt-4",
    temperature=0.3
)

demo_orchestrator_agent = OrchestrationAgent(
    agent_id="orchestrator_001",
    name="OrchestratorAgent",
    description="Coordinates tasks across multiple agents",
    max_concurrent_tasks=5
)

demo_executor_agent = LlmAgent(
    agent_id="executor_001",
    name="ExecutorAgent",
    description="Executes assigned tasks and generates results",
    model_name="gpt-4",
    temperature=0.7
)

# Initialize agents
demo_discovery_agent.initialize()
demo_orchestrator_agent.initialize()
demo_executor_agent.initialize()

# Start agents
demo_discovery_agent.start()
demo_orchestrator_agent.start()
demo_executor_agent.start()

# Register executor as sub-agent of orchestrator
demo_orchestrator_agent.register_agent(demo_executor_agent)

print(f"\n✓ Created {demo_discovery_agent.name} - {demo_discovery_agent.get_status()['state']}")
print(f"✓ Created {demo_orchestrator_agent.name} - {demo_orchestrator_agent.get_status()['state']}")
print(f"✓ Created {demo_executor_agent.name} - {demo_executor_agent.get_status()['state']}")
print(f"\n✓ Orchestrator has {len(demo_orchestrator_agent.get_sub_agents())} registered sub-agent(s)")
