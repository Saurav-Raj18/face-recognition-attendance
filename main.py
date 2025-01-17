
import cv2
import face_recognition
import numpy as np
import os
import sqlite3
import csv
from datetime import datetime
from flask import Flask, render_template, Response, jsonify, send_file

app = Flask(__name__)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance(name TEXT, time TEXT, date TEXT)''')
    conn.commit()
    conn.close()

# Load known images and their names
images = []
class_names = []
faces_dir = "images/"

for filename in os.listdir(faces_dir):
    currImg = cv2.imread(f'{faces_dir}/{filename}')
    images.append(currImg)
    class_names.append(os.path.splitext(filename)[0])  # Get the name without extension

# Function to find encodings for all known faces
def findEncodings(images):
    encodeList = []
    for item in images:
        item = cv2.cvtColor(item, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(item)[0]
        encodeList.append(encoding)
    return encodeList

encodeListKnown = findEncodings(images)
print("Encoding Complete!!!!")

# Function to mark attendance and return success message
def markAttendance(name):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    currTime = datetime.now().strftime("%H:%M:%S")
    currDate = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT * FROM attendance WHERE name=?", (name,))
    existingEntry = c.fetchone()
    
    if existingEntry:
        return f"Attendance for {name} already marked."
    else:
        c.execute("INSERT INTO attendance(name, time, date) VALUES(?, ?, ?)", (name, currTime, currDate))
        conn.commit()
        conn.close()
        return f"Attendance for {name} marked successfully!"


def deleteAllEntries():
    # Connect to the SQLite database
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    # SQL command to delete all rows in the table
    c.execute("DELETE FROM attendance")
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

@app.route("/video_feed")
def video_feed():
    def generate():
        video_capture = cv2.VideoCapture(0)  # Open camera
        if not video_capture.isOpened():
            return "Error: Could not access the camera."

        try:
            while True:
                ret, frame = video_capture.read()  # Read frame by frame
                if not ret:
                    break

                # Convert frame from BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for faceLoc, face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
                    faceDis = face_recognition.face_distance(encodeListKnown, face_encoding)
                    matchIndex = np.argmin(faceDis)
                    #print(faceDis)

                    if matches[matchIndex]:
                        name = class_names[matchIndex].upper()
                        #print(name)
                        y1, x2, y2, x1 = faceLoc
                        cv2.rectangle(
                            frame, 
                            (x1, y1),  # Top-left corner
                            (x2, y2),  # Bottom-right corner
                            (255, 0, 0),  # Color (Blue in BGR format)
                            2  # Thickness of the rectangle
                        )
                        # Display name on the face
                        cv2.putText(
                            frame, 
                            name, 
                            (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.9, 
                            (255, 0, 0), 
                            2
                        )

                        # Call markAttendance and get the message
                        attendanceMessage = markAttendance(name)

                # Encode the frame to JPEG
                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    continue

                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        finally:
            video_capture.release()  # Release the camera when done

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

# Route to view attendance
@app.route('/view_attendance')
def view_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    records = c.fetchall()
    conn.close()
    return render_template('view_attendance.html', records=records)

# Route to download attendance
@app.route('/download_attendance')
def download_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    records = c.fetchall()
    conn.close()

    with open('attendance.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Time', 'Date'])
        writer.writerows(records)

    return send_file('attendance.csv', as_attachment=True)

# Main Home Route
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)



















# import cv2
# import face_recognition
# import numpy as np
# import os
# import csv
# from datetime import datetime
# from flask import Flask, render_template, Response, request, jsonify
# import sqlite3

# app=Flask(__name__)

# #set Up SqLite Database
# def init_db():
#     conn=sqlite3.connect('attendance.db')
#     c=conn.cursor()
#     c.execute('''create table if not exists attendace(name text,time text,date text)''') #A cursor is an object in SQLite (and many other database systems) used to interact with the database. It acts as an intermediary between your Python application and the SQLite database. 
#     conn.commit()
#     conn.close()

# # print(app)
# images = []
# class_names = []

# # Directory containing images of people (known faces)
# faces_dir = "images/"

# # Load known images and their names
# for filename in os.listdir(faces_dir):
#     currImg = cv2.imread(f'{faces_dir}/{filename}')
#     images.append(currImg)
#     class_names.append(os.path.splitext(filename)[0])  # Get the name without extension

# # Function to find encodings for all known faces
# def findEncodings(images):
#     encodeList = []
#     for item in images:
#         item = cv2.cvtColor(item, cv2.COLOR_BGR2RGB)
#         encoding = face_recognition.face_encodings(item)[0]
#         encodeList.append(encoding)
#     return encodeList

# encodeListKnown = findEncodings(images)
# print("Encoding Complete!!!!")

# # Function to mark attendance
# def markAttendance(name):
#     # with open('attendance.csv', 'r+') as f:
#     #     # Read all rows from the CSV file
#     #     myDataList = f.readlines()
#     #     nameList = []
        
#     #     for line in myDataList:
#     #         entry = line.split(',')
#     #         nameList.append(entry[0])  # Add the name to the list
            
#     #     # If the name is not already in the list, append it
#     #     if name not in nameList:
#     #         now = datetime.now()
#     #         date_time = now.strftime('%Y-%m-%d %H:%M:%S')
#     #         f.writelines(f'\n{name},{date_time}')
#     conn=sqlite3.connect('attendance.db')
#     c=conn.cursor()
#     currTime=datetime.now().strftime("%H:%M:%S")
#     currDate=datetime.now().strftime("%Y-%m-%d")
#     c.execute("Insert into attendance(name,time,date) values(?,?,?)",(name,currTime,currDate))
#     conn.commit()
#     conn.close()

# # cap = cv2.VideoCapture(0)

# # while True:
# #     # Capture img-by-img
# #     ret, img = cap.read()
# #     if not ret:
# #         print("Failed to grab frame")
# #         break

# #     img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
# #     # Convert the image from BGR to RGB (required by face_recognition)
# #     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# #     # Find faces and encodings in the current frame
# #     facesCurrFrame = face_recognition.face_locations(imgRGB)
# #     encodingCurrFrame = face_recognition.face_encodings(imgRGB, facesCurrFrame)

# #     # Loop through each face found in the current frame
# #     for encodeFace, faceLoc in zip(encodingCurrFrame, facesCurrFrame):
# #         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
# #         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# #         print(faceDis)
# #         matchIndex = np.argmin(faceDis)

# #         if matches[matchIndex]:
# #             name = class_names[matchIndex].upper()
# #             print(name)
# #             y1, x2, y2, x1 = faceLoc
# #             cv2.rectangle(
# #                 img, 
# #                 (x1, y1),  # Top-left corner
# #                 (x2, y2),  # Bottom-right corner
# #                 (255, 0, 0),  # Color (Blue in BGR format)
# #                 2  # Thickness of the rectangle
# #             )
# #             # Display name on the face
# #             cv2.putText(
# #                 img, 
# #                 name, 
# #                 (x1, y1 - 10), 
# #                 cv2.FONT_HERSHEY_SIMPLEX, 
# #                 0.9, 
# #                 (255, 0, 0), 
# #                 2
# #             )

# #             # Mark attendance
# #             markAttendance(name)

# #     # Show the live video stream
# #     cv2.imshow("Webcam", img)

# #     # Exit when the user presses 'q'
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # # Release the video capture and close all OpenCV windows
# # cap.release()
# # cv2.destroyAllWindows()

# # Flask Route for Video Feed
# @app.route("/video_feed")
# def video_feed():
#     def generate():
#         video_capture = cv2.VideoCapture(0)
#         while True:
#             ret, frame = video_capture.read()
#             rgb_frame = frame[:, :, ::-1]  # Convert frame from BGR to RGB
#             face_locations = face_recognition.face_locations(rgb_frame)
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#             for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#                 matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
#                 name = "Unknown"

#                 if True in matches:
#                     first_match_index = matches.index(True)
#                     name = class_names[first_match_index]
#                     markAttendance(name)

#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

#             ret, jpeg = cv2.imencode('.jpg', frame)
#             if not ret:
#                 continue
#             frame = jpeg.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#         video_capture.release()

#     return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

# # Main Home Route
# @app.route('/')
# def index():
#     return render_template("index.html")

# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)





