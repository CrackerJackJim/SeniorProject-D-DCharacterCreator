from fastapi import APIRouter
import os

router = APIRouter()

FONT_DIR = os.path.join("assets", "Fonts")

@router.get("/fonts")
def list_fonts():
    try:
        files = os.listdir(FONT_DIR)
        font_files = [f for f in files if f.lower().endswith((".ttf", ".otf"))]
        return font_files
    except Exception:
        return []