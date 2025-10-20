from typing import Optional, Dict, Any, List
from dataclasses import dataclass
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
class TaskCardCopy:
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

# Test validation for TaskCard
print("=== Testing TaskCard Validation ===")
try:
    _invalid_task = TaskCardCopy(task_id="", title="Test", description="Test", required_skills=[])
    print("❌ FAILED: Empty task_id should raise ValueError")
except ValueError as e:
    print(f"✅ PASSED: Empty task_id validation - {e}")

try:
    _invalid_task = TaskCardCopy(task_id="123", title="", description="Test", required_skills=[])
    print("❌ FAILED: Empty title should raise ValueError")
except ValueError as e:
    print(f"✅ PASSED: Empty title validation - {e}")

print("✅ TaskCard validation: Complete")