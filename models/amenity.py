#!/usr/bin/python
""" holds class Amenity"""
from os import getenv

import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    """Representation of Amenity"""

    if models.storage_t == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
