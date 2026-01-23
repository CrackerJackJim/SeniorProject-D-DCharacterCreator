from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import auth_router

app = FastAPI()

# -------------------------------------------------
# CORS CONFIGURATION
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# STATIC FILES (HTML, JS, CSS)
# -------------------------------------------------
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# -------------------------------------------------
# ROOT ROUTE → LOGIN PAGE
# -------------------------------------------------
@app.get("/")
def root():
    return FileResponse("assets/login.html")

# -------------------------------------------------
# ROUTERS
# -------------------------------------------------
app.include_router(auth_router.router)

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@app.get("/api/health")
def health():
    return {"status": "ok"}