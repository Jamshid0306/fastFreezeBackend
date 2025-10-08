from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .. import models, schemas, database
import shutil
import os
from fastapi import Form

router = APIRouter(prefix="/about", tags=["about"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "state/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.About)
async def create_about(
    description_uz: str,
    description_ru: str,
    description_en: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    about = models.About(
        description_uz=description_uz,
        description_ru=description_ru,
        description_en=description_en,
        image_path=file_location 
    )
    db.add(about)
    db.commit()
    db.refresh(about)
    return about


@router.get("/", response_model=list[schemas.AboutOut])
def get_about(db: Session = Depends(get_db)):
    about_list = db.query(models.About).all()
    result = []
    for a in about_list:
        result.append({
            "id": a.id,
            "description_uz": a.description_uz,
            "description_ru": a.description_ru,
            "description_en": a.description_en,
            "image_url": f"/images/{os.path.basename(a.image_path)}"
        })
    return result


@router.put("/{about_id}", response_model=schemas.About)
async def update_about(
    about_id: int,
    description_uz: str = Form(None),
    description_ru: str = Form(None),
    description_en: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    about = db.query(models.About).filter(models.About.id == about_id).first()
    if not about:
        raise HTTPException(status_code=404, detail="About not found")

    if description_uz is not None:
        about.description_uz = description_uz
    if description_ru is not None:
        about.description_ru = description_ru
    if description_en is not None:
        about.description_en = description_en

    if file:
        if os.path.exists(about.image_path):
            os.remove(about.image_path)
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        about.image_path = file_location

    db.commit()
    db.refresh(about)
    return about
@router.delete("/{about_id}")
def delete_about(about_id: int, db: Session = Depends(get_db)):
    about = db.query(models.About).filter(models.About.id == about_id).first()
    if not about:
        raise HTTPException(status_code=404, detail="About not found")
    
    # rasm faylini o'chirish
    if os.path.exists(about.image_path):
        os.remove(about.image_path)
    
    db.delete(about)
    db.commit()
    return {"detail": "About block deleted successfully"}
