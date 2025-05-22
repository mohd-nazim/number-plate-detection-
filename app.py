import streamlit as st
import cv2
import pytesseract

# ------------------ UI Setup ------------------
st.set_page_config(page_title="🚘 License Plate Detector", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #0e76a8;'>🚘 Live License Plate Detection</h1>",
    unsafe_allow_html=True
)

st.markdown("This app uses OpenCV and Tesseract OCR to detect vehicle number plates in real time.")
st.markdown("---")

# Sidebar Instructions
st.sidebar.title("📌 How to Use")
st.sidebar.info("""
1. Click the checkbox to start your webcam.
2. Hold a license plate visible in the frame.
3. Detected text will be displayed below the video.
""")

# Live Toggle
run = st.checkbox("🎥 Start Camera")

# Video Display Frame
FRAME_WINDOW = st.image([], channels="RGB", use_column_width=True)
plate_text_display = st.empty()

# Load Haar Cascade
plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# Start camera
camera = cv2.VideoCapture(0)

# Loop for video
while run:
    ret, frame = camera.read()
    if not ret:
        st.warning("⚠️ Could not access webcam.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, 1.1, 4)

    detected_text = "Not Detected"

    for (x, y, w, h) in plates:
        roi = frame[y:y + h, x:x + w]
        text = pytesseract.image_to_string(roi, config='--psm 8').strip()
        if text:
            detected_text = text
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, detected_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (36,255,12), 2)

    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    plate_text_display.markdown(
        f"<div style='background-color:#f5f5f5; padding:15px; border-radius:10px; text-align:center; font-size:20px; color:#1a5276;'><strong>📄 Detected Plate:</strong> {detected_text}</div>",
        unsafe_allow_html=True
    )

camera.release()
