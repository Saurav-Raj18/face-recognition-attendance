echo "# Face Recognition **Attendance** System

## Description

This project is a Face Recognition **Attendance** System built using Flask, OpenCV, SQLite, and deep learning techniques. It uses the `face_recognition` library (built on top of `dlib`) for facial detection and recognition, marking **attendance** based on facial recognition. The **attendance** data is stored in a local SQLite database.

## Features

- Facial Recognition for **Attendance** (powered by `face_recognition` and `dlib`)
- Real-time Video Feed
- SQLite Database for **Attendance** Storage

## Prerequisites

- Python 3.x
- Flask
- OpenCV
- SQLite
- face_recognition (built on top of dlib)
- dlib

## Installation

1. Clone the repository:

   \`\`\`
   git clone https://github.com/Saurav-Raj18/face-recognition-attendance.git
   \`\`\`

2. Navigate to the project directory:

   \`\`\`
   cd face-recognition-attendance
   \`\`\`

3. Install dependencies:

   \`\`\`
   pip install -r requirements.txt
   \`\`\`

4. Install `dlib` and `face_recognition`:

   \`\`\`
   pip install dlib face_recognition
   \`\`\`

## Usage

1. Run the application:

   \`\`\`
   python main.py
   \`\`\`

2. Access the web application at \`http://localhost:5000/\` or the video feed at \`http://localhost:5000/video_feed\`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Flask Framework
- OpenCV
- SQLite
- `dlib` for facial recognition
- `face_recognition` library for easy-to-use face recognition

> README.md
