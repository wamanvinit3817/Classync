import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header_home import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists
from src.database.db import create_teacher,teacher_login
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np

from datetime import datetime

import pandas as pd

from src.database.config import supabase


from src.components.dialog_voice_attendance import voice_attendance_dialog

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()
    
   
   
def teacher_dashboard():
    #st.header(f"Hi, {st.session_state.teacher_data['username']}")
    
    col1,col2 = st.columns(2,vertical_alignment="center",gap="xxlarge")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Logout",key="loginbackbtn",type="secondary",shortcut="control+backspace"):
            st.session_state.is_logged_in=False
            del st.session_state["teacher_data"]
            st.rerun()
    st.space()
    st.markdown(f"""
                <h2 class="hi-head">Welcome back, {st.session_state.teacher_data['username']} !</h2>
                    <style>
                    .hi-head{{
                        color:black !important;
                        font-weight:20 !important;
                        font-size:2.5rem !important;
                    }}
                    </style>
                """,unsafe_allow_html=True)
    
    st.space()
    
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1,tab2,tab3 = st.columns(3)
    
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',width='stretch',type=type1,icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects',width='stretch',icon=':material/book_ribbon:',type=type2):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()
    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',width='stretch',icon=':material/cards_stack:',type=type3):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()
            
    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()
    footer_dashboard()
    
def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.markdown(
        """
        <h2 class="student-rep">Take AI Attendance</h2>

        <style>
        .student-rep{
            color:black !important;
            font-weight:25 !important;
            font-size:1.8rem !important;
            margin-left:0rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.markdown(
            """
            <h2 class="student-rep">Added Photos:</h2>

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
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()


    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)


                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log  = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <h2 class="student-rep">Manage Subjects</h2>

            <style>
            .student-rep{
                color:black !important;
                font-weight:25 !important;
                font-size:1.8rem !important;
                margin-left:0rem !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:

        for sub in subjects:

            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats
            )

            if st.button(
                f"Share Code: {sub['name']}",
                key=f"share_{sub['subject_code']}",
                icon=":material/share:"
            ):
                share_subject_dialog(
                    sub['name'],
                    sub['subject_code']
                )

            st.space()

    else:
        st.info("No Subjects found! Create the one from above!")


def teacher_tab_attendance_records():
    st.markdown(
        """
        <h2 class="student-rep">Attendance Records:</h2>

        <style>
        .student-rep{
            color:black !important;
            font-weight:25 !important;
            font-size:1.8rem !important;
            margin-left:0rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)



    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)







def teacher_login_fn(teacher_username,teacher_password):
    if not teacher_username or not teacher_password:
        return False
    
    data = teacher_login(teacher_username,teacher_password)
    if data:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = data
        st.session_state.is_logged_in = True
        return True
    else:
        return False
    
    
def teacher_screen_login():
    col1,col2 = st.columns(2,vertical_alignment="center",gap="xxlarge")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go Back to Home",key="loginbackbtn",type="secondary",shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
        
    st.markdown("""
                <h2 class="student-rep">Login using password:</h2>
                    <style>
                    .student-rep{
                        color:black !important;
                        font-weight:25 !important;
                        font-size:1.8rem !important;
                    }
                    </style>
                """,unsafe_allow_html=True)
    st.space()
    teacher_username = st.text_input("Enter Username",placeholder="Anonymous")
    teacher_password = st.text_input("Enter Password",type="password",placeholder="Enter Password")
    st.divider()
    btnc1,btnc2 = st.columns(2)
    
    with btnc1:
        if st.button('Login',width="stretch",shortcut='control+enter',icon=":material/passkey:"):
           if teacher_login_fn(teacher_username,teacher_password):
               st.success(f"Welcome back {teacher_username}! 👋")
               import time
               time.sleep(2)
               st.rerun()
           else:
               st.error("Invalid username or password!")
    with btnc2:
        if st.button('Register Instead',width="stretch",icon=":material/passkey:",type="primary"):
            st.session_state.teacher_login_type='register'
            st.rerun()
    footer_dashboard()

def register_teacher(teacher_username,teacher_password,teacher_name,teacher_confirm_password):
    if not teacher_username or not teacher_password or not teacher_name or not teacher_confirm_password:
        return False,"All fields are required!"
    
    if check_teacher_exists(teacher_username):
        return False,"The username is already taken!"
    
    if teacher_password != teacher_confirm_password:
        return False,"Password doesnot match, Please try again!"
    
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True,"Registration Succesfull, Kindly Login Now!"
    except Exception as e: 
        print(e)
        return False,"Unexpected error occured!"
    
    
def teacher_screen_register():
    col1,col2 = st.columns(2,vertical_alignment="center",gap="xxlarge")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go Back to Home",key="loginbackbtn",type="secondary",shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
        
    st.markdown("""
                <h2 class="student-rep">Register Your Teacher Profile:</h2>
                    <style>
                    .student-rep{
                        color:black !important;
                        font-weight:25 !important;
                        font-size:1.8rem !important;
                    }
                    </style>
                """,unsafe_allow_html=True)
    st.space()
    teacher_username = st.text_input("Enter Username",placeholder="Anonymous")
    teacher_name = st.text_input("Enter your name",placeholder="John Doe")
    teacher_password = st.text_input("Enter Password",type="password",placeholder="Enter Password")
    teacher_confirm_password = st.text_input("Confirm your Password",type="password",placeholder="Confirm Password")
    st.divider()
    btnc1,btnc2 = st.columns(2)
    
    with btnc1:
        if st.button('Register',width="stretch",shortcut='control+enter',icon=":material/passkey:"):
            success,message = register_teacher(teacher_username,teacher_password,teacher_name,teacher_confirm_password)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message)
        
    with btnc2:
        if st.button('Login Instead',width="stretch",icon=":material/passkey:",type="primary"):
            st.session_state.teacher_login_type='login'
            st.rerun()
    footer_dashboard()