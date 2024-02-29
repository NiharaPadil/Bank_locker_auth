import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://bank-locker-authentication-default-rtdb.firebaseio.com/"
})


ref = db.reference('Auth_ppl')

data = {
    "Adithi":
        {
            "Name":"Adithi",
            "Acc_num":"Num1",
            "tot_login":1,
            "last_login":"2024-02-29 00:35:12"
        },
    "Lima":
        {
            "Name": "Lima",
            "Acc_num": "Num2",
            "tot_login": 1,
            "last_login": "2024-02-29 00:35:12"
        },
    "Mayur":
        {
            "Name": "Mayur",
            "Acc_num": "Num3",
            "tot_login": 1,
            "last_login": "2024-02-29 00:35:12"
        },
    "Nihara":
        {
            "Name": "Nihara",
            "Acc_num": "Num4",
            "tot_login": 1,
            "last_login": "2024-02-29 00:35:12"
        }
}

for key,value in data.items():
    ref.child(key).set(value)
