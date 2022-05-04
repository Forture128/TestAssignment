from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from application.dependencies.database import get_db
from application.infrastructure.base_repository.base_repository import BaseRepo
from application.infrastructure.model.country import Region


class RegionRepository(BaseRepo):
    model = Region

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_regions(self, country_id: str = None, size: int = None, page: int = 0):
        return self.paginate(self.query(Region.country_id == country_id), page=page, size=size)

    def get_region(self, country_id, region_id):
        return self.query(Region.country_id == country_id, Region.id == region_id).first()

    def create(self, country_id: str, region_data: Region):
        region = self.query(Region.name == region_data.name, Region.id == country_id).one_or_none()
        if region:
            raise HTTPException(status_code=400, detail=f"Region {region_data.name} already exist")
        return self.add(region_data)

    def update_region(self, country_id: str, region_id: str, region_data: Region):
        update_region_in_country = self.query(Region.country_id == country_id, Region.id == region_id)
        if update_region_in_country is None:
            raise HTTPException(status_code=400,
                                detail=f"Cannot find country with id : {country_id} and region with : {region_id}")
        update_company = self.update(region_id, region_data)
        return update_company

    def delete_region(self, country_id, region_id):
        region_in_country = self.query(Region.country_id == country_id, Region.id == region_id)
        if not region_in_country:
            raise HTTPException(status_code=400,
                                detail=f"Cannot find country with id : {country_id} and region with : {region_id}")
        self.delete(region_id)
        return True
