import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools.agent_tools import tools_list

load_dotenv()

# Using a functional model because gemma2-9b-it throws model_decommissioned 400 error
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
agent_executor = create_react_agent(llm, tools_list)

def process_chat(user_message: str, current_state: dict):
    sys_msg = f"""You are an AI assistant for a Medical CRM. Your job is to help the user fill out an interaction log via tools.
Current form state: {json.dumps(current_state)}
Decide which tool to call based on the user's input.
CRITICAL INSTRUCTION: NEVER call clear_form unless the user explicitly asks you to reset or clear. Keep the data filled so the user can visually verify it!"""
    
    response = agent_executor.invoke({
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_message}
        ]
    })
    
    actions = []
    for msg in response["messages"]:
        if getattr(msg, "type", "") == "tool" or msg.__class__.__name__ == "ToolMessage":
            try:
                data = json.loads(msg.content)
                if isinstance(data, dict) and "type" in data:
                    actions.append(data)
            except Exception:
                pass
                
    return {
        "reply": response["messages"][-1].content,
        "actions": actions
    }
