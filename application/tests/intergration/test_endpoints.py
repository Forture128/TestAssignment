import json

from starlette.testclient import TestClient

from application.app import create_app

app = create_app()
client = TestClient(app)


class TestSingleCountry:
    def __init__(self, country, country_data) -> None:
        self.country = country
        self.country_data = country_data
        self.regions_of_country = [region for region in self.country_data.keys() if region != "All"]
        self.current_country_id: str = ""
        self.current_country_obj = None
        self.current_region_id: str = ""
        self.current_region_obj = None
        self.run_all_test_case_single()

    def run_all_test_case_single(self):
        test_cases = [
            'test_search_country',
            'test_get_country',
            'test_get_regions_country',
            'test_get_specific_region_country',

            'test_update_country',
            'test_update_region',

            'test_delete_country',
            'test_delete_region',
        ]
        for case in test_cases:
            getattr(TestSingleCountry, case)(self)
        return None

    def test_get_countries(self):
        response = client.get("/data/countries")
        assert response.status_code == 200

        response_data = response.json()
        assert response_data is not None
        for item in response_data['countries']:
            assert item['name'] == self.country

        for key, value in self.country_data['All'].items():
            assert key in response_data.keys()
            assert value == response_data[key]

    def test_search_country(self):
        params = {
            "query_string": self.country,
            "page": 0,
            "size": 10,
        }
        response = client.get("/data/countries/search", params=params)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['countries'] is not None
        if len(response_data['countries']) > 0:
            self.current_country_id = response_data['countries'][0]['id']
            self.current_country_obj = response_data['countries'][0]

    def test_get_regions_country(self):
        response = client.get(f"/data/country/{self.current_country_id}/regions")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data is not None
        for region in response_data['regions']:
            # if key == "All":
            #     continue
            assert region is not None
            assert region["name"] in self.regions_of_country
        if len(response_data['regions']) > 0:
            self.current_region_id = response_data['regions'][0]['id']
            self.current_country_obj = response_data['regions'][0]

    def test_get_country(self):
        response = client.get(f"/data/country/{self.current_country_id}")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data is not None

    def test_get_specific_region_country(self):
        if self.current_country_id and self.current_region_id:
            response = client.get(f"/data/country/{self.current_country_id}/region/{self.current_region_id}")
            assert response.status_code == 200
            response_data = response.json()
            assert response_data is not None
        return

    def test_delete_country(self):
        if self.current_country_id:
            response = client.delete(f"/data/country/{self.current_country_id}")
            assert response.status_code == 200
            response_data = response.json()
            assert response_data is True
        return

    def test_delete_region(self):
        if self.current_country_id and self.current_region_id:
            response = client.delete(f"/data/country/{self.current_country_id}/region/{self.current_region_id}")
            assert response.status_code == 200
            response_data = response.json()
            assert response_data is True
        return


def load_verify_data():
    json_path = "covid-stats.json"
    f = open(json_path)
    return json.load(f)


class TestIntegration:
    """
        This class will get random real data.

        Loop all test case in router
    """
    json_path = "covid-stats.json"
    f = open(json_path)
    json_data = json.load(f)

    def test_verify_data(self):
        for key, value in self.json_data.items():
            TestSingleCountry(key, value)
