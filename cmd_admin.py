import qrcode
import uuid
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("DogRescueDB").sheet1

print("\n🐾 DOG BIO-DATA ENTRY & QR GENERATOR 🐾\n")

name = input("Enter Dog's Name: ")
age = input("Enter Age (e.g., 2 Years): ")
dog_type = input("Domestic or Street Dog?: ")
location = input("Location/Address: ")
photo_url = input("Enter Photo Link (Any image URL): ")

# Unique ID banana
dog_id = f"{name.lower().replace(' ', '')}_{str(uuid.uuid4())[:5]}"

print("\nSaving to Google Sheets...")
sheet.append_row([dog_id, name, age, dog_type, location, photo_url])
print("✅ Data saved successfully!")

# !!! YAHAN APNA LIVE STREAMLIT LINK DAALNA JAB APP DEPLOY HO JAYE !!!
# Abhi test karne ke liye 'http://localhost:8501' use kar rahe hain
base_url = "http://localhost:8501" 
final_url = f"{base_url}/?dog_id={dog_id}"

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(final_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
filename = f"QR_{name}_{dog_id}.png"
img.save(filename)

print(f"\n✅ QR Code saved in your folder as: {filename}")