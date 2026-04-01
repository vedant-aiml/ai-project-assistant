from fastapi import APIRouter
from pydantic import BaseModel
from app.db import supabase
from app.services.image import generate_image
from app.services.gemini import analyze_image

router = APIRouter()

class ImageRequest(BaseModel):
    project_id: str
    prompt: str

@router.post("/generate-image")
def create_image(req: ImageRequest):
    image_url = generate_image(req.prompt)

    supabase.table("images").insert({
        "project_id": req.project_id,
        "url": image_url,
        "prompt": req.prompt
    }).execute()

    return {
        "success": True,
        "image_url": image_url
    }


@router.get("/analyze-image/{image_id}")
def analyze_image_api(image_id: str):
    data = supabase.table("images").select("*").eq("id", image_id).execute()

    if not data.data:
        return {"success": False, "error": "Image not found"}

    image_url = data.data[0]["url"]

    result = analyze_image(image_url)

    return {
        "success": True,
        "analysis": result
    }