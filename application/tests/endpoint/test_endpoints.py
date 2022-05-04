from starlette.testclient import TestClient

from application import create_app

app = create_app()
client = TestClient(app)


class TestEndPoints:

    def test_get_countries(self):
        response = client.get("/data/countries")
        assert response.status_code == 200

    def test_search_country(self):
        params = {
            "query_string": "12123213123",
            "page": 0,
            "size": 10,
        }
        response = client.get("/data/countries/search", params=params)
        assert response.status_code == 200

    def test_get_regions_country(self):
        country_id = "cbf7740f-d88a-4b3e-9390-508a549bdf13"
        response = client.get(f"/data/country/{country_id}/regions")
        assert response.status_code == 200

    def test_get_country(self):
        country_id = "cbf7740f-d88a-4b3e-9390-508a549bdf13"
        response = client.get(f"/data/country/{country_id}")
        assert response.status_code == 200

    def test_get_specific_region_country(self):
        country_id = "cbf7740f-d88a-4b3e-9390-508a549bdf13"
        region_id = "ccbbd4a7-29df-4804-8b5c-8013f7e2157d"
        response = client.get(f"/data/country/{country_id}/region/{region_id}")
        assert response.status_code == 200

    def test_create_country(self):
        response = client.get("/data/countries")
        assert response.status_code == 200

    def test_create_region(self):
        response = client.get("/data/countries")
        assert response.status_code == 200

    def test_delete_country(self):
        country_id = "cbf7740f-d88a-4b3e-9390-508a549bdf13"
        response = client.get(f"/data/country/{country_id}")
        assert response.status_code == 200

    def test_delete_region(self):
        country_id = "cbf7740f-d88a-4b3e-9390-508a549bdf13"
        region_id = "ccbbd4a7-29df-4804-8b5c-8013f7e2157d"
        response = client.get(f"/data/country/{country_id}/region/{region_id}")
        assert response.status_code == 200

    def test_update_country(self):
        country_id = "cbf7740f-d88a-4b3e-9390-508a549bdf13"
        request_body = {
            "name": "test string",
            "confirmed": 0,
            "recovered": 0,
            "deaths": 0,
            "population": 0,
            "sq_km_area": 0,
            "life_expectancy": "string",
            "elevation_in_meters": "string",
            "continent": "string",
            "abbreviation": "string",
            "location": "string",
            "iso": 0,
            "capital_city": "string",
            "lat": "string",
            "long": "string"
        }
        response = client.put(f"/data/country/{country_id}", json=request_body)
        assert response.status_code == 200

    def test_update_region(self):
        country_id = "cbf7740f-d88a-4b3e-9390-508a549bdf122"
        region_id = "ccbbd4a7-29df-4804-8b5c-8013f7e2157d"
        request_body = {
            "name": "Testing",
            "confirmed": 10,
            "recovered": 10,
            "deaths": 0,
            "lat": "string of lat",
            "long": "string of long"
        }
        response = client.put(f"/data/country/{country_id}/region/{region_id}", json=request_body)
        assert response.status_code == 200
