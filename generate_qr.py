# Terminal mein pehle run karein: pip install qrcode[pil]
import qrcode

# Tumhari Streamlit app ka live link (Deploy hone ke baad jo milega)
base_url = "https://yatharth-dogs.streamlit.app"

# Kis dog ke liye QR bana rahe ho?
dog_id = "sheru001" 

# Final link jo QR code mein save hoga
final_url = f"{base_url}/?dog_id={dog_id}"

# QR Code create karna
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction so scratched QR also works
    box_size=10,
    border=4,
)
qr.add_data(final_url)
qr.make(fit=True)

# Image save karna
img = qr.make_image(fill_color="black", back_color="white")
img.save(f"{dog_id}_qrcode.png")

print(f"QR code saved for {dog_id}. It will redirect to: {final_url}")