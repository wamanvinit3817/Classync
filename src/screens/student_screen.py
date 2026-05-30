import streamlit as st
from src.components.header_home import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)
from src.database.db import get_all_students, create_student
from src.pipelines.voice_pipeline import get_voice_embedding
import time
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
            f"""
            <h2 class="student-rep">Hi, {student_data['name']}</h2>

            <style>
            .student-rep{{
                color:black !important;
                font-weight:25 !important;
                font-size:1.8rem !important;
                margin-left:1rem !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()


    st.space()

    c1, c2 =st.columns(2)
    with c1:
        st.markdown(
            """
            <h2 class="student-rep">Your enrolled subjects</h2>

            <style>
            .student-rep{
                color:black !important;
                font-weight:25 !important;
                font-size:1.8rem !important;
                margin-left:1rem !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()


    st.divider()


    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']


        stats = stats_map.get(sid,{"total":0, "attended": 0} )
        def unenroll_button():
            if st.button(
                "Unenroll from this course",
                key=f"unenroll_{sid}",
                type='tertiary',
                width='stretch',
                icon=':material/delete_forever:'
            ):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenrolled from {sub['name']} successfully!")
                st.rerun()

        with cols[i % 2]:

            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()




def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
    else:
        student_screen_login()


def student_screen_login():

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    col1, col2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with col1:
        header_dashboard()

    with col2:
        if st.button(
            "Go Back to Home",
            key="loginbackbtn",
            type="secondary"
        ):
            st.session_state["login_type"] = None
            st.session_state.show_registration = False
            st.rerun()

    st.markdown(
        """
        <h2 class="student-rep">Login using FaceId:</h2>

        <style>
        .student-rep{
            color:black !important;
            font-weight:25 !important;
            font-size:1.8rem !important;
            margin-left:1rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.space()

    photo_source = st.camera_input(
        "Position your face in center, Please remove the spects if you are having them"
    )

    if photo_source:

        img = np.array(Image.open(photo_source))

        with st.spinner(
            "AI is scanning the face, Please wait..."
        ):

            detected, all_ids, num_faces = predict_attendance(
                img
            )
            #print(detected,all_ids,num_faces)

        if num_faces > 1:

            st.warning("Multiple faces detected!")

        elif num_faces == 0:

            st.warning("No faces detected!")

        else:

            if detected:

                student_id = list(detected.keys())[0]

                all_students = get_all_students()

                student = next(
                    (
                        s for s in all_students
                        if int(s["student_id"]) == int(student_id)
                    ),
                    None
                )

                if student:

                    st.session_state.is_logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.student_data = student
                    st.session_state.show_registration = False

                    st.success(
                        f"Welcome back {student['name']}!"
                    )

                    time.sleep(1)
                    st.rerun()

            else:

                st.info(
                    "Face not recognized. You might be a new student!"
                )

                st.session_state.show_registration = True

    if st.session_state.show_registration:

        with st.container(border=True):

            st.markdown(
                """
                <h2 class="student-rep">
                    Register New Profile
                </h2>

                <style>
                .student-rep{
                    color:black !important;
                    font-weight:25 !important;
                    font-size:1.8rem !important;
                    margin-left:1rem !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.space()

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g John Doe"
            )

            st.markdown(
        """
        <h2 class="student-rep">Optional voice recording :</h2>

        <style>
        .student-rep{
            color:black !important;
            font-weight:25 !important;
            font-size:1.2rem !important;
            margin-left:1rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
        )

            st.info(
                "Enroll for voice-only attendance"
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Record a short phrase like: "
                    "I am present, my name is John Doe"
                )

            except Exception:

                st.error("Audio recording failed!")

            if st.button(
                "Create Account",
                type="primary"
            ):

                if not photo_source:

                    st.error(
                        "Please capture your face first."
                    )

                elif not new_name:

                    st.error(
                        "Please enter your name."
                    )

                else:

                    with st.spinner(
                        "Creating account, Please wait..."
                    ):

                        img = np.array(
                            Image.open(photo_source)
                        )

                        encodings = get_face_embeddings(
                            img
                        )
                        #print("Faces Detected =", len(encodings))

                        if encodings:

                            face_emb = (
                                encodings[0].tolist()
                            )

                            voice_emb = None

                            if audio_data:

                                voice_emb = (
                                    get_voice_embedding(
                                        audio_data.read()
                                    )
                                )

                            response_data = create_student(
                                new_name,
                                face_emb,
                                voice_emb
                            )

                            if response_data:

                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = (
                                    response_data[0]
                                )

                                st.session_state.show_registration = False

                                st.success(
                                    f"Profile created. Hi {new_name}!"
                                )

                                time.sleep(1)
                                st.rerun()

                            else:

                                st.error(
                                    "Failed to create profile."
                                )

                        else:

                            st.error(
                                "Could not recognize facial features for registration."
                            )

    footer_dashboard()