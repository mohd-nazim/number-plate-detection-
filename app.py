import streamlit as st
from streamlit_webrtc import webrtc_streamer
from av import VideoFrame
import cv2
import pytesseract

st.set_page_config(page_title="License Plate Detector", layout="centered")
st.title("🚘 Live License Plate Detection")

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
        cv2.putText(frame, detected_text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (36,255,12), 2)

    st.session_state.detected_text = detected_text
    return frame

def video_frame_callback(frame):
    try:
        img = frame.to_ndarray(format="bgr24")
        img = detect_plate(img)
        return VideoFrame.from_ndarray(img, format="bgr24")
    except Exception as e:
        st.error(f"Error in video callback: {e}")
        return frame

if 'detected_text' not in st.session_state:
    st.session_state.detected_text = "Not Detected"

webrtc_streamer(
    key="live-detector",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {
                "urls": [
                    "turn:turn.xirsys.com:3478?transport=udp",
                    "turn:turn.xirsys.com:3478?transport=tcp"
                ],
                "username": "mohdnazim",
                "credential": "Abcd+1234"
            }
        ]
    },
)

st.markdown(f"### Detected Plate: **{st.session_state.detected_text}**")
