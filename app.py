import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. UI sabse pehle load karo taaki black screen na aaye
st.set_page_config(page_title="Dog Bio-Data", page_icon="🐾", layout="centered")
st.title("🐾 Dog Rescue & Bio-Data System")

# 2. Check karo ki scan kiya hua URL aaya hai ya normal link
query_params = st.query_params
url_dog_id = query_params.get("dog_id")

if url_dog_id:
    # 3. Agar QR scan hua hai, toh hi Google Sheets se connect karo
    with st.spinner("Fetching profile from database... ⏳"):
        try:
            creds_dict = dict(st.secrets["gcp_service_account"])
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            sheet = client.open("DogRescueDB").sheet1
            
            records = sheet.get_all_records()
            dog_data = next((item for item in records if str(item["Dog_ID"]) == str(url_dog_id)), None)
            
            if dog_data:
                st.image(dog_data["Photo_URL"], use_countainer_width=True)
                st.subheader(f"{dog_data['Name']}'s Profile")
                st.markdown(f"""
                **Age:** {dog_data['Age']}  
                **Type:** {dog_data['Type']}  
                **Location:** {dog_data['Location']}
                """)
            else:
                st.error("❌ Dog profile not found in database! Please check if data exists in Google Sheets.")
        except Exception as e:
            st.error(f"Database Connection Error: {e}")
            st.warning("Please check your Streamlit Secrets format.")
else:
    # Agar bina scan kiye khola hai, toh turant ye message dikhao
    st.info("✅ System is active and ready! Please scan a valid QR code to view a dog's profile.")
