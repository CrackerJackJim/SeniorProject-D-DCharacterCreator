import os
import sys

# Ensure the project root ("Server_side") is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import Server_side.services.character_service as cs
print(">>> PYTHON IS IMPORTING character_service FROM:", cs.__file__)

# FIXED: All router imports must use the full package path
from Server_side.routers.auth_router import router as auth_router
from Server_side.routers.characters_router import router as characters_router
from Server_side.routers.fonts_router import router as fonts_router
from Server_side.routers import metadata_router

# FIXED: Level-up router import
from Server_side.routers.level_up_router import subclass_router, levelup_router


app = FastAPI()

@app.middleware("http")
async def no_cache_static(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/assets/"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

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
        directory="Z:/DnD_Final_Project/DnD_Project/Server_side/assets",
        html=True
    ),
    name="assets",
)

# Existing routers
app.include_router(auth_router, prefix="/api")
app.include_router(characters_router)
app.include_router(fonts_router, prefix="/api")
app.include_router(metadata_router.router, prefix="/api")

# New routers
app.include_router(subclass_router)
app.include_router(levelup_router)


@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/assets/login.html")