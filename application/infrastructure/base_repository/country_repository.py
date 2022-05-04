from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from application.dependencies.database import get_db
from application.infrastructure.base_repository.base_repository import BaseRepo
from application.infrastructure.model.country import Country, Region


class CountryRepository(BaseRepo):
    model = Country

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, size: int = None, page: int = 0):
        return self.paginate(self.db.query(Country), page=page, size=size)

    def create(self, country_data: Country):
        country = self.query(Country.name == country_data.name).one_or_none()
        if country:
            raise HTTPException(status_code=400, detail=f"Country {country_data.name} already exist")
        return self.add(country_data)

    def update_country(self, country_id: str, country_data: Country):
        update_country = self.query(Country.id == country_id)
        if update_country is None:
            raise HTTPException(status_code=400, detail=f"Cannot find country with id : {country_id}")
        update_company = self.update(country_id, country_data)
        return update_company

    def delete_country_by_id(self, id):
        country = self.query(Country.id == id).one_or_none()
        if not country:
            HTTPException(status_code=400, detail=f"Cannot find country with id: {id}")
        self.delete(id)
        return True

    def search_country(self, query_string, size: int = None, page: int = 0):
        return self.paginate(self.query(Country.name.contains(query_string)), page=page, size=size)

    # def with_region(self, query: Query):
    #     query = query.outerjoin(
    #         Region,
    #         and_(Country.id == Region.country_id, Region.is_deleted == False)
    #     )
    #     query = query.options(contains_eager(Country.regions))
    #     return query.populate_existing()
