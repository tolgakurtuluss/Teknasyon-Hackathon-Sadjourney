import pandas as pd
import uuid
import random
from faker import Faker

fake = Faker('tr_TR')
user_data = []

def generate_turkish_phone_number():
    number = fake.numerify('905#########')
    return f"+{number[:2]} {number[2:5]}-{number[5:8]}-{number[8:10]}-{number[10:]}"

def generate_turkish_male_full_name():
    first_name = fake.first_name_male()
    last_name = fake.last_name_male()
    return f"{first_name} {last_name}"

def generate_turkish_car_plate_number():
    plate_number = fake.random_int(min=1, max=81)  # Random city code (1-81)
    plate_number = f"{plate_number:02d}"          # Format city code with leading zeros
    plate_number += f" {fake.random_uppercase_letter()}{fake.random_uppercase_letter()} "  # Random uppercase letters
    plate_number += str(fake.random_number(digits=3))   # Random digits (converted to string)
    return plate_number

for _ in range(80):
    user_id = str(uuid.uuid4())[:8]
    full_name = generate_turkish_male_full_name()
    password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))
    carplate = generate_turkish_car_plate_number()
    phone_number = generate_turkish_phone_number()
    
    user_data.append({
        'user_id': user_id,        
        'password': password,
        'full_name': full_name,
        'carplate': carplate,
        'phone_number': phone_number
    })

df = pd.DataFrame(user_data)
print(df)

df.to_csv("database/driverdata.csv", index=False)