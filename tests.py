import unittest
from unittest import TestCase
from app import *


class SGApi(TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        """Tests index page"""
        res = self.client.get('/')
        self.assertIn(b'You are at index', res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_people(self):
        """Tests '/people' endpoint"""
        
        res = self.client.get('/people')
        self.assertEqual(res.status_code, 200)

        with app.app_context():
            example_person = {
                "id": "ba924631-068e-4436-b6de-f3283fa848f0",
                "name": "Ashitaka",
                "gender": "male",
                "age": "late teens",
                "eye_color": "brown",
                "hair_color": "brown",
                "films": [],
                "species": "https://ghibliapi.herokuapp.com/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2",
                "url": "https://ghibliapi.herokuapp.com/people/ba924631-068e-4436-b6de-f3283fa848f0"
                }
            self.assertIn(example_person["url"], get_people().json)

    def test_get_brown_haired_humans(self):
        """Tests /people/<string:color>-haired' endpoint"""
        res = self.client.get('/people/<string:color>-haired')
        self.assertEqual(res.status_code, 200)

        with app.app_context():
            # Test brown-hair only; will have to write a test for each color
            example_person = {
                "id": "ba924631-068e-4436-b6de-f3283fa848f0",
                "name": "Ashitaka",
                "gender": "male",
                "age": "late teens",
                "eye_color": "brown",
                "hair_color": "brown",
                "films": [],
                "species": "https://ghibliapi.herokuapp.com/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2",
                "url": "https://ghibliapi.herokuapp.com/people/ba924631-068e-4436-b6de-f3283fa848f0"
                }
            self.assertIn(example_person["url"], get_humans('Brown').json)
    
    def test_get_pilots(self):
        """Tests /pilots endpoint"""
        res = self.client.get('/pilots')
        self.assertEqual(res.status_code, 200)

        with app.app_context():
            example_pilot = {
                "pilot_name": "Colonel Muska",
                "url": "https://ghibliapi.herokuapp.com/people/40c005ce-3725-4f15-8409-3e1b1b14b583",
                "vehicle_name": "Air Destroyer Goliath"
            }
            self.assertIn(example_pilot, get_pilots().json)

    def test_create_nonsg_person(self):
        """Tests /nonsg_people endpoint with POST method and outcome"""

        with app.app_context():
            r = self.client.get('/nonsg_people')
            r_data = json.loads(r.data)
            nonsg_people = r_data["nonsg_people"]
            ids = [person["id"] for person in nonsg_people]
            current_last_id = ids[-1]

            example_person = {
                "id": current_last_id + 1,
                "name": "Example Name",
                "species": "af3910a6-429f-4c74-9ad5-dfe1c4aa04f2"
            }

            res = self.client.post('/nonsg_people', json=example_person)
            self.assertEqual(res.status_code, 201)

            self.assertIn(example_person, get_nonsg_people().json["nonsg_people"])

    def test_delete_nonsg_person(self):
        """Tests /nonsg_people endpoint with DELETE method and outcome"""

        with app.app_context():
            # example_nonsg_id = 1
            # print(delete_nonsg_person(example_nonsg_id).json["nonsg_person_deleted"])
            # deleted_person = delete_nonsg_person(example_nonsg_id).json["nonsg_person_deleted"]
            res = self.client.delete('/nonsg_people/1', follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            # self.assertNotIn(deleted_person, get_nonsg_people().json["nonsg_people"])


if __name__ == "__main__":
    unittest.main()
