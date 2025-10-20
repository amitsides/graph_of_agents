from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    """Status of a task in the A2A protocol."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """Priority levels for tasks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class TaskCard:
    """Represents a task to be executed by an agent."""
    task_id: str
    title: str
    description: str
    required_skills: List[str]
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_agent_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate the task card data."""
        if not self.task_id or not isinstance(self.task_id, str):
            raise ValueError("Task ID must be a non-empty string")
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Task title must be a non-empty string")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Task description must be a non-empty string")
        if not isinstance(self.required_skills, list):
            raise ValueError("Required skills must be a list")
        if not isinstance(self.status, TaskStatus):
            raise ValueError("Status must be a TaskStatus enum")
        if not isinstance(self.priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority enum")
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

# Test with sample data
task_card_sample = TaskCard(
    task_id="task_001",
    title="Analyze Q4 Sales Data",
    description="Generate insights from Q4 sales dataset",
    required_skills=["data_analysis", "visualization"],
    status=TaskStatus.PENDING,
    priority=TaskPriority.HIGH,
    assigned_agent_id="agent_001",
    context={"dataset": "sales_q4.csv", "metrics": ["revenue", "growth"]}
)

print("TaskCard created successfully:")
print(f"  Task ID: {task_card_sample.task_id}")
print(f"  Title: {task_card_sample.title}")
print(f"  Description: {task_card_sample.description}")
print(f"  Required Skills: {task_card_sample.required_skills}")
print(f"  Status: {task_card_sample.status.value}")
print(f"  Priority: {task_card_sample.priority.value}")
print(f"  Assigned to: {task_card_sample.assigned_agent_id}")