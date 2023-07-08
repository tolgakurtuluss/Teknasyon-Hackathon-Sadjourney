import pandas as pd
import uuid
import random
import requests
import time
from faker import Faker

# dataset gathered from https://www.kaggle.com/datasets/mehmetuzelbey/10000-random-gaussiannormal-locations-in-istanbul
empdata = pd.read_csv("./employee.csv")
empdata = empdata.head(1000)

fake = Faker('tr_TR')
user_data = []

def generate_turkish_phone_number():
    number = fake.numerify('905#########')
    return f"+{number[:2]} {number[2:5]}-{number[5:8]}-{number[8:10]}-{number[10:]}"

def fake_photo_generator(gender):
    current_time = time.time()
    req = requests.get("https://this-person-does-not-exist.com/new?time="+ str(int(current_time)) + "&gender="+ str(gender) + "&age=26-35&etnic=all")
    content = req.json()
    link = "https://this-person-does-not-exist.com" + content['src']
    return link

for _ in range(1000):
    user_id = str(uuid.uuid4())[:8]
    gender = random.choice(["male", "female"])
    name = fake.first_name_male() if gender=="male" else fake.first_name_female()
    full_name = name + " " + fake.last_name()
    password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))
    attendance_status = random.choices([1, 0], k=5) + [0, 0]
    phone_number = generate_turkish_phone_number()

    user_data.append({

        'user_id': user_id,
        'password': password,
        'full_name': full_name,
        'gender': gender,
        'attendance_status': attendance_status,
        'phone_number': phone_number,
    })


df = pd.DataFrame(user_data)

df_c = pd.concat([df.reset_index(drop=True), empdata], axis=1)
print(df_c)

df_c.to_csv("database/employeedata.csv", index=False)