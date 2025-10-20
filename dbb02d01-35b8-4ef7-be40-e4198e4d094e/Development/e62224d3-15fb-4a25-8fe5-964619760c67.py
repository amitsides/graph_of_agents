from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Re-define CardBuilder dependencies for testing
@dataclass
class EntityCard:
    """Base class for entity cards in the system."""
    card_id: str
    card_type: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary."""
        _result = asdict(self)
        _result['created_at'] = self.created_at.isoformat()
        _result['updated_at'] = self.updated_at.isoformat()
        return _result

class CardBuilder:
    """Service for creating and managing entity cards (agents, tasks, etc.)."""
    
    def __init__(self):
        self._cards: Dict[str, EntityCard] = {}
    
    def create_agent_card(self, agent_id: str, name: str, description: str,
                         skills: List[Any], version: str = "1.0.0",
                         metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create an agent card with validation."""
        if not agent_id or not isinstance(agent_id, str):
            raise ValueError("Agent ID must be a non-empty string")
        if not name or not isinstance(name, str):
            raise ValueError("Agent name must be a non-empty string")
        if not description or not isinstance(description, str):
            raise ValueError("Agent description must be a non-empty string")
        if not isinstance(skills, list):
            raise ValueError("Skills must be a list")
        
        _card_id = f"card_{agent_id}"
        _now = datetime.now()
        
        _card_data = {
            "card_id": _card_id,
            "card_type": "agent",
            "agent_id": agent_id,
            "name": name,
            "description": description,
            "skills": skills,
            "version": version,
            "metadata": metadata or {},
            "created_at": _now,
            "updated_at": _now
        }
        
        _card = EntityCard(
            card_id=_card_id,
            card_type="agent",
            created_at=_now,
            updated_at=_now,
            metadata=_card_data
        )
        
        self._cards[_card_id] = _card
        return _card_data
    
    def create_task_card(self, task_id: str, title: str, description: str,
                        required_skills: List[str], status: str = "pending",
                        priority: str = "medium", assigned_agent_id: Optional[str] = None,
                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a task card with validation."""
        if not task_id or not isinstance(task_id, str):
            raise ValueError("Task ID must be a non-empty string")
        if not title or not isinstance(title, str):
            raise ValueError("Task title must be a non-empty string")
        if not description or not isinstance(description, str):
            raise ValueError("Task description must be a non-empty string")
        if not isinstance(required_skills, list):
            raise ValueError("Required skills must be a list")
        
        _card_id = f"card_{task_id}"
        _now = datetime.now()
        
        _card_data = {
            "card_id": _card_id,
            "card_type": "task",
            "task_id": task_id,
            "title": title,
            "description": description,
            "required_skills": required_skills,
            "status": status,
            "priority": priority,
            "assigned_agent_id": assigned_agent_id,
            "context": context or {},
            "created_at": _now,
            "updated_at": _now
        }
        
        _card = EntityCard(
            card_id=_card_id,
            card_type="task",
            created_at=_now,
            updated_at=_now,
            metadata=_card_data
        )
        
        self._cards[_card_id] = _card
        return _card_data
    
    def create_skill_card(self, skill_name: str, description: str,
                         parameters: Optional[Dict[str, Any]] = None,
                         examples: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a skill card with validation."""
        if not skill_name or not isinstance(skill_name, str):
            raise ValueError("Skill name must be a non-empty string")
        if not description or not isinstance(description, str):
            raise ValueError("Skill description must be a non-empty string")
        
        _card_id = f"card_skill_{skill_name}"
        _now = datetime.now()
        
        _card_data = {
            "card_id": _card_id,
            "card_type": "skill",
            "name": skill_name,
            "description": description,
            "parameters": parameters or {},
            "examples": examples or [],
            "created_at": _now,
            "updated_at": _now
        }
        
        _card = EntityCard(
            card_id=_card_id,
            card_type="skill",
            created_at=_now,
            updated_at=_now,
            metadata=_card_data
        )
        
        self._cards[_card_id] = _card
        return _card_data
    
    def get_card(self, card_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a card by its ID."""
        _card = self._cards.get(card_id)
        if _card and _card.metadata:
            return _card.metadata
        return None
    
    def update_card(self, card_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing card with new data."""
        _card = self._cards.get(card_id)
        if not _card:
            raise ValueError(f"Card {card_id} not found")
        
        if _card.metadata:
            _card.metadata.update(updates)
            _card.metadata['updated_at'] = datetime.now()
            _card.updated_at = datetime.now()
            return _card.metadata
        
        raise ValueError(f"Card {card_id} has no metadata to update")
    
    def link_cards(self, source_card_id: str, target_card_id: str, 
                   relationship_type: str) -> Dict[str, Any]:
        """Create a relationship link between two cards."""
        _source = self._cards.get(source_card_id)
        _target = self._cards.get(target_card_id)
        
        if not _source:
            raise ValueError(f"Source card {source_card_id} not found")
        if not _target:
            raise ValueError(f"Target card {target_card_id} not found")
        
        _link = {
            "source_card_id": source_card_id,
            "target_card_id": target_card_id,
            "relationship_type": relationship_type,
            "created_at": datetime.now().isoformat()
        }
        
        return _link
    
    def validate_card(self, card_id: str) -> tuple[bool, List[str]]:
        """Validate a card's structure and required fields."""
        _card = self._cards.get(card_id)
        if not _card:
            return False, [f"Card {card_id} not found"]
        
        _errors = []
        
        if not _card.metadata:
            _errors.append("Card has no metadata")
            return False, _errors
        
        _metadata = _card.metadata
        _card_type = _metadata.get('card_type')
        
        # Type-specific validation
        if _card_type == 'agent':
            if 'agent_id' not in _metadata or not _metadata['agent_id']:
                _errors.append("Agent card missing agent_id")
            if 'name' not in _metadata or not _metadata['name']:
                _errors.append("Agent card missing name")
            if 'skills' not in _metadata or not isinstance(_metadata['skills'], list):
                _errors.append("Agent card missing or invalid skills")
        
        elif _card_type == 'task':
            if 'task_id' not in _metadata or not _metadata['task_id']:
                _errors.append("Task card missing task_id")
            if 'title' not in _metadata or not _metadata['title']:
                _errors.append("Task card missing title")
            if 'required_skills' not in _metadata or not isinstance(_metadata['required_skills'], list):
                _errors.append("Task card missing or invalid required_skills")
        
        elif _card_type == 'skill':
            if 'name' not in _metadata or not _metadata['name']:
                _errors.append("Skill card missing name")
        
        return len(_errors) == 0, _errors
    
    def list_cards_by_type(self, card_type: str) -> List[Dict[str, Any]]:
        """Get all cards of a specific type."""
        _result = []
        for _card in self._cards.values():
            if _card.metadata and _card.metadata.get('card_type') == card_type:
                _result.append(_card.metadata)
        return _result

# Test CardBuilder service
test_card_builder = CardBuilder()

# Test 1: Create agent card
print("Test 1: Create agent card")
test_agent_card = test_card_builder.create_agent_card(
    agent_id="agent_001",
    name="Data Analyst",
    description="Analyzes data",
    skills=["data_analysis", "visualization"]
)
print(f"  ✓ Created: {test_agent_card['card_id']}")

# Test 2: Create task card
print("\nTest 2: Create task card")
test_task_card = test_card_builder.create_task_card(
    task_id="task_001",
    title="Analyze Q4 Data",
    description="Analyze quarterly data",
    required_skills=["data_analysis"],
    priority="high"
)
print(f"  ✓ Created: {test_task_card['card_id']}")

# Test 3: Create skill card
print("\nTest 3: Create skill card")
test_skill_card = test_card_builder.create_skill_card(
    skill_name="data_analysis",
    description="Analyze datasets"
)
print(f"  ✓ Created: {test_skill_card['card_id']}")

# Test 4: Validate cards
print("\nTest 4: Validate cards")
agent_valid, agent_errors = test_card_builder.validate_card("card_agent_001")
print(f"  Agent card valid: {agent_valid}")
task_valid, task_errors = test_card_builder.validate_card("card_task_001")
print(f"  Task card valid: {task_valid}")

# Test 5: Link cards
print("\nTest 5: Link cards")
test_link = test_card_builder.link_cards(
    "card_agent_001",
    "card_task_001",
    "assigned_to"
)
print(f"  ✓ Linked: {test_link['relationship_type']}")

print("\n✓ CardBuilder tests completed")