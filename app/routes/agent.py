from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.db import supabase
from app.services.agent import run_agent

router = APIRouter()

class AgentRequest(BaseModel):
    project_id: str

@router.post("/run-agent")
def start_agent(req: AgentRequest, background_tasks: BackgroundTasks):
    run = supabase.table("agent_runs").insert({
        "project_id": req.project_id,
        "status": "pending"
    }).execute()

    run_id = run.data[0]["id"]

    background_tasks.add_task(run_agent, req.project_id, run_id)

    return {
        "success": True,
        "run_id": run_id,
        "status": "started"
    }


@router.get("/agent-status/{run_id}")
def get_status(run_id: str):
    data = supabase.table("agent_runs").select("*").eq("id", run_id).execute()
    return {"success": True, "data": data.data}