from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

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

print("CardBuilder service created successfully")
print("  - Base class: EntityCard")
print("  - Service: CardBuilder")
print("  - Card types: agent, task, skill")
print("  - Key methods: create_*_card(), get_card(), update_card(), link_cards()")
print("  - Validation: validate_card() with type-specific checks")