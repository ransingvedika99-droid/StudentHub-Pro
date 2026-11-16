
import os
import re
import html
import pandas as pd
import streamlit as st
import altair as alt
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError

load_dotenv(".env", override=True)

st.set_page_config(
    page_title="StudentHub Pro | University Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
:root {
    --navy: #101827;
    --panel: #192438;
    --border: #34435c;
    --lavender: #c3b5fd;
    --muted: #a9b6ca;
}

.stApp {
    background: #101827;
    color: #eef2ff;
}

[data-testid="stSidebar"] {
    background: #151e30;
    border-right: 1px solid #2b3951;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f5f3ff !important;
    letter-spacing: -0.5px;
}

.portal-banner {
    background: linear-gradient(115deg, #253453, #35416b);
    border: 1px solid #4b537c;
    border-radius: 18px;
    padding: 30px 34px;
    margin-bottom: 26px;
}

.portal-banner h1 {
    font-size: 30px;
    margin: 0 0 10px;
    font-weight: 750;
}

.portal-banner p {
    color: #cbd4e9;
    font-size: 15px;
    margin: 0;
}

.eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #c3b5fd;
    margin-bottom: 12px;
}

.section-heading {
    font-size: 19px;
    font-weight: 700;
    color: #f1edff;
    margin: 28px 0 15px;
}

[data-testid="stMetric"] {
    background: #1c2940;
    border: 1px solid #364764;
    border-radius: 15px;
    padding: 22px;
    min-height: 132px;
}

[data-testid="stMetricLabel"] {
    color: #b5c1d5;
    font-size: 13px;
}

[data-testid="stMetricValue"] {
    color: #f5f3ff;
    font-size: 30px;
}

[data-testid="stForm"] {
    background: #1a263b;
    border: 1px solid #34445e;
    border-radius: 16px;
    padding: 24px;
}

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button {
    background: #7663c8;
    border: 1px solid #9382e5;
    border-radius: 9px;
    color: white;
    font-weight: 600;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    border-color: #c4b5fd;
    color: white;
}

[data-testid="stDataFrame"] {
    border: 1px solid #36435c;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 11px;
}

.portal-footer {
    color: #8191ac;
    font-size: 12px;
    text-align: center;
    padding: 22px 0 8px;
    border-top: 1px solid #283750;
    margin-top: 40px;
}


[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 6px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 10px 12px;
    border-radius: 9px;
    transition: background 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #25324b;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #2d3556;
    border: 1px solid #7568b9;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #e1d9ff;
    font-weight: 650;
}

[data-testid="stMetric"] {
    transition: transform 0.2s ease, border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: #9b8ce0;
}


:root {
    --navy: #722F37;
    --panel: #FFF1F5;
    --border: #E9A9BE;
    --lavender: #A64B5B;
    --muted: #9C6574;
}

.stApp {
    background: #FFF1F5;
    color: #722F37;
}

[data-testid="stSidebar"] {
    background: #722F37;
    border-right: 1px solid #A64B5B;
}

[data-testid="stSidebar"] * {
    color: #FFF1F5;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #8D3B48;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #F8C8DC;
    border: 1px solid #E9A9BE;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #722F37;
}

.portal-banner {
    background: linear-gradient(110deg, #722F37, #A64B5B);
    border: 1px solid #A64B5B;
    box-shadow: 0 10px 25px #722F3722;
}

.portal-banner h1 {
    color: #FFFFFF !important;
}

.portal-banner p {
    color: #FFE8EF;
}

.eyebrow {
    color: #F8C8DC;
}

h1, h2, h3 {
    color: #722F37 !important;
}

.section-heading {
    color: #722F37;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E9A9BE;
    box-shadow: 0 5px 18px #722F3710;
}

[data-testid="stMetricLabel"] {
    color: #9C6574;
}

[data-testid="stMetricValue"] {
    color: #722F37;
}

[data-testid="stMetric"]:hover {
    border-color: #A64B5B;
    box-shadow: 0 8px 24px #722F3720;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E9A9BE;
}

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button {
    background: #722F37;
    border: 1px solid #A64B5B;
    color: #FFFFFF;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background: #A64B5B;
    color: #FFFFFF;
}

[data-testid="stDataFrame"] {
    border: 1px solid #E9A9BE;
}

.portal-footer {
    color: #9C6574;
    border-top: 1px solid #E9A9BE;
}

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label {
    color: #722F37;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #FFF1F5;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #722F37;
}

[data-testid="stAppViewContainer"] [data-testid="stAlert"] p {
    color: inherit;
}


</style>
""", unsafe_allow_html=True)


@st.cache_resource

@st.cache_resource
def get_collection():
    def get_setting(name):
        if name in st.secrets:
            return st.secrets[name]
        return os.getenv(name)

    client = MongoClient(
        f"mongodb+srv://{get_setting('MONGO_HOST')}/",
        username=get_setting("MONGO_USER"),
        password=get_setting("MONGO_PASSWORD"),
        authSource="admin",
        serverSelectionTimeoutMS=10000
    )

    client.admin.command("ping")
    return client["student_management"]["students"]


try:
    students = get_collection()
except Exception:
    st.error("Unable to connect to MongoDB Atlas.")
    st.stop()


DEPARTMENTS = [
    "Computer Science",
    "Data Science",
    "Information Technology"
]


def get_records(query=None, sort_field="name", order=1):
    return list(
        students.find(
            query if query is not None else {},
            {"_id": 0}
        ).sort(sort_field, order)
    )


def get_dataframe(query=None, sort_field="name", order=1):
    return pd.DataFrame(
        get_records(query, sort_field, order)
    )


def banner(title, subtitle, category="UNIVERSITY ADMINISTRATION"):
    st.markdown(
        f"""
        <div class="portal-banner">
            <div class="eyebrow">{html.escape(category)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def heading(title):
    st.markdown(
        f'<div class="section-heading">{html.escape(title)}</div>',
        unsafe_allow_html=True
    )


def show_table(df):
    if df.empty:
        st.info("No matching student records found.")
        return

    columns = [
        "roll_no", "name", "department",
        "semester", "marks", "email", "skills"
    ]
    visible = [col for col in columns if col in df.columns]

    st.dataframe(
        df[visible],
        width="stretch",
        hide_index=True,
        column_config={
            "roll_no": "Roll Number",
            "name": "Student Name",
            "department": "Department",
            "semester": "Semester",
            "marks": st.column_config.ProgressColumn(
                "Marks",
                min_value=0,
                max_value=100,
                format="%d"
            ),
            "email": "Email Address",
            "skills": st.column_config.ListColumn("Skills")
        }
    )


def valid_email(email):
    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email.strip()
        )
    )


def department_options(current=None):
    options = DEPARTMENTS.copy()
    if current and current not in options:
        options.append(current)
    return options


def department_analytics():
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "total_students": {"$sum": 1},
                "average_marks": {"$avg": "$marks"},
                "highest_marks": {"$max": "$marks"}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    return list(students.aggregate(pipeline))



import altair as alt


def draw_department_chart(df):
    chart = alt.Chart(df).mark_bar(
        color="#A64B5B",
        cornerRadiusTopLeft=7,
        cornerRadiusTopRight=7
    ).encode(
        x=alt.X("Department:N", title=None),
        y=alt.Y("total_students:Q", title="Students"),
        tooltip=["Department", "total_students"]
    ).properties(
        height=300
    ).configure_view(
        stroke=None
    ).configure(
        background="#FFF1F5",
        axis={
            "labelColor": "#722F37",
            "titleColor": "#722F37",
            "gridColor": "#E9A9BE",
            "domainColor": "#E9A9BE",
            "tickColor": "#E9A9BE"
        }
    )

    st.altair_chart(chart, width="stretch")


def draw_marks_chart(df):
    chart = alt.Chart(df).mark_bar(
        color="#E9A9BE",
        cornerRadiusTopLeft=7,
        cornerRadiusTopRight=7
    ).encode(
        x=alt.X("Department:N", title=None),
        y=alt.Y("average_marks:Q", title="Average Marks"),
        tooltip=["Department", "average_marks"]
    ).properties(
        height=300
    ).configure_view(
        stroke=None
    ).configure(
        background="#FFF1F5",
        axis={
            "labelColor": "#722F37",
            "titleColor": "#722F37",
            "gridColor": "#E9A9BE",
            "domainColor": "#E9A9BE",
            "tickColor": "#E9A9BE"
        }
    )

    st.altair_chart(chart, width="stretch")


st.sidebar.markdown("## 🎓 StudentHub Pro")
st.sidebar.caption("UNIVERSITY MANAGEMENT PORTAL")
st.sidebar.divider()

page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Dashboard",
        "Student Registration",
        "Student Directory",
        "Update Records",
        "Delete Records",
        "Academic Analytics"
    ]
)

admin_pages = [
    "Student Registration",
    "Update Records",
    "Delete Records"
]

if page in admin_pages:
    st.sidebar.divider()
    admin_password = st.sidebar.text_input(
        "Admin Password",
        type="password"
    )

    try:
        correct_password = st.secrets["ADMIN_PASSWORD"]
    except (KeyError, FileNotFoundError):
        correct_password = os.getenv("ADMIN_PASSWORD", "")

    if not correct_password or admin_password != correct_password:
        st.warning("Admin access required to modify student records.")
        st.stop()


st.sidebar.divider()
st.sidebar.markdown("**SYSTEM STATUS**")
st.sidebar.success("MongoDB Atlas Connected")
st.sidebar.caption("Python · Streamlit · MongoDB")

if st.sidebar.button("Refresh Data"):
    st.rerun()


if page == "Dashboard":
    banner(
        "University Overview",
        "Monitor student records, academic performance and department activity."
    )

    total = students.count_documents({})
    department_count = len(students.distinct("department"))
    top_performers = students.count_documents(
        {"marks": {"$gte": 90}}
    )

    average_result = list(students.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$marks"}}}
    ]))
    average = average_result[0]["avg"] if average_result else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Students", total)
    c2.metric("Departments", department_count)
    c3.metric("Average Marks", f"{average:.1f}")
    c4.metric("High Achievers (90+)", top_performers)

    heading("Academic Performance")

    results = department_analytics()

    if results:
        analytics = pd.DataFrame(results).rename(
            columns={"_id": "Department"}
        )

        left, right = st.columns(2, gap="large")

        with left:
            st.subheader("Department Enrollment")
            draw_department_chart(analytics)

        with right:
            st.subheader("Average Department Marks")
            draw_marks_chart(analytics)

    heading("Student Directory Preview")

    df = get_dataframe()
    show_table(df.head(8))

    st.caption("Showing up to 8 students. Open Student Directory for all records.")


elif page == "Student Registration":
    banner(
        "Student Registration",
        "Create a new student record in the university database.",
        "STUDENT ADMINISTRATION"
    )

    with st.form("registration_form", clear_on_submit=True):
        st.subheader("Personal & Academic Information")

        left, right = st.columns(2, gap="large")

        with left:
            roll_no = st.text_input(
                "Student Roll Number",
                placeholder="STU013"
            )
            name = st.text_input(
                "Full Name",
                placeholder="Enter student name"
            )
            age = st.number_input(
                "Age", 1, 100, 20
            )
            email = st.text_input(
                "Email Address",
                placeholder="student@example.com"
            )

        with right:
            department = st.selectbox(
                "Department", DEPARTMENTS
            )
            semester = st.number_input(
                "Semester", 1, 8, 5
            )
            marks = st.number_input(
                "Marks", 0, 100, 75
            )
            skills = st.text_input(
                "Skills",
                placeholder="Python, SQL, MongoDB"
            )

        submitted = st.form_submit_button(
            "Register Student",
            type="primary"
        )

    if submitted:
        if not roll_no.strip() or not name.strip():
            st.warning("Roll number and full name are required.")
        elif not valid_email(email):
            st.warning("Please enter a valid email address.")
        else:
            document = {
                "roll_no": roll_no.strip(),
                "name": name.strip(),
                "age": int(age),
                "email": email.strip(),
                "department": department,
                "semester": int(semester),
                "marks": int(marks),
                "skills": [
                    item.strip()
                    for item in skills.split(",")
                    if item.strip()
                ]
            }

            try:
                students.insert_one(document)
                st.success("Student registered successfully!")
            except DuplicateKeyError:
                st.error("This roll number already exists.")
            except PyMongoError:
                st.error("Unable to save the student record.")


elif page == "Student Directory":
    banner(
        "Student Directory",
        "Browse, search and export student information.",
        "RECORDS MANAGEMENT"
    )

    left, middle, right = st.columns(3)

    with left:
        search = st.text_input(
            "Search Students",
            placeholder="Name or roll number"
        )

    with middle:
        department = st.selectbox(
            "Department Filter",
            ["All Departments"] +
            sorted(students.distinct("department"))
        )

    with right:
        sort_by = st.selectbox(
            "Sort Records",
            ["Name A–Z", "Highest Marks", "Lowest Marks"]
        )

    query = {}

    if search.strip():
        pattern = re.escape(search.strip())
        query["$or"] = [
            {"name": {"$regex": pattern, "$options": "i"}},
            {"roll_no": {"$regex": pattern, "$options": "i"}}
        ]

    if department != "All Departments":
        query["department"] = department

    sorting = {
        "Name A–Z": ("name", 1),
        "Highest Marks": ("marks", -1),
        "Lowest Marks": ("marks", 1)
    }

    sort_field, order = sorting[sort_by]
    df = get_dataframe(query, sort_field, order)

    st.metric("Matching Records", len(df))

    heading("Registered Students")
    show_table(df)

    if not df.empty:
        st.download_button(
            "Download CSV Report",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="student_directory.csv",
            mime="text/csv"
        )


elif page == "Update Records":
    banner(
        "Update Student Records",
        "Modify student information while preserving their roll number.",
        "RECORDS MANAGEMENT"
    )

    roll_numbers = sorted(students.distinct("roll_no"))

    if not roll_numbers:
        st.info("No student records available.")
    else:
        selected = st.selectbox(
            "Choose Student Roll Number",
            roll_numbers
        )

        student = students.find_one({"roll_no": selected})

        if student:
            st.info(
                f"Selected Student: {student.get('name', '')}"
            )

            with st.form(f"edit_{selected}"):
                left, right = st.columns(2, gap="large")

                with left:
                    name = st.text_input(
                        "Full Name",
                        value=student.get("name", "")
                    )
                    age = st.number_input(
                        "Age", 1, 100,
                        int(student.get("age", 20))
                    )
                    email = st.text_input(
                        "Email Address",
                        value=student.get("email", "")
                    )

                with right:
                    current = student.get(
                        "department", DEPARTMENTS[0]
                    )
                    options = department_options(current)

                    department = st.selectbox(
                        "Department",
                        options,
                        index=options.index(current)
                    )
                    semester = st.number_input(
                        "Semester", 1, 8,
                        int(student.get("semester", 5))
                    )
                    marks = st.number_input(
                        "Marks", 0, 100,
                        int(student.get("marks", 75))
                    )

                skills = st.text_input(
                    "Skills",
                    value=", ".join(student.get("skills", []))
                )

                submitted = st.form_submit_button(
                    "Save Changes",
                    type="primary"
                )

            if submitted:
                if not name.strip() or not valid_email(email):
                    st.warning("Enter a name and valid email.")
                else:
                    try:
                        students.update_one(
                            {"roll_no": selected},
                            {
                                "$set": {
                                    "name": name.strip(),
                                    "age": int(age),
                                    "email": email.strip(),
                                    "department": department,
                                    "semester": int(semester),
                                    "marks": int(marks),
                                    "skills": [
                                        item.strip()
                                        for item in skills.split(",")
                                        if item.strip()
                                    ]
                                }
                            }
                        )
                        st.success("Student updated successfully!")
                    except PyMongoError:
                        st.error("Unable to update the student.")


elif page == "Delete Records":
    banner(
        "Delete Student Records",
        "Remove a student from the university database.",
        "RECORDS MANAGEMENT"
    )

    roll_numbers = sorted(students.distinct("roll_no"))

    if not roll_numbers:
        st.info("No students available.")
    else:
        selected = st.selectbox(
            "Select Student",
            roll_numbers
        )

        student = students.find_one({"roll_no": selected})

        if student:
            st.subheader("Student Details")

            st.write("**Roll Number:**", selected)
            st.write("**Name:**", student.get("name", ""))
            st.write(
                "**Department:**",
                student.get("department", "")
            )

            st.warning(
                "Deleting this record is permanent. "
                "Please confirm the selected student."
            )

            confirm = st.checkbox(
                "I confirm that I want to delete this record."
            )

            if st.button(
                "Delete Student",
                type="primary",
                disabled=not confirm
            ):
                try:
                    result = students.delete_one(
                        {"roll_no": selected}
                    )
                    if result.deleted_count:
                        st.success("Student deleted successfully!")
                        st.rerun()
                    else:
                        st.warning("Student record not found.")
                except PyMongoError:
                    st.error("Unable to delete the student.")


elif page == "Academic Analytics":
    banner(
        "Academic Analytics",
        "Department performance and enrollment insights.",
        "ACADEMIC INTELLIGENCE"
    )

    results = department_analytics()

    if not results:
        st.info("No student data available.")
    else:
        df = pd.DataFrame(results).rename(
            columns={"_id": "Department"}
        )

        total = int(df["total_students"].sum())
        departments = len(df)
        highest = int(df["highest_marks"].max())

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Enrollment", total)
        c2.metric("Active Departments", departments)
        c3.metric("Highest Marks", highest)

        heading("Department Performance")

        left, right = st.columns(2, gap="large")

        with left:
            st.subheader("Enrollment by Department")
            draw_department_chart(df)

        with right:
            st.subheader("Average Marks by Department")
            draw_marks_chart(df)

        heading("MongoDB Aggregation Summary")

        display = df.rename(
            columns={
                "total_students": "Total Students",
                "average_marks": "Average Marks",
                "highest_marks": "Highest Marks"
            }
        )

        display["Average Marks"] = display[
            "Average Marks"
        ].round(2)

        st.dataframe(
            display,
            width="stretch",
            hide_index=True
        )

        st.caption(
            "Data generated using MongoDB aggregation: "
            "$group, $sum, $avg, $max and $sort."
        )


st.markdown(
    """
    <div class="portal-footer">
        StudentHub Pro · University Management Portal
        <p>Powered by Python, Streamlit and MongoDB Atlas</p>
    </div>
    """,
    unsafe_allow_html=True
)
