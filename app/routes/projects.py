from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.db import supabase

router = APIRouter()

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    goals: Optional[List[str]] = []

@router.post("/projects")
def create_project(project: ProjectCreate):
    data = supabase.table("projects").insert({
        "title": project.title,
        "description": project.description,
        "goals": project.goals
    }).execute()

    return {"success": True, "data": data.data}


@router.get("/projects")
def get_projects():
    data = supabase.table("projects").select("*").execute()
    return {"success": True, "data": data.data}


@router.get("/projects/{project_id}")
def get_project(project_id: str):
    data = supabase.table("projects").select("*").eq("id", project_id).execute()
    return {"success": True, "data": data.data}