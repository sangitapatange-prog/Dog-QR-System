import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

st.set_page_config(page_title="Dog Bio-Data Profile", page_icon="🐾", layout="centered")

# Streamlit secrets se secure JSON read karna
creds_dict = dict(st.secrets["gcp_service_account"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("DogRescueDB").sheet1

# --- Yahan se niche apna purana URL dog_id nikalne wala code same rakhna ---
query_params = st.query_params
url_dog_id = query_params.get("dog_id")
# ... baki same
