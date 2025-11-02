from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
import os, shutil

router = APIRouter(prefix="/cards", tags=["cards"])

UPLOAD_DIR = "state/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_cards(db: Session = Depends(get_db)):
    cards = db.query(models.Card).all()
    result = []
    for c in cards:
        result.append({
            "id": c.id,
            "title_uz": c.title_uz,
            "title_ru": c.title_ru,
            "title_en": c.title_en,
            "description_uz": c.description_uz,
            "description_ru": c.description_ru,
            "description_en": c.description_en,
            "is_image": c.is_image,
            "video_link": c.video_link,
            "image_url": f"/images/{os.path.basename(c.image_path)}" if c.image_path else None
        })
    return result


@router.post("/")
async def create_card(
    title_uz: str = Form(...),
    title_ru: str = Form(...),
    title_en: str = Form(...),
    description_uz: str = Form(...),
    description_ru: str = Form(...),
    description_en: str = Form(...),
    is_image: bool = Form(True),
    video_link: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_card = models.Card(
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        description_uz=description_uz,
        description_ru=description_ru,
        description_en=description_en,
        is_image=is_image,
        video_link=video_link,
        image_path=file_location
    )

    db.add(new_card)
    db.commit()
    db.refresh(new_card)

    return {"message": "Service added successfully"}


@router.put("/{card_id}")
async def update_card(
    card_id: int,
    title_uz: str = Form(...),
    title_ru: str = Form(...),
    title_en: str = Form(...),
    description_uz: str = Form(...),
    description_ru: str = Form(...),
    description_en: str = Form(...),
    is_image: bool = Form(True),
    video_link: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    if file:
        if card.image_path and os.path.exists(card.image_path):
            os.remove(card.image_path)
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        card.image_path = file_location

    card.title_uz = title_uz
    card.title_ru = title_ru
    card.title_en = title_en
    card.is_image = is_image
    card.video_link = video_link
    card.description_uz = description_uz
    card.description_ru = description_ru
    card.description_en = description_en

    db.commit()
    db.refresh(card)
    return {"message": "Service updated successfully"}


@router.delete("/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    if card.image_path and os.path.exists(card.image_path):
        os.remove(card.image_path)

    db.delete(card)
    db.commit()
    return {"message": "Service deleted successfully"}
