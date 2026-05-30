# Classync

Classync is an AI-powered attendance management platform that automates classroom attendance using Face Recognition and Voice Recognition. It eliminates traditional roll calls by allowing students to register biometric profiles and enabling teachers to mark attendance through classroom photos or voice recordings.

Built with Streamlit, Supabase, Dlib, and Resemblyzer, Classync provides a modern, cloud-based solution for educational institutions looking to make attendance management smarter, faster, and more reliable.

---

## Features

### Student Portal
- Face-based registration and login
- Voice profile registration
- Biometric authentication
- Subject enrollment using course codes
- View enrolled subjects
- Unenroll from courses

### Teacher Portal
- Secure login system
- Create and manage subjects
- Share subject enrollment codes
- View attendance records
- Manage student enrollments

### Face Attendance
- Automatic face detection
- Face embedding generation using Dlib
- AI-based student recognition
- Multi-student attendance detection from classroom photos
- Attendance preview before saving

### Voice Attendance
- Voice embedding generation using Resemblyzer
- Speaker recognition from classroom recordings
- Automatic attendance detection
- Attendance confirmation workflow

### Attendance Management
- Subject-wise attendance tracking
- Cloud-based attendance storage
- Attendance preview and verification
- Historical attendance records

---

## Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Database
- Supabase

### Machine Learning
- Dlib
- face_recognition_models
- Scikit-Learn
- Resemblyzer

### Audio Processing
- Librosa
- Soundfile

### Security
- Bcrypt

### Utilities
- Pillow
- Segno

---

## How It Works

### Student Registration

1. Student captures a face image.
2. Face embeddings are generated and stored.
3. Student records a voice sample.
4. Voice embeddings are generated and stored.
5. Student can now log in using Face ID and participate in voice attendance.

### Face Attendance Workflow

1. Teacher uploads a classroom image.
2. Faces are detected automatically.
3. Face embeddings are generated.
4. Stored student embeddings are compared.
5. Attendance preview is displayed.
6. Teacher confirms and saves attendance.

### Voice Attendance Workflow

1. Teacher records classroom audio.
2. Audio is processed using Resemblyzer.
3. Speaker embeddings are extracted.
4. Student voice profiles are matched.
5. Attendance preview is displayed.
6. Teacher confirms and saves attendance.

---

## Project Structure

```text
Classync
│
├── app.py
│
├── src
│   │
│   ├── components
│   │   ├── dialog_add_photo.py
│   │   ├── dialog_voice_attendance.py
│   │   ├── dialog_create_subject.py
│   │   ├── dialog_attendance_results.py
│   │   ├── dialog_enroll.py
│   │   └── subject_card.py
│   │
│   ├── database
│   │   ├── config.py
│   │   └── db.py
│   │
│   ├── pipelines
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   │
│   ├── screens
│   │   ├── home_screen.py
│   │   ├── student_screen.py
│   │   └── teacher_screen.py
│   │
│   └── ui
│       └── base_layout.py
│
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/wamanvinit3817/Classync.git

cd Classync
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Supabase

Create a file:

```text
.streamlit/secrets.toml
```

Add your credentials:

```toml
SUPABASE_URL = "YOUR_SUPABASE_URL"

SUPABASE_KEY = "YOUR_SUPABASE_KEY"
```

---

## Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## Database Tables

### teachers

| Column | Description |
|----------|-------------|
| teacher_id | Unique teacher ID |
| username | Login username |
| password | Hashed password |
| name | Teacher name |

### students

| Column | Description |
|----------|-------------|
| student_id | Unique student ID |
| name | Student name |
| face_embedding | Face vector |
| voice_embedding | Voice vector |

### subjects

| Column | Description |
|----------|-------------|
| subject_id | Subject ID |
| name | Subject name |
| subject_code | Enrollment code |
| section | Section |
| teacher_id | Owner teacher |

### subject_students

| Column | Description |
|----------|-------------|
| subject_id | Subject ID |
| student_id | Student ID |

### attendance_logs

| Column | Description |
|----------|-------------|
| attendance_id | Attendance record |
| student_id | Student ID |
| subject_id | Subject ID |
| timestamp | Attendance time |
| is_present | Attendance status |

---

## Future Improvements

- Liveness detection
- Anti-spoofing protection
- Attendance analytics dashboard
- Attendance percentage tracking
- Parent portal
- Mobile application
- Multi-camera attendance
- Real-time classroom monitoring
- Attendance reports and exports

---

## Why Classync?

Traditional attendance systems consume valuable classroom time and are prone to human error. Classync combines Artificial Intelligence, Face Recognition, Voice Recognition, and Cloud Computing to provide a seamless attendance experience for both students and teachers.

By leveraging biometric verification and automated record management, Classync makes attendance faster, smarter, and more reliable.

---

## Author

**Vineet Waman**

Classync was developed as a full-stack AI-powered attendance management platform integrating Machine Learning, Computer Vision, Voice Biometrics, Cloud Databases, and Modern Web Technologies to automate classroom attendance in an efficient and scalable manner.

---

## License

This project is intended for educational, research, and learning purposes. Feel free to use, modify, and build upon it with proper attribution.
