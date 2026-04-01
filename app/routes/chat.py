from fastapi import APIRouter
from pydantic import BaseModel
from app.db import supabase
from app.services.claude import get_ai_response
from app.services.memory import save_memory, get_memory

router = APIRouter()

class ChatRequest(BaseModel):
    project_id: str
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    conv = supabase.table("conversations").insert({
        "project_id": req.project_id
    }).execute()

    conversation_id = conv.data[0]["id"]

    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": "user",
        "content": req.message
    }).execute()

    # memory
    memory = get_memory(req.project_id)

    memory_text = ""
    for m in memory:
        memory_text += f"{m['key']}: {m['value']}\n"

    full_prompt = f"""
    Project memory:
    {memory_text}

    User: {req.message}
    """

    ai_response = get_ai_response(full_prompt)

    if "student" in req.message.lower():
        save_memory(req.project_id, "target_user", "students")

    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": "assistant",
        "content": ai_response
    }).execute()

    return {
        "success": True,
        "conversation_id": conversation_id,
        "response": ai_response
    }