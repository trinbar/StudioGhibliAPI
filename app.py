import flask
from flask import Flask, request, json, jsonify, make_response
import requests  # for calling 3rd party API


app = Flask(__name__)


URL = 'https://ghibliapi.herokuapp.com'
MY_URL = 'http://localhost:5000'
HUMAN_SPECIES_ID = 'af3910a6-429f-4c74-9ad5-dfe1c4aa04f2'

nonsg_people = [
    {"id": 1,
    "name": "Trinity Gaerlan",
    "species": HUMAN_SPECIES_ID
    },
    {"id": 2,
    "name": "Ning Gaerlan",
    "species": HUMAN_SPECIES_ID
    },
    {"id": 3,
    "name": "Trini Monterola",
    "species": HUMAN_SPECIES_ID}
]

@app.route('/')
def index():
    return "You are at index"

@app.route('/people', methods=['GET'])
def get_people():
    """Returns all human urls"""

    res = requests.get(URL + '/species/' + HUMAN_SPECIES_ID)
    data = res.json()
    people = data["people"]

    return jsonify(people)

@app.route('/people/brown-haired', methods=['GET'])
def get_brown_haired_humans():
    """Returns all brown-haired humans"""

    # Initiate answer listd
    brown_haired_people = []

    all_people = requests.get(URL + '/species/' + HUMAN_SPECIES_ID)
    all_people = all_people.json()["people"]

    # Iterate through people at endpoint '/people'
    for url in all_people:
        res = requests.get(url)
        data = res.json()
        hair_color = data["hair_color"]
        if "Brown" in hair_color:
            brown_haired_people.append(url)
    # If "Brown" in "hair_colors".value, append people_id empty list

    # Return the empty list
    return jsonify(brown_haired_people)

@app.route('/pilots', methods=['GET'])
def get_pilots():
    """
    Returns pilot names and urls

        Output:
        {"name": "Colonel Muska",
        "url": "https://ghibliapi.herokuapp.com/people/40c005ce-3725-4f15-8409-3e1b1b14b583"}
    """

    # Returns a list of vehicle objects
    vehicles = requests.get(f'{URL}/vehicles').json()
    vehicle_names = list(map(lambda v: v["name"], vehicles))
    # Returns a list of pilot urls
    pilots = list(map(lambda x: x["pilot"], vehicles))

    answer = []

    for i in range(len(pilots)):
        res = requests.get(pilots[i])
        data = res.json()
        name = data["name"]
        url = data["url"]
        answer.append({
            "vehicle_name": vehicle_names[i],
            "pilot_name": name,
            "url": url
        })

    return jsonify(answer)

@app.route('/nonsg_people', methods=['GET'])
def get_nonsg_people():
    """Returns non_sg_people"""
    return jsonify({"nonsg_people": [person for person in nonsg_people]})

@app.route('/nonsg_people', methods=['POST'])
def create_nonsg_person():
    """Creates a non-Studio Ghibli person"""
    # Input must be a JSON object, and required fields: id, name, species=human

    data = request.json
    name = data["name"]

    if not data or not name:
        return make_response(jsonify({
            "message": "Please check that input is valid. Input must include name in JSON"
        }), 400)

    nonsg_person_to_create = {
        "id": nonsg_people[-1]["id"] + 1,
        "name": name,
        "species": HUMAN_SPECIES_ID
    }

    nonsg_people.append(nonsg_person_to_create)

    return make_response(jsonify({"nonsg_person created": nonsg_person_to_create}), 201)

@app.route('/nonsg_people/<int:nonsg_id>', methods=['DELETE'])
def delete_nonsg_person(nonsg_id):
    """Deletes a non-Studio Ghibli person"""

    nonsg_person_to_delete = [person for person in nonsg_people if person["id"] == nonsg_id]
    print('delete this person: ', nonsg_person_to_delete)
    
    if len(nonsg_person_to_delete) == 0:
        return make_response(jsonify({
            "message": "Please check that input is valid. Input must include name in JSON"
        }), 400)

    nonsg_people.remove(nonsg_person_to_delete[0])
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(debug=True)