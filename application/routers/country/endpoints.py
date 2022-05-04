from fastapi import APIRouter, Depends

from application.services.country.country import CountryService, CreateUpdateCountryInput
from application.services.region.region import RegionService, CreateUpdateRegionInput

router = APIRouter()


@router.get("/countries")
def get_countries(size: int = None, page: int = 0, cr: CountryService = Depends()):
    items, count, has_more, page = cr.get_countries(size, page)
    return dict(countries=items, count=count, page=page, has_more=has_more)


@router.get("/countries/search")
def search_countries(query_string, size: int = None, page: int = 0, cr: CountryService = Depends()):
    items, count, has_more, page = cr.search_country_by_name(query_string, size, page)
    return dict(countries=items, count=count, page=page, has_more=has_more)


@router.get("/country/{country_id}/regions")
def get_regions(country_id, size: int = None, page: int = 0, rs: RegionService = Depends()):
    items, count, has_more, page = rs.get_regions_in_country(country_id, size, page)
    return dict(regions=items, count=count, page=page, has_more=has_more)


@router.get("/country/{country_id}")
def get_country(country_id: str = '', cr: CountryService = Depends()):
    return cr.get_company(country_id)


@router.get("/country/{country_id}/region/{region_id}")
def get_region(country_id, region_id, rs: RegionService = Depends()):
    return rs.get_region_in_country(country_id, region_id)


@router.post("/country")
def create_country(request_data: CreateUpdateCountryInput, sv: CountryService = Depends()):
    return sv.create_new_country(request_data)


@router.post("/country/{country_id}/region")
def create_region(request_data: CreateUpdateRegionInput, country_id: str, rs: RegionService = Depends()):
    return rs.create_new_region(country_id, request_data)


@router.delete("/country/{country_id}")
def delete_country(country_id: str, sv: CountryService = Depends()):
    return sv.delete_country(country_id)


@router.delete("/country/{country_id}/region/{region_id}")
def delete_region(country_id: str, region_id: str, rs: RegionService = Depends()):
    return rs.delete_region(country_id, region_id)


@router.put("/country/{country_id}")
def update_country_object(country_id, country_data: CreateUpdateCountryInput, sv: CountryService = Depends()):
    return sv.update_country(country_id, country_data)


@router.put("/country/{country_id}/region/{region_id}")
def update_region_object(country_id, region_id, region_data: CreateUpdateRegionInput, rs: RegionService = Depends()):
    return rs.update_region(country_id, region_id, region_data)
