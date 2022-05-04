import uuid

from sqlalchemy import Column, String, ForeignKey, BigInteger, Integer, Float, DateTime
from sqlalchemy.orm import relationship

from application.dependencies.database import Base
from application.infrastructure.model.base_model import BaseModelMixin
from sqlalchemy.dialects.postgresql import UUID


class Country(BaseModelMixin, Base):
    __tablename__ = 'country'
    #
    # id = Column(
    #     UUID(as_uuid=True),
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     unique=True,
    #     nullable=False,
    #     index=True,
    # )

    name = Column(String(length=120))
    confirmed = Column(Integer)
    recovered = Column(Integer)
    deaths = Column(Integer)
    population = Column(BigInteger)
    sq_km_area = Column(Float)
    life_expectancy = Column(String(length=10))
    elevation_in_meters = Column(String(length=120))
    continent = Column(String(length=120))
    abbreviation = Column(String(length=120))
    location = Column(String(length=120))
    iso = Column(Integer)
    capital_city = Column(String(length=120))
    lat = Column(String(length=120))
    long = Column(String(length=120))
    updated = Column(DateTime)

    regions = relationship('Region', back_populates="country")


class Region(BaseModelMixin, Base):
    __tablename__ = 'region'

    # id = Column(
    #     UUID(as_uuid=True),
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     unique=True,
    #     nullable=False,
    #     index=True,
    # )

    country_id = Column(UUID(as_uuid=True), ForeignKey('country.id'), nullable=True)
    name = Column(String(length=120))
    lat = Column(String(length=120))
    long = Column(String(length=120))
    confirmed = Column(Integer)
    recovered = Column(Integer)
    deaths = Column(Integer)
    updated = Column(DateTime)

    country = relationship('Country', back_populates="regions")

