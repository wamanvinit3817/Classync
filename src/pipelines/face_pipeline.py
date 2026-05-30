import dlib
import face_recognition_models
import numpy as np
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(face_recognition_models.pose_predictor_five_point_model_location())
    facerec = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 0)

    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        encoding = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(encoding))

    return encodings


@st.cache_resource
def get_trained_model():
    student_db = get_all_students()

    if not student_db:
        return None

    x, y = [], []

    for student in student_db:
        embedding = student.get("face_embedding")

        if embedding:
            x.append(np.array(embedding))
            y.append(student.get("student_id"))

    if not x:
        return None

    unique_students = list(dict.fromkeys(y))

    if len(unique_students) < 2:
        return {"x": x, "y": y, "clf": None}

    try:
        clf = SVC(kernel="linear", probability=True, class_weight="balanced")
        clf.fit(x, y)
        return {"x": x, "y": y, "clf": clf}
    except Exception:
        return None


def train_classifier():
    st.cache_resource.clear()
    return bool(get_trained_model())


def predict_attendance(class_img_np):
    encodings = get_face_embeddings(class_img_np)
    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)

    clf = model_data["clf"]
    x = model_data["x"]
    y = model_data["y"]

    all_students = list(dict.fromkeys(y))

    if not encodings:
        return detected_students, all_students, 0

    resemblance_threshold = 0.5

    for encoding in encodings:

        if len(all_students) >= 2 and clf is not None:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        student_embedding = x[y.index(predicted_id)]

        distance = np.linalg.norm(student_embedding - encoding)

        if distance <= resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)