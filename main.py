import cv2
import face_recognition
import numpy as np
import os
import csv
from datetime import datetime

images = []
class_names = []

# Directory containing images of people (known faces)
faces_dir = "images/"

# Load known images and their names
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

# Function to mark attendance
def markAttendance(name):
    with open('attendance.csv', 'r+') as f:
        # Read all rows from the CSV file
        myDataList = f.readlines()
        nameList = []
        
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])  # Add the name to the list
            
        # If the name is not already in the list, append it
        if name not in nameList:
            now = datetime.now()
            date_time = now.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'\n{name},{date_time}')

cap = cv2.VideoCapture(0)

while True:
    # Capture img-by-img
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    # Convert the image from BGR to RGB (required by face_recognition)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Find faces and encodings in the current frame
    facesCurrFrame = face_recognition.face_locations(imgRGB)
    encodingCurrFrame = face_recognition.face_encodings(imgRGB, facesCurrFrame)

    # Loop through each face found in the current frame
    for encodeFace, faceLoc in zip(encodingCurrFrame, facesCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = class_names[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            cv2.rectangle(
                img, 
                (x1, y1),  # Top-left corner
                (x2, y2),  # Bottom-right corner
                (255, 0, 0),  # Color (Blue in BGR format)
                2  # Thickness of the rectangle
            )
            # Display name on the face
            cv2.putText(
                img, 
                name, 
                (x1, y1 - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.9, 
                (255, 0, 0), 
                2
            )

            # Mark attendance
            markAttendance(name)

    # Show the live video stream
    cv2.imshow("Webcam", img)

    # Exit when the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
