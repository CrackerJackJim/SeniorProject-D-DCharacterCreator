from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from routers.fonts_router import router as fonts_router

# -----------------------------
# IMPORT ROUTERS
# -----------------------------
from routers.auth_router import router as auth_router
from routers.character_router import router as character_router

# -----------------------------
# CREATE APP
# -----------------------------
app = FastAPI()

# -----------------------------
# CORS CONFIG
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# STATIC FILES (CSS, JS, IMAGES, FONTS)
# -----------------------------
# Mount the assets folder correctly
app.mount("/assets", StaticFiles(directory="Z:/DnD_Final_Project/MySQL/Server side/assets"), name="assets")

# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(auth_router, prefix="/api")
app.include_router(character_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(character_router, prefix="/api")
app.include_router(fonts_router)  # no prefix needed

# -----------------------------
# ROOT REDIRECT TO LOGIN PAGE
# -----------------------------
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/assets/login.html")