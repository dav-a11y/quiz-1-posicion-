import streamlit as st
import cv2
import mediapipe as mp
import threading
import time

st.set_page_config(page_title="Detección de Postura", layout="centered")
st.title("🧍‍♂️ Detección de Postura con MediaPipe")


st.sidebar.header("Configuración de Cámara")
cam_index = st.sidebar.selectbox("Selecciona la cámara:", [0, 1], index=0)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


frame_lock = threading.Lock()
frame_global = None
results_global = None
running = True


def detectar_postura(landmarks):
    cadera_izq = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    rodilla_izq = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    cadera_der = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    rodilla_der = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]

    altura_caderas = (cadera_izq.y + cadera_der.y) / 2
    altura_rodillas = (rodilla_izq.y + rodilla_der.y) / 2
    diferencia = altura_rodillas - altura_caderas

    return "🪑 de pie" if diferencia > 0.15 else "🧍 sentado"


def hilo_captura():
    global frame_global, running
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        st.error(f"❌ No se puede abrir la cámara /dev/video{cam_index}.")
        running = False
        return
    while running:
        ret, frame = cap.read()
        if not ret:
            continue
        with frame_lock:
            frame_global = frame.copy()
        time.sleep(0.03)  # 30 fps aprox
    cap.release()


def hilo_procesamiento():
    global frame_global, results_global, running
    while running:
        with frame_lock:
            if frame_global is None:
                continue
            frame_rgb = cv2.cvtColor(frame_global, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        with frame_lock:
            results_global = results
        time.sleep(0.05)


t1 = threading.Thread(target=hilo_captura, daemon=True)
t2 = threading.Thread(target=hilo_procesamiento, daemon=True)
t1.start()
t2.start()


frame_placeholder = st.empty()
estado_placeholder = st.empty()

while running:
    with frame_lock:
        if frame_global is None:
            continue
        frame = frame_global.copy()
        results = results_global

    if results and results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        estado = detectar_postura(results.pose_landmarks.landmark)
        estado_placeholder.markdown(f"### 🟢 Estado actual: **{estado}**")
    else:
        estado_placeholder.markdown("### ⚪ No se detecta persona")

    frame_placeholder.image(frame, channels="BGR")
    time.sleep(0.05)


running = False
