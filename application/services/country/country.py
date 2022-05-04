from typing import Optional

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from application.dependencies.database import get_db
from application.infrastructure.base_repository.country_repository import CountryRepository
from application.infrastructure.model.country import Country


class CreateUpdateCountryInput(BaseModel):
    name: Optional[str] = None
    confirmed: Optional[int] = None
    recovered: Optional[int] = None
    deaths: Optional[int] = None
    population: Optional[int] = None
    sq_km_area: Optional[float] = None
    life_expectancy: Optional[str] = None
    elevation_in_meters: Optional[str] = None
    continent: Optional[str] = None
    abbreviation: Optional[str] = None
    location: Optional[str] = None
    iso: Optional[int] = None
    capital_city: Optional[str] = None
    lat: Optional[str] = None
    long: Optional[str] = None


class CountryService:

    def __init__(self,
                 db: Session = Depends(get_db),
                 cr: CountryRepository = Depends(),
                 ):
        self.db = db
        self.cr = cr

    def get_countries(self, size: int = None, page: int = 0):
        count, items = self.cr.get_all(size=size, page=page)
        has_more = count > (page + 1) * size if size is not None else False
        page = min(page, count / size) if size is not None else 0
        return items, count, has_more, page

    def get_company(self, country_id: str):
        return self.cr.get_by_id(country_id)

    def create_new_country(self, request_data: CreateUpdateCountryInput):
        data = self.cr.create(Country(**request_data.dict()))
        return data

    def update_country(self, country_id: str, request_data):
        data = self.cr.update_country(country_id, Country(**request_data.dict()))
        return self.cr.get_by_id(data.id) if data else None

    def delete_country(self, country_id):
        return self.cr.delete_country_by_id(country_id)

    def search_country_by_name(self, query_string, size: int = None, page: int = 0):
        count, items = self.cr.search_country(query_string)
        has_more = count > (page + 1) * size if size is not None else False
        page = min(page, count / size) if size is not None else 0
        return items, count, has_more, page
