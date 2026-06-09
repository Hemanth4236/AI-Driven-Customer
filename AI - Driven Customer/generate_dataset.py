import pandas as pd
import random

first_names = [
    "Jairam","Sneha","Rohit","Priya","Ravi","Anjali","Kiran",
    "Pooja","Vamsi","Divya","Arjun","Nikhil","Keerthi",
    "Harsha","Suresh","Swathi","Ram","Lakshmi","Akhil",
    "Bhavya","Teja","Manoj","Deepika","Krishna","Sai",
    "Kavya","Varun","Sindhu","Rakesh","Meghana"
]

data = []

for i in range(1, 101):

    customer_id = 1000 + i
    name = random.choice(first_names)

    age = random.randint(18, 60)

    gender = random.choice(["Male", "Female"])

    annual_income = random.randint(300000, 1500000)

    monthly_salary = annual_income // 12

    monthly_spending = random.randint(
        int(monthly_salary * 0.20),
        int(monthly_salary * 0.80)
    )

    purchase_frequency = random.randint(1, 20)

    churn = random.choice([0, 1])

    data.append([
        customer_id,
        name,
        age,
        gender,
        annual_income,
        monthly_salary,
        monthly_spending,
        purchase_frequency,
        churn
    ])

df = pd.DataFrame(
    data,
    columns=[
        "Customer_ID",
        "Name",
        "Age",
        "Gender",
        "Annual_Income",
        "Monthly_Salary",
        "Monthly_Spending",
        "Purchase_Frequency",
        "Churn"
    ]
)

df.to_csv("customers.csv", index=False)

print("100 customer records generated successfully!")