import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firebase collection with request body.
    """
    print(request.json)
    try:
        first_name = request.json['firstname']
        last_name = request.json['lastname']
        email = request.json['email']
        job_title = request.json['jobtitle']
        favorite_animal = request.json['favanimal']
        favorite_icecream = request.json['favicecream']
        contact_platform = request.json['contactplatform']

        # addPerson(first_name, last_name, email, job_title, favorite_animal, favorite_icecream, contact_platform)
        # return jsonify({"success": True}), 200

        return jsonify(
            {"firstname": first_name, "lastname": last_name, "email": email, "jobtitle": job_title,
             "favanimal": favorite_animal, "favicecream": favorite_icecream,
             "contactplatform": contact_platform}), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 404


@app.route('/list', methods=['GET'])
def read():
    """
        read() : gets all matches from Firebase as JSON.
    """
    try:
        # Check if email was passed to URL query

        email_id = request.args.get("email")

        if email_id:
            return jsonify({"success": True}), 200
            # matches = getMatches(email_id)
            # return jsonify(matches), 200
        else:
            return jsonify({"email": "No email given"}), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 404


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
