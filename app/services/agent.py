from app.db import supabase
from app.services.claude import get_ai_response

def run_agent(project_id: str, run_id: str):
    try:
        # update status → running
        supabase.table("agent_runs").update({
            "status": "running"
        }).eq("id", run_id).execute()

        # 🔍 fetch data
        project = supabase.table("projects").select("*").eq("id", project_id).execute().data
        messages = supabase.table("messages").select("*").execute().data
        memory = supabase.table("memory").select("*").eq("project_id", project_id).execute().data

        # 🧠 combine data
        prompt = f"""
        Analyze this project and summarize:

        Project:
        {project}

        Messages:
        {messages}

        Memory:
        {memory}

        Give structured output:
        - summary
        - target users
        - key features
        """

        # 🤖 AI
        result = get_ai_response(prompt)

        # save result
        supabase.table("agent_runs").update({
            "status": "completed",
            "result": result
        }).eq("id", run_id).execute()

    except Exception as e:
        supabase.table("agent_runs").update({
            "status": "failed",
            "result": str(e)
        }).eq("id", run_id).execute()