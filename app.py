import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from database import create_connection, create_tables
from auth import register_user, login_user
from medication import (
    get_all_medications,
    add_medication,
    delete_medication,
    mark_as_taken
)


# ---------------- EMAIL FUNCTION ---------------- #
def send_email_reminder(to_email, medicine_name, dosage):

    sender_email = st.secrets["EMAIL"]
    sender_password = st.secrets["PASSWORD"]

    subject = "💊 Medicine Reminder"

    body = f"""
Hello,

This is your medicine reminder.

Medicine: {medicine_name}
Dosage: {dosage}

Please take it now.

Stay Healthy 💙
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(
            sender_email,
            to_email,
            msg.as_string()
        )

        server.quit()
        return True

    except Exception as e:
        st.error(f"Email Error: {e}")
        return False


# ---------------- SETUP ---------------- #
st.set_page_config(
    page_title="Medication Reminder",
    layout="wide"
)

conn = create_connection()
create_tables(conn)


# ---------------- SESSION ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "email" not in st.session_state:
    st.session_state.email = None


# ---------------- AUTH ---------------- #
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Sign Up"]
    )

    if menu == "Login":

        st.title("💊 Medication Reminder Login")

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(
                conn,
                username,
                password
            )

            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.email = user[3]

                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid Credentials")

    elif menu == "Sign Up":

        st.title("📝 Create Account")

        new_user = st.text_input("New Username")
        email = st.text_input("Email")
        new_pass = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Register"):

            if new_user and email and new_pass:

                if register_user(
                    conn,
                    new_user,
                    new_pass,
                    email
                ):
                    st.success(
                        "Account Created! Please Login."
                    )

                else:
                    st.error(
                        "Username already exists"
                    )

            else:
                st.warning(
                    "Please fill all fields"
                )


# ---------------- MAIN APP ---------------- #
else:

    st_autorefresh(
        interval=60000,
        key="refresh"
    )

    st.sidebar.success(
        f"Welcome {st.session_state.username}"
    )

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Add Medication",
            "View Medications",
            "Logout"
        ]
    )

    if menu == "Add Medication":

        st.title("➕ Add Medication")

        name = st.text_input("Medication Name")
        dosage = st.text_input("Dosage")
        time_input = st.time_input("Time")

        if st.button("Add"):

            if name and dosage:

                add_medication(
                    conn,
                    st.session_state.user_id,
                    name,
                    dosage,
                    str(time_input)
                )

                st.success("Medication Added")

            else:
                st.warning("Fill all fields")

    elif menu == "View Medications":

        st.title("📋 Your Medications")

        df = get_all_medications(
            conn,
            st.session_state.user_id
        )

        if not df.empty:

            current_time = datetime.now().strftime("%H:%M")

            for _, row in df.iterrows():

                med_time = row["time"][:5]

                if (
                    row["status"] == "Pending"
                    and med_time == current_time
                ):

                    st.warning(
                        f"⏰ Reminder: Take {row['name']} ({row['dosage']}) now!"
                    )

                    email_sent = send_email_reminder(
                        st.session_state.email,
                        row["name"],
                        row["dosage"]
                    )

                    if email_sent:
                        mark_as_taken(
                            conn,
                            row["id"]
                        )

            total = len(df)
            taken = len(df[df["status"] == "Taken"])
            pending = len(df[df["status"] == "Pending"])

            col1, col2, col3 = st.columns(3)

            col1.metric("Total", total)
            col2.metric("Taken", taken)
            col3.metric("Pending", pending)

            st.divider()

            for _, row in df.iterrows():

                col1, col2, col3, col4, col5 = st.columns(5)

                col1.write(row["name"])
                col2.write(row["dosage"])
                col3.write(row["time"])
                col4.write(row["status"])

                if row["status"] == "Pending":

                    if col5.button(
                        "Mark Taken",
                        key=f"taken{row['id']}"
                    ):
                        mark_as_taken(
                            conn,
                            row["id"]
                        )
                        st.rerun()

                if col5.button(
                    "Delete",
                    key=f"delete{row['id']}"
                ):
                    delete_medication(
                        conn,
                        row["id"]
                    )
                    st.rerun()

        else:
            st.info("No medications added yet.")

    elif menu == "Logout":

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.email = None

        st.success("Logged Out")
        st.rerun()