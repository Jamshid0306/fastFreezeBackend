from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routers import about, service, admin, projects
# oldingi holat (agar mavjud bo'lsa)
from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(about.router)
app.include_router(service.router)
app.include_router(admin.router)
app.include_router(projects.router)
app.mount("/images", StaticFiles(directory="state/images"), name="images")
