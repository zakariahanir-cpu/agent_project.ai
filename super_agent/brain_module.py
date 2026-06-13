import json
import os
from datetime import datetime

class BrainModule:
    def __init__(self, memory_file="logs/memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"history": [], "knowledge": {}}
        return {"history": [], "knowledge": {}}

    def save_memory(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2)

    def record_event(self, event_type, details):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details
        }
        self.memory["history"].append(event)
        # Keep memory manageable (last 50 events)
        if len(self.memory["history"]) > 50:
            self.memory["history"] = self.memory["history"][-50:]
        self.save_memory()

    def get_context_for_grok(self):
        # Summarize recent history for Grok
        recent_history = self.memory["history"][-10:]
        context = "Recent History of Decisions and Results:\n"
        for event in recent_history:
            context += f"- [{event['timestamp']}] {event['type']}: {json.dumps(event['details'])[:200]}...\n"
        return context

    def plan_task(self, grok, goal, environment_state):
        system_prompt = f"""
        You are the Brain of a Super AI Agent. Your goal is to plan complex tasks.
        Context from Memory:
        {self.get_context_for_grok()}
        
        Current Environment State:
        {environment_state}
        
        Goal: {goal}
        
        Analyze the goal, reason about the best approach, and return a detailed plan in JSON:
        {{
            "reasoning": "Your step-by-step thinking process",
            "steps": [
                {{"action": "write/delete/test/cmd", "path": "file_path", "content": "content", "reason": "why"}}
            ],
            "expected_outcome": "What success looks like"
        }}
        """
        response = grok.chat(system_prompt, "Generate a plan for the goal.")
        return self._parse_json_response(response)

    def _parse_json_response(self, response):
        try:
            json_str = response.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            return json.loads(json_str)
        except:
            return {"error": "Failed to parse JSON", "raw": response}
