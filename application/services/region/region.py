from typing import Optional

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from application.dependencies.database import get_db
from application.infrastructure.base_repository.region_repository import RegionRepository
from application.infrastructure.model.country import Region
from application.services.base.base_input import PaginatedPage


class SearchCountry(PaginatedPage):
    search: Optional[str] = None
    is_deleted: Optional[bool] = False


class CreateUpdateRegionInput(BaseModel):
    name: Optional[str] = None
    confirmed: Optional[int] = None
    recovered: Optional[int] = None
    deaths: Optional[int] = None
    lat: Optional[str] = None
    long: Optional[str] = None


class RegionService:

    def __init__(self,
                 db: Session = Depends(get_db),
                 rr: RegionRepository = Depends()
                 ):
        self.db = db
        self.rr = rr

    def create_new_region(self, country_id, request_data: CreateUpdateRegionInput):
        region_data = Region(**request_data.dict())
        region_data.country_id = country_id
        data = self.rr.create(country_id, region_data)
        return self.rr.get_by_id(data.id)

    def update_region(self, country_id, region_id, request_data: CreateUpdateRegionInput):
        data = self.rr.update_region(country_id, region_id, Region(**request_data.dict()))
        return self.rr.get_by_id(data.id) if data else None

    def delete_region(self, country_id, region_id):
        return self.rr.delete_region(country_id, region_id)

    def get_regions_in_country(self, country_id: str = None, size: int = None, page: int = 0):
        count, items = self.rr.get_regions(country_id, size, page)
        has_more = count > (page + 1) * size if size is not None else False
        page = min(page, count / size) if size is not None else 0
        return items, count, has_more, page

    def get_region_in_country(self, country_id, region_id):
        return self.rr.get_region(country_id, region_id)
