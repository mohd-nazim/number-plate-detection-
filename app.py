import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import pytesseract

# Load Haar cascade
plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

def detect_plate(frame):
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
    return frame

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = detect_plate(img)
    return img

st.title("🚘 License Plate Detector with Browser Webcam")

webrtc_streamer(
    key="license-plate-detector",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

