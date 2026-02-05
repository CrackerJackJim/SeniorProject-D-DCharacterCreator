from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# ⭐ DEBUG: Show which character_service file Python is actually importing
import services.character_service as cs
print(">>> PYTHON IS IMPORTING character_service FROM:", cs.__file__)

from routers.auth_router import router as auth_router
from routers.characters_router import router as characters_router
from routers.fonts_router import router as fonts_router
from routers import metadata_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/assets",
    StaticFiles(
        directory="Z:/DnD_Final_Project/MySQL/Server side/assets",
        html=True
    ),
    name="assets",
)

# ⭐ All routers mounted cleanly and consistently
app.include_router(auth_router, prefix="/api")
app.include_router(characters_router)  # already has /api/characters prefix inside file
app.include_router(fonts_router, prefix="/api")
app.include_router(metadata_router.router, prefix="/api")

@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/assets/login.html")