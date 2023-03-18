import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
	'databaseURL': ""
})

ref = db.reference('Person')

data = {
	"111111":
		{
			"name": "Elon Musk",
			"major": "CSE",
			"starting_year": 2017,
			"total_attendance": 5,
			"standing": "S",
			"year": 4,
			"last_attendance_time": "2023-03-12 02:03:22"

		},
	"333333":
		{
			"name": "Nashith",
			"major": "IT",
			"starting_year": 2020,
			"total_attendance": 5,
			"standing": "S",
			"year": 4,
			"last_attendance_time": "2023-03-12 02:03:22"

		},
	"222222":
		{
			"name": "Laura Morano",
			"major": "Tailoring",
			"starting_year": 2002,
			"total_attendance": 7,
			"standing": "A",
			"year": 4,
			"last_attendance_time": "2023-03-12 02:03:22"

		}
}

for key, value in data.items():
	ref.child(key).set(value)
