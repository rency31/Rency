import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize or load event data
if 'events' not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=["Event Name", "Date", "Time", "Description"])

# Helper function to add a new event
def add_event(event_name, date, time, description):
    new_event = pd.DataFrame([{
        "Event Name": event_name,
        "Date": date,
        "Time": time,
        "Description": description
    }])
    # Use pd.concat instead of append
    st.session_state.events = pd.concat([st.session_state.events, new_event], ignore_index=True)

# Helper function to edit an existing event
def edit_event(index, event_name, date, time, description):
    st.session_state.events.at[index, "Event Name"] = event_name
    st.session_state.events.at[index, "Date"] = date
    st.session_state.events.at[index, "Time"] = time
    st.session_state.events.at[index, "Description"] = description

# Helper function to delete an event
def delete_event(index):
    st.session_state.events = st.session_state.events.drop(index).reset_index(drop=True)

# Streamlit interface
st.title("Event Planner")

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Add Event", "View Events", "Edit/Delete Events"])

# Tab 1: Add Event
with tab1:
    st.header("Add a New Event")
    event_name = st.text_input("Event Name")
    date = st.date_input("Event Date", datetime.now())
    time = st.time_input("Event Time")
    description = st.text_area("Event Description")

    if st.button("Add Event"):
        if event_name:
            add_event(event_name, date, time, description)
            st.success("Event added successfully!")
        else:
            st.error("Event name is required.")

# Tab 2: View Events
with tab2:
    st.header("View All Events")
    if st.session_state.events.empty:
        st.write("No events added yet.")
    else:
        st.dataframe(st.session_state.events)

# Tab 3: Edit/Delete Events
with tab3:
    st.header("Edit or Delete Events")
    if st.session_state.events.empty:
        st.write("No events to edit or delete.")
    else:
        for i, row in st.session_state.events.iterrows():
            with st.expander(f"{row['Event Name']} - {row['Date']}"):
                new_name = st.text_input("Event Name", row["Event Name"], key=f"name_{i}")
                new_date = st.date_input("Date", row["Date"], key=f"date_{i}")
                new_time = st.time_input("Time", row["Time"], key=f"time_{i}")
                new_description = st.text_area("Description", row["Description"], key=f"desc_{i}")

                if st.button("Save Changes", key=f"save_{i}"):
                    edit_event(i, new_name, new_date, new_time, new_description)
                    st.success("Event updated successfully!")

                if st.button("Delete Event", key=f"delete_{i}"):
                    delete_event(i)
                    st.warning("Event deleted!")
