from pydantic import BaseModel
from typing import Optional
class AboutBase(BaseModel):
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None

class AboutCreate(AboutBase):
    pass

class AboutOut(BaseModel):
    id: int
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image_url: str 

    class Config:
        orm_mode = True

class About(AboutBase):
    id: int
    image_path: str

    class Config:
        orm_mode = True

# Card schemalari

class CardBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    description_uz: str
    description_ru: str
    description_en: str

class CardCreate(CardBase):
    pass

class Card(CardBase):  # POST / PUT uchun (bazaga yoziladi)
    id: int
    image_path: str

    class Config:
        orm_mode = True

class CardOut(CardBase):  # GET endpoint uchun (frontendga image_url yuboriladi)
    id: int
    image_url: str

    class Config:
        orm_mode = True



class ProjectTypeBase(BaseModel):
    name_uz: str
    name_ru: str
    name_en: str

class ProjectTypeCreate(ProjectTypeBase):
    pass

class ProjectTypeOut(ProjectTypeBase):
    id: int
    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    description_uz: str
    description_ru: str
    description_en: str
    project_type_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    image_url: Optional[str]
    project_type: Optional[ProjectTypeOut]

    class Config:
        orm_mode = True