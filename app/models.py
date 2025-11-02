from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)
    description_uz = Column(String, nullable=False)
    description_ru = Column(String, nullable=False)
    description_en = Column(String, nullable=False)
    image_path = Column(String)

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title_uz = Column(String)
    title_ru = Column(String)
    title_en = Column(String)
    description_uz = Column(String)
    description_ru = Column(String)
    description_en = Column(String)
    image_path = Column(String)
    is_image = Column(Boolean, default=True) 
    video_link = Column(String, nullable=True) 
    
    
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class ProjectType(Base):
    __tablename__ = "project_types"

    id = Column(Integer, primary_key=True, index=True)
    name_uz = Column(String, nullable=False)
    name_ru = Column(String, nullable=False)
    name_en = Column(String, nullable=False)

    projects = relationship("Project", back_populates="project_type")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title_uz = Column(String)
    title_ru = Column(String)
    title_en = Column(String)
    description_uz = Column(String)
    description_ru = Column(String)
    description_en = Column(String)
    image_path = Column(String)
    project_type_id = Column(Integer, ForeignKey("project_types.id"))

    project_type = relationship("ProjectType", back_populates="projects")