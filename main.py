import datetime as dt
import pandas as pd
import smtplib
import random
import os

today = dt.datetime.today()
birthdays_today = []

df = pd.read_csv("birthdays.csv")
df.columns = df.columns.str.strip()
    #clean column names
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

for index, row in df.iterrows():
    name = row["name"]
    email = row["email"]
    year = row["year"]
    month = int(row["month"])
    day = int(row["day"])
    if month == today.month and day == today.day:
        birthdays_today.append({"name": name, "email": email})

letter_templates = [
    "letter_templates/letter_1.txt",
    "letter_templates/letter_2.txt",
    "letter_templates/letter_3.txt",
]

for birthday in birthdays_today:
    with open(random.choice(letter_templates), "r") as f:
        letter = f.read()
    name = birthday["name"]
    email = birthday["email"]
    personalized = letter.replace("[NAME]", name)

    MY_EMAIL=os.environ.get("MY_EMAIL")
    MY_PASSWORD = os.environ.get("MY_PASSWORD")

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=email, msg= f"Subject: Happy Birthday!\n\n {personalized}"
    )
    connection.quit()
