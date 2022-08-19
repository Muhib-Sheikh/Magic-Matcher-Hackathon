import json
import os

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()  # this connects to our Firestore database
MentorCollection = db.collection('Mentors')  # opens 'places' collection
InternCollection = db.collection('Interns')  # opens 'places' collection


# print(doc.to_dict)

# docs = MentorCollection.stream()

# for i in docs:
#     print(i.to_dict())

# print(collection.stream())

def addPerson(keys, values):
    # collection = db.collection('Interns')
    data = {}

    for i in range(len(keys)):
        data[keys[i]] = values[i]

    db.collection('Interns').document(data['Email']).set(data)


def returnMatches(email):
    userDoc = InternCollection.document(email)
    print('userDoc: ', userDoc.to_dict())
    userInfo = userDoc.get().to_dict()
    compareScores = {"joe.johnson@ukg.com": 5000}

    docs = InternCollection.stream()
    try:
        for doc in docs:  # iterate through interns
            print('user: ', userInfo)
            compareToInfo = doc.to_dict()
            # print('compareToInfo: ', compareToInfo.items())
            internEmail = compareToInfo["Email"]
            # print('internEmail: ', internEmail)
            # print('email: ', email)
            if internEmail == email: continue
            compareScores[internEmail] = 0

            if compareToInfo.items() is None: continue

            for key, value in compareToInfo.items():  # iterate through preference dictionary
                # print('key: ', key)
                # print('value: ', value)
                if not userInfo: continue
                if value == userInfo[key]: compareScores[internEmail] += 1
    except Exception as e:
        print(e)

    return sorted(compareScores.items(), key=lambda pair: -pair[1])[:min(5, len(compareScores))]


# print(returnMatches("gabriel.mason@ukg.com"))

# addPerson('John Doe', 'test@test.com', 'Soft Eng', 'cat', 'vanilla', 'teams')


# TODO obtain user email from API, pass email to returnMatches, send data back to API

app = Flask(__name__)
CORS(app)

@app.route('/add', methods=['POST'])
@cross_origin()
def create():
    """
        create() : Add document to Firebase collection with request body.
    """
    # print(request.json)
    try:
        # first_name = request.json['firstname']
        # last_name = request.json['lastname']
        # email = request.json['email']
        # job_title = request.json['jobtitle']
        # favorite_animal = request.json['favanimal']
        # favorite_icecream = request.json['favicecream']
        # contact_platform = request.json['contactplatform']

        # keys = ["first_name", "last_name", "email", "job_title", "favorite_animal", "favorite_icecream", "contact_platform"]
        # values = [first_name, last_name, email, job_title, favorite_animal, favorite_icecream, contact_platform]

        keys = []
        values = []

        data = request.json
        # print(data.items())

        for k, v in data.items():
            keys.append(k)
            values.append(v)

        # print(keys, values)

        addPerson(keys, values)

        # addPerson(first_name, last_name, email, job_title, favorite_animal, favorite_icecream, contact_platform)
        return jsonify({"success": True}), 200

        # return jsonify(
        #     {"firstname": first_name, "lastname": last_name, "email": email, "jobtitle": job_title,
        #      "favanimal": favorite_animal, "favicecream": favorite_icecream,
        #      "contactplatform": contact_platform}), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 404


@app.route('/list', methods=['GET'])
def read():
    """
        read() : gets all matches from Firebase as JSON.
    """
    try:
        # Check if email was passed to URL query

        email_id = request.args.get("Email")

        if email_id:
            # matches = getMatches(email_id)
            matches = returnMatches(email_id)
            # print(matches)
            # matches = dict(matches)
            # for m in matches:

            response = jsonify(dict(matches))
        else:
            response = jsonify({"email": "No email given"})

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception as e:
        return f"An Error Occurred: {e}", 404


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
