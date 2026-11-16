
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env", override=True)

client = MongoClient(
    f"mongodb+srv://{os.getenv('MONGO_HOST')}/",
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASSWORD"),
    authSource="admin",
    serverSelectionTimeoutMS=10000
)

client.admin.command("ping")

db = client["student_management"]
students = db["students"]

sample_students = [
    {
        "roll_no": "STU001",
        "name": "Aarav Sharma",
        "age": 20,
        "department": "Computer Science",
        "semester": 5,
        "email": "aarav@example.com",
        "marks": 88,
        "skills": ["Python", "Java", "MongoDB"]
    },
    {
        "roll_no": "STU002",
        "name": "Ananya Patel",
        "age": 21,
        "department": "Data Science",
        "semester": 5,
        "email": "ananya@example.com",
        "marks": 92,
        "skills": ["Python", "Machine Learning"]
    },
    {
        "roll_no": "STU003",
        "name": "Rohan Mehta",
        "age": 20,
        "department": "Information Technology",
        "semester": 5,
        "email": "rohan@example.com",
        "marks": 76,
        "skills": ["HTML", "CSS", "JavaScript"]
    },
    {
        "roll_no": "STU004",
        "name": "Isha Kulkarni",
        "age": 21,
        "department": "Data Science",
        "semester": 5,
        "email": "isha@example.com",
        "marks": 95,
        "skills": ["Python", "SQL", "Power BI"]
    },
    {
        "roll_no": "STU005",
        "name": "Kabir Singh",
        "age": 20,
        "department": "Computer Science",
        "semester": 5,
        "email": "kabir@example.com",
        "marks": 81,
        "skills": ["C++", "Java", "Python"]
    },
    {
        "roll_no": "STU006",
        "name": "Meera Joshi",
        "age": 21,
        "department": "Information Technology",
        "semester": 5,
        "email": "meera@example.com",
        "marks": 89,
        "skills": ["React", "Node.js", "MongoDB"]
    },
    {
        "roll_no": "STU007",
        "name": "Aditya Deshmukh",
        "age": 20,
        "department": "Data Science",
        "semester": 5,
        "email": "aditya@example.com",
        "marks": 73,
        "skills": ["Python", "Statistics"]
    },
    {
        "roll_no": "STU008",
        "name": "Sara Khan",
        "age": 21,
        "department": "Computer Science",
        "semester": 5,
        "email": "sara@example.com",
        "marks": 94,
        "skills": ["Java", "Python", "AI"]
    },
    {
        "roll_no": "STU009",
        "name": "Dev Nair",
        "age": 20,
        "department": "Information Technology",
        "semester": 5,
        "email": "dev@example.com",
        "marks": 79,
        "skills": ["HTML", "CSS", "MongoDB"]
    },
    {
        "roll_no": "STU010",
        "name": "Priya Rao",
        "age": 21,
        "department": "Data Science",
        "semester": 5,
        "email": "priya@example.com",
        "marks": 91,
        "skills": ["Python", "Deep Learning", "SQL"]
    }
]

students.create_index("roll_no", unique=True)

inserted = 0

for student in sample_students:
    result = students.update_one(
        {"roll_no": student["roll_no"]},
        {"$setOnInsert": student},
        upsert=True
    )
    if result.upserted_id is not None:
        inserted += 1

print("SUCCESS! Database: student_management")
print("Collection: students")
print("New students inserted:", inserted)
print("Total students:", students.count_documents({}))

client.close()
