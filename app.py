import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

st.set_page_config(page_title="Dog Bio-Data Profile", page_icon="🐾", layout="centered")

# Custom CSS for aesthetics (Photo centering, rounded corners, card design)
st.markdown("""
<style>
    .profile-img-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .profile-img {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        max-width: 300px; /* Isse photo choti aur perfect lagegi */
        height: auto;
        object-fit: cover;
    }
    .dog-name {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .info-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .info-item {
        margin-bottom: 10px;
        font-size: 1.1em;
    }
    .info-label {
        font-weight: 600;
        color: #555;
    }
    .map-container {
        margin-top: 20px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Google Sheets Setup
try:
    creds_dict = dict(st.secrets["gcp_service_account"])
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("DogRescueDB").sheet1

    # URL se ID nikalna
    query_params = st.query_params
    url_dog_id = query_params.get("dog_id")

    if url_dog_id:
        records = sheet.get_all_records()
        dog_data = next((item for item in records if str(item.get("Dog_ID", "")) == str(url_dog_id)), None)
        
        if dog_data:
            # Helper to get data regardless of case
            def get_val(key):
                return dog_data.get(key, dog_data.get(key.lower(), "N/A"))

            name = get_val("Name")
            age = get_val("Age")
            dog_type = get_val("Type")
            location = get_val("Location")
            photo_url = get_val("Photo_URL")
            
            # Agar sheet mein Medical aur Contact ke columns hue, toh ye dikhayega
            medical = get_val("Medical")
            contact = get_val("Emergency_Contact")
            
            # --- Centered Image ---
            st.markdown(f'<div class="profile-img-container"><img src="{photo_url}" class="profile-img" alt="{name}"></div>', unsafe_allow_html=True)
            
            # --- Title ---
            st.markdown(f'<div class="dog-name">🐾 {name.upper()}\'S PROFILE</div>', unsafe_allow_html=True)
            
            # --- Beautiful Info Card ---
            medical_html = f'<div class="info-item"><span class="info-label">💉 Medical Info:</span> {medical}</div>' if medical != "N/A" else ""
            contact_html = f'<div class="info-item"><span class="info-label">📞 Emergency Contact:</span> {contact}</div>' if contact != "N/A" else ""
            
            st.markdown(f"""
            <div class="info-card">
                <div class="info-item"><span class="info-label">🎂 Age:</span> {age}</div>
                <div class="info-item"><span class="info-label">🏷️ Category:</span> {dog_type}</div>
                <div class="info-item"><span class="info-label">📍 Location:</span> {location}</div>
                {medical_html}
                {contact_html}
            </div>
            """, unsafe_allow_html=True)
            
            # --- Live Google Map ---
            st.subheader("🗺️ Last Known Location")
            # Create a Google Maps embed URL based on the Location column
            map_location = str(location).replace(" ", "+")
            map_html = f"""
            <div class="map-container">
                <iframe 
                    width="100%" 
                    height="300" 
                    frameborder="0" 
                    scrolling="no" 
                    marginheight="0" 
                    marginwidth="0" 
                    src="https://maps.google.com/maps?q={map_location}&hl=en&z=15&output=embed">
                </iframe>
            </div>
            """
            st.markdown(map_html, unsafe_allow_html=True)

        else:
            st.error("Dog profile not found in database! Please check the QR code.")
    else:
        st.info("Welcome! Please scan a valid Dog QR Code to view the profile.")

except Exception as e:
    st.error(f"Configuration or Database error: {e}")
    st.info("Please check if Streamlit secrets are configured correctly.")
