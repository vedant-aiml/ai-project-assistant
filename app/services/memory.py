from app.db import supabase

def save_memory(project_id: str, key: str, value: str):
    supabase.table("memory").insert({
        "project_id": project_id,
        "key": key,
        "value": value
    }).execute()


def get_memory(project_id: str):
    data = supabase.table("memory").select("*").eq("project_id", project_id).execute()
    return data.data