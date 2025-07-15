
def assemble_prompt(user_profile, summarized_data, isolated_tool, original_query):
    """
    Assembles the final, context-rich prompt for the LLM.
    """
    
    # 1. System Persona
    system_persona = "You are an expert assistant helping employees write high-quality performance reports."

    # 2. User Info (from WRITE)
    user_info = f"- User: {user_profile['name']}, Role: {user_profile['role']}, Tone: {user_profile['preferences']['tone']}"

    # 3. Retrieved & Compressed Data (from COMPRESS)
    retrieved_data = "\\n".join([f"- {item}" for item in summarized_data])

    # 4. Isolated Tool (from ISOLATE)
    # In a real scenario, you might format this as a JSON schema
    isolated_tool_info = f"- Tool: {isolated_tool['name']}()"

    # Assemble the final prompt
    final_prompt = f"""
// System Persona
{system_persona}

// User Info (from WRITE)
{user_info}

// Retrieved & Compressed Data (from SELECT/COMPRESS)
{retrieved_data}

// Isolated Tool (from ISOLATE)
{isolated_tool_info}

// Original User Query
{original_query}
"""
    return final_prompt.strip() 