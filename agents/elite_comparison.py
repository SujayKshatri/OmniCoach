from antigravity import Agent, hooks
import json
import math

class EliteComparisonAgent:
    def __init__(self, archetype_matrix_path: str):
        with open(archetype_matrix_path, 'r') as f:
            self.matrix = json.load(f)

    def calculate_deltas(self, sport: str, archetype_id: str, user_telemetry: dict) -> dict:
        """
        Pure deterministic function to calculate structural deviations.
        No LLM calls here—pure, raw speed.
        """
        target_archetype = self.matrix["sports"].get(sport, {}).get("archetypes", {}).get(archetype_id, {})
        if not target_archetype:
            raise ValueError(f"Archetype {archetype_id} not found for sport {sport}")
            
        metrics = target_archetype["metrics"]
        delta_report = {}

        for metric_name, user_value in user_telemetry.items():
            if metric_name in metrics:
                target = metrics[metric_name]["target_deg"]
                tolerance = metrics[metric_name]["tolerance"]
                
                # Structural variance computation
                variance = user_value - target
                outside_tolerance = abs(variance) > tolerance
                
                delta_report[metric_name] = {
                    "user_value": user_value,
                    "target_value": target,
                    "variance": round(variance, 2),
                    "outside_tolerance": outside_tolerance,
                    "severity": "CRITICAL" if abs(variance) > (tolerance * 2) else "WARNING" if outside_tolerance else "OPTIMAL"
                }
                
        return delta_report

    @hooks.post_tool_call
    async def evaluate_deltas_with_agent(self, delta_report: dict, config: dict):
        """
        Antigravity Stateful Context Call.
        Feeds the calculated deltas into the agent to understand mechanical implications.
        """
        # Filter down to only anomalous metrics to save prompt tokens
        anomalies = {k: v for k, v in delta_report.items() if v["outside_tolerance"]}
        
        # Open the stateful SDK context manager for the sub-agent
        async with Agent(config) as agent:
            prompt = f"""
            Analyze these biomechanical anomalies relative to the pro baseline:
            {json.dumps(anomalies, indent=2)}
            
            Synthesize the mechanical consequence. (e.g., 'An excessive knee extension reduces power transfer').
            Keep it strictly technical and brief.
            """
            response = await agent.process(prompt)
            return response
