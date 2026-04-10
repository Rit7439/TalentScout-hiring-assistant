"""Handle candidate data storage and retrieval with privacy compliance."""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class DataHandler:
    """Manages candidate data with privacy and security measures."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.candidates_file = self.data_dir / "candidates.json"
        self.conversations_file = self.data_dir / "conversations.json"
    
    def save_candidate(self, candidate_data: Dict) -> str:
        """Save candidate information and return candidate ID."""
        candidate_id = self._generate_candidate_id()
        candidate_data["id"] = candidate_id
        candidate_data["created_at"] = datetime.now().isoformat()
        
        candidates = self._load_json(self.candidates_file)
        candidates[candidate_id] = candidate_data
        self._save_json(self.candidates_file, candidates)
        
        return candidate_id
    
    def save_conversation(self, candidate_id: str, messages: List[Dict]) -> None:
        """Save conversation history."""
        conversations = self._load_json(self.conversations_file)
        
        if candidate_id not in conversations:
            conversations[candidate_id] = []
        
        conversations[candidate_id] = {
            "messages": messages,
            "updated_at": datetime.now().isoformat()
        }
        
        self._save_json(self.conversations_file, conversations)
    
    def get_candidate(self, candidate_id: str) -> Optional[Dict]:
        """Retrieve candidate information."""
        candidates = self._load_json(self.candidates_file)
        return candidates.get(candidate_id)
    
    def get_conversation(self, candidate_id: str) -> Optional[List[Dict]]:
        """Retrieve conversation history."""
        conversations = self._load_json(self.conversations_file)
        conv_data = conversations.get(candidate_id)
        return conv_data.get("messages") if conv_data else None
    
    def anonymize_candidate_data(self, candidate_data: Dict) -> Dict:
        """Remove PII from candidate data for analysis."""
        anonymized = candidate_data.copy()
        anonymized.pop("contact", None)
        anonymized.pop("name", None)
        anonymized.pop("location", None)
        return anonymized
    
    def export_candidate_summary(self, candidate_id: str) -> Dict:
        """Export complete candidate summary."""
        candidate = self.get_candidate(candidate_id)
        conversation = self.get_conversation(candidate_id)
        
        if not candidate:
            return {}
        
        return {
            "candidate_id": candidate_id,
            "timestamp": datetime.now().isoformat(),
            "candidate_info": candidate,
            "has_conversation": conversation is not None,
            "message_count": len(conversation) if conversation else 0
        }
    
    def _load_json(self, filepath: Path) -> Dict:
        """Load JSON file with error handling."""
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_json(self, filepath: Path, data: Dict) -> None:
        """Save JSON file with error handling."""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving file {filepath}: {e}")
    
    def _generate_candidate_id(self) -> str:
        """Generate unique candidate ID."""
        return f"cand_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
