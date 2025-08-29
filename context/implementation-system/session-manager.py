#!/usr/bin/env python3

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set


class SessionManager:
    def __init__(self, base_path: str = None):
        if base_path is None:
            self.base_path = Path(__file__).parent / "sessions"
        else:
            self.base_path = Path(base_path)
        
        self.session_structure = {
            "1-requirement-analysis": [
                "user-requirements.md",
                "knowledge-requirements.md", 
                "knowledge-extraction.md"
            ],
            "2-specification-design": [
                "architecture-specification.md",
                "interface-specification.md",
                "behavior-specification.md"
            ],
            "3-implementation-preparation": [
                "coordination-plan.md",
                "knowledge-packages/"
            ],
            "4-code-generation": [
                "handoffs/"
            ]
        }
    
    def initialize_session(self, session_name: str) -> bool:
        session_path = self.base_path / session_name
        
        if session_path.exists():
            print(f"Session '{session_name}' already exists")
            return False
        
        try:
            session_path.mkdir(parents=True, exist_ok=True)
            
            for stage, files in self.session_structure.items():
                stage_path = session_path / stage
                stage_path.mkdir(exist_ok=True)
                
                for file_item in files:
                    if file_item.endswith("/"):
                        (stage_path / file_item.rstrip("/")).mkdir(exist_ok=True)
                    else:
                        file_path = stage_path / file_item
                        file_path.touch()
            
            state_file = session_path / ".session-state.json"
            initial_state = {
                "session_name": session_name,
                "created": datetime.now().isoformat(),
                "current_stage": 1,
                "stages": {
                    "1": {"status": "pending", "files": {}},
                    "2": {"status": "pending", "files": {}},
                    "3": {"status": "pending", "files": {}},
                    "4": {"status": "pending", "files": {}}
                }
            }
            
            with open(state_file, 'w') as f:
                json.dump(initial_state, f, indent=2)
            
            print(f"Session '{session_name}' initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing session: {e}")
            return False
    
    def validate_template(self, file_path: Path) -> Dict[str, any]:
        if not file_path.exists():
            return {"valid": False, "error": "File does not exist"}
        
        if file_path.stat().st_size == 0:
            return {"valid": False, "error": "File is empty"}
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            required_sections = self._get_required_sections(file_path.name)
            missing_sections = []
            
            for section in required_sections:
                if f"## {section}" not in content and f"# {section}" not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                return {
                    "valid": False, 
                    "error": f"Missing required sections: {', '.join(missing_sections)}"
                }
            
            return {"valid": True, "sections_found": len(required_sections)}
            
        except Exception as e:
            return {"valid": False, "error": f"Error reading file: {e}"}
    
    def _get_required_sections(self, filename: str) -> List[str]:
        section_map = {
            "user-requirements.md": ["Requirements", "Acceptance Criteria"],
            "knowledge-requirements.md": ["Knowledge Categories", "Risk Assessment"],
            "knowledge-extraction.md": ["Extracted Knowledge", "Sources"],
            "architecture-specification.md": ["System Architecture", "Components"],
            "interface-specification.md": ["Interfaces", "Data Schemas"],
            "behavior-specification.md": ["Behaviors", "Test Cases"],
            "coordination-plan.md": ["Implementation Units", "Coordination Strategy"]
        }
        return section_map.get(filename, [])
    
    def get_session_state(self, session_name: str) -> Optional[Dict]:
        session_path = self.base_path / session_name
        state_file = session_path / ".session-state.json"
        
        if not state_file.exists():
            return None
        
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading session state: {e}")
            return None
    
    def update_session_state(self, session_name: str, stage: int, file_name: str, status: str) -> bool:
        session_path = self.base_path / session_name
        state_file = session_path / ".session-state.json"
        
        try:
            state = self.get_session_state(session_name)
            if state is None:
                return False
            
            stage_key = str(stage)
            if stage_key not in state["stages"]:
                return False
            
            state["stages"][stage_key]["files"][file_name] = {
                "status": status,
                "updated": datetime.now().isoformat()
            }
            
            all_complete = all(
                f.get("status") == "complete" 
                for f in state["stages"][stage_key]["files"].values()
            )
            
            if all_complete and len(state["stages"][stage_key]["files"]) > 0:
                state["stages"][stage_key]["status"] = "complete"
                if stage < 4:
                    state["current_stage"] = stage + 1
            
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error updating session state: {e}")
            return False
    
    def list_sessions(self) -> List[str]:
        if not self.base_path.exists():
            return []
        
        sessions = []
        for item in self.base_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                sessions.append(item.name)
        
        return sorted(sessions)
    
    def validate_session_structure(self, session_name: str) -> Dict[str, any]:
        session_path = self.base_path / session_name
        
        if not session_path.exists():
            return {"valid": False, "error": "Session does not exist"}
        
        validation_results = {
            "valid": True,
            "stages": {},
            "missing_files": [],
            "missing_directories": []
        }
        
        for stage, expected_files in self.session_structure.items():
            stage_path = session_path / stage
            stage_results = {"exists": stage_path.exists(), "files": {}}
            
            if not stage_path.exists():
                validation_results["missing_directories"].append(stage)
                validation_results["valid"] = False
                continue
            
            for file_item in expected_files:
                if file_item.endswith("/"):
                    dir_path = stage_path / file_item.rstrip("/")
                    if not dir_path.exists():
                        validation_results["missing_directories"].append(f"{stage}/{file_item}")
                        validation_results["valid"] = False
                else:
                    file_path = stage_path / file_item
                    file_exists = file_path.exists()
                    stage_results["files"][file_item] = file_exists
                    
                    if not file_exists:
                        validation_results["missing_files"].append(f"{stage}/{file_item}")
                        validation_results["valid"] = False
            
            validation_results["stages"][stage] = stage_results
        
        return validation_results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Session Management Utility")
    parser.add_argument("command", choices=["init", "validate", "status", "list"])
    parser.add_argument("--session", "-s", help="Session name")
    parser.add_argument("--stage", type=int, help="Stage number (1-4)")
    parser.add_argument("--file", help="File name")
    parser.add_argument("--status", help="File status (pending, in_progress, complete)")
    
    args = parser.parse_args()
    
    manager = SessionManager()
    
    if args.command == "init":
        if not args.session:
            print("Session name required for init command")
            return
        manager.initialize_session(args.session)
    
    elif args.command == "validate":
        if not args.session:
            print("Session name required for validate command")
            return
        
        result = manager.validate_session_structure(args.session)
        print(f"Session '{args.session}' validation:")
        print(f"Valid: {result['valid']}")
        
        if result['missing_files']:
            print(f"Missing files: {', '.join(result['missing_files'])}")
        if result['missing_directories']:
            print(f"Missing directories: {', '.join(result['missing_directories'])}")
    
    elif args.command == "status":
        if not args.session:
            print("Session name required for status command")
            return
        
        if args.stage and args.file and args.status:
            success = manager.update_session_state(args.session, args.stage, args.file, args.status)
            print(f"Status update: {'Success' if success else 'Failed'}")
        else:
            state = manager.get_session_state(args.session)
            if state:
                print(f"Session: {state['session_name']}")
                print(f"Current Stage: {state['current_stage']}")
                for stage, info in state['stages'].items():
                    print(f"  Stage {stage}: {info['status']}")
            else:
                print("Session state not found")
    
    elif args.command == "list":
        sessions = manager.list_sessions()
        if sessions:
            print("Available sessions:")
            for session in sessions:
                print(f"  - {session}")
        else:
            print("No sessions found")


if __name__ == "__main__":
    main()