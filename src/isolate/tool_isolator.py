
def get_all_tool_schemas():
    """
    Returns a list of all available tool schemas for the agent.
    In a real application, this would be a more extensive library of tools.
    """
    return [
        {
            "name": "get_direct_reports_feedback",
            "description": "Get feedback from Sarah's direct reports.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to ask for feedback on."
                    }
                },
                "required": ["topic"]
            }
        },
        {
            "name": "schedule_meeting",
            "description": "Schedule a meeting with a colleague.",
            "parameters": {
                "type": "object",
                "properties": {
                    "person": {"type": "string"},
                    "time": {"type": "string"}
                },
                "required": ["person", "time"]
            }
        },
        # ... 48 other mock tools
    ]

def get_isolated_tool_schema(tool_name="get_direct_reports_feedback"):
    """
    Isolates and returns the schema for a specific tool.
    """
    all_tools = get_all_tool_schemas()
    for tool in all_tools:
        if tool["name"] == tool_name:
            return tool
    return None 