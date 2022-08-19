# data to be sent to api
import random
import requests

API_URL = "http://127.0.0.1:8080/"

fields = ['Name', 'Email', 'Title', 'Sport', 'Os', 'Programming', 'Drink', 'Contact', 'Social', 'Timezone',
          'Entertainment', 'Hobby']
names = {
    'FirstName': ['John', 'Joe', 'Tom', 'Chris', 'Steve'],
    'LastName': ['Smith', 'Williams', 'Brown', 'Jones', 'Davis']
}

options = {
    'Title': ['Intern', 'SWE', 'PM', 'DS', 'Manager'],
    'Sport': ['football', 'basketball', 'baseball', 'tennis', 'soccer'],
    'Os': ['pc', 'mac'],
    'Programming': ['frontend', 'backend', 'fullstack'],
    'Drink': ['coffee', 'tea'],
    'Contact': ['teams', 'email', 'linkedin', 'slack'],
    'Social': ['facebook', 'twitter', 'tiktok', 'instagram'],
    'Timezone': ['eastern', 'central', 'mountain', 'pacific', 'other'],
    'Entertainment': ['movie', 'tv'],
    'Hobby': ['read', 'code', 'netflix', 'outside']}


def send_data():
    data = {}
    fullnames = []
    emails = []
    for f in names['FirstName']:
        for l in names['LastName']:
            fullnames.append(f + ' ' + l)
            emails.append(f.lower() + '.' + l.lower() + '@ukg.com')

    for i in range(len(fullnames)):
        for k, v in options.items():
            data[k] = v[random.randint(0, len(v) - 1)]

        data['Name'] = fullnames[i]
        data['Email'] = emails[i]

        requests.post(url=API_URL + "add", json=data)


# data = {'Email': "a.b@ukg.com",
#         'Animal': "bunny",
#         'IceCream': "Vanilla"
#         }

# sending post request and saving response as response object
# r = requests.post(url=API_URL + "add", json=data)

send_data()
