from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
import shutil
import os


router = APIRouter(prefix="/projects", tags=["projects"])

UPLOAD_DIR = "state/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ProjectTypes ---
@router.post("/types", response_model=schemas.ProjectTypeOut)
def create_project_type(type_in: schemas.ProjectTypeCreate, db: Session = Depends(get_db)):
    pt = models.ProjectType(**type_in.dict())
    db.add(pt)
    db.commit()
    db.refresh(pt)
    return pt

@router.get("/types", response_model=list[schemas.ProjectTypeOut])
def get_project_types(db: Session = Depends(get_db)):
    return db.query(models.ProjectType).all()

@router.put("/types/{type_id}", response_model=schemas.ProjectTypeOut)
def update_project_type(
    type_id: int,
    type_in: schemas.ProjectTypeCreate,
    db: Session = Depends(get_db)
):
    pt = db.query(models.ProjectType).filter(models.ProjectType.id == type_id).first()
    if not pt:
        raise HTTPException(status_code=404, detail="Project type not found")

    pt.name_uz = type_in.name_uz
    pt.name_ru = type_in.name_ru
    pt.name_en = type_in.name_en

    db.commit()
    db.refresh(pt)
    return pt

@router.delete("/types/{type_id}")
def delete_project_type(type_id: int, db: Session = Depends(get_db)):
    project_type = db.query(models.ProjectType).filter(models.ProjectType.id == type_id).first()
    if not project_type:
        raise HTTPException(status_code=404, detail="Project type not found")

    # Qo‘lda o‘chirish: avval shu turga tegishli loyihalarni o‘chiramiz
    projects = db.query(models.Project).filter(models.Project.project_type_id == type_id).all()
    for project in projects:
        db.delete(project)

    db.delete(project_type)
    db.commit()

    return {"message": "Project type va unga tegishli barcha projectlar o‘chirildi"}

# --- Projects ---
@router.post("/", response_model=schemas.ProjectOut)
async def create_project(
    title_uz: str = Form(...),
    title_ru: str = Form(...),
    title_en: str = Form(...),
    description_uz: str = Form(...),
    description_ru: str = Form(...),
    description_en: str = Form(...),
    project_type_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    project = models.Project(
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        description_uz=description_uz,
        description_ru=description_ru,
        description_en=description_en,
        project_type_id=project_type_id,
        image_path=file_location
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return schemas.ProjectOut(
        id=project.id,
        title_uz=project.title_uz,
        title_ru=project.title_ru,
        title_en=project.title_en,
        description_uz=project.description_uz,
        description_ru=project.description_ru,
        description_en=project.description_en,
        project_type_id=project.project_type_id,
        project_type={
            "id": project.project_type.id,
            "name_uz": project.project_type.name_uz,
            "name_ru": project.project_type.name_ru,
            "name_en": project.project_type.name_en
        } if project.project_type else None,
        image_url=f"/images/{os.path.basename(project.image_path)}"
    )
@router.get("/", response_model=list[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    result = []
    for p in projects:
        result.append({
            "id": p.id,
            "title_uz": p.title_uz,
            "title_ru": p.title_ru,
            "title_en": p.title_en,
            "description_uz": p.description_uz,
            "description_ru": p.description_ru,
            "description_en": p.description_en,
            "project_type_id": p.project_type_id,
            "project_type": {
                "id": p.project_type.id,
                "name_uz": p.project_type.name_uz,
                "name_ru": p.project_type.name_ru,
                "name_en": p.project_type.name_en
            } if p.project_type else None,
            "image_url": f"/images/{os.path.basename(p.image_path)}" if p.image_path else None
        })
    return result

@router.put("/{project_id}", response_model=schemas.ProjectOut)
async def update_project(
    project_id: int,
    title_uz: str = None,
    title_ru: str = None,
    title_en: str = None,
    description_uz: str = None,
    description_ru: str = None,
    description_en: str = None,
    project_type_id: int = None,
    file: UploadFile = None,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if title_uz: project.title_uz = title_uz
    if title_ru: project.title_ru = title_ru
    if title_en: project.title_en = title_en
    if description_uz: project.description_uz = description_uz
    if description_ru: project.description_ru = description_ru
    if description_en: project.description_en = description_en
    if project_type_id: project.project_type_id = project_type_id

    if file:
        if os.path.exists(project.image_path):
            os.remove(project.image_path)
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        project.image_path = file_location

    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if os.path.exists(project.image_path):
        os.remove(project.image_path)
    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully"}
