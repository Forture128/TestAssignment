import datetime
import json
import uuid

from sqlalchemy.orm import Session

from application.dependencies.database import SessionLocal

from application.infrastructure.model.country import Country, Region


def insert_data():
    print('Start insert data')
    db: Session = SessionLocal()
    data_file = "covid-stats.json"
    f = open(data_file)
    data_as_dict: dict = json.load(f)

    for co, value in data_as_dict.items():
        country_exist = db.query(Country).filter(Country.name == co).first()
        if country_exist:
            print(f' Country alr exist {co}')
            continue
        list_regions = value.keys()
        all_data = data_as_dict[co]['All']

        country = Country()
        country.id = uuid.uuid4()
        country.name = co
        country.confirmed = all_data['confirmed']
        country.recovered = all_data['recovered']
        country.deaths = all_data['deaths']
        country.continent = all_data.get('continent', None)
        country.population = all_data.get('population', None)
        country.sq_km_area = all_data.get('sq_km_area', None)
        country.life_expectancy = all_data.get('life_expectancy', None)
        country.elevation_in_meters = all_data.get('elevation_in_meters', None)
        country.abbreviation = all_data.get('abbreviation', None)
        country.location = all_data.get('location', None)
        country.iso = all_data.get('iso', None)
        country.capital_city = all_data.get('capital_city', None)
        country.lat = all_data.get('lat', None)
        country.long = all_data.get('long', None)
        country.updated = datetime.datetime.strptime(all_data['updated']+'00', '%Y/%m/%d %H:%M:%S%z') if all_data.get('updated') is not None else None
        db.add(country)

        if len(list_regions) == 1:  # Only have All object
            continue

        for re in list_regions:
            if re != "All":
                region_obj = data_as_dict[co][re]
                region = Region()
                region.name = re
                region.lat = region_obj['lat']
                region.long = region_obj['long']
                region.confirmed = region_obj['confirmed']
                region.recovered = region_obj['recovered']
                region.deaths = region_obj['deaths']
                region.country_id = country.id
                region.updated = datetime.datetime.strptime(region_obj['updated']+'00', '%Y/%m/%d %H:%M:%S%z') if region_obj.get(
                    'updated') is not None else None
                db.add(region)
    db.commit()
    print(f'Insert data finished')


if __name__ == '__main__':
    insert_data()
