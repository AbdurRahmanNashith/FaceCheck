import os
import pickle
import cvzone
import cv2
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    #'databaseURL':"Enter Storage URL here",
    #'storageBucket': "Enter RealTime URL here"
})



cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# importing modes from resources directory into a list
folderModePath = 'Resources/Modes'
modePathList = sorted(os.listdir(folderModePath))
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))




#print(len(imgModeList))


# Load the encodings file
print("Loading Encode file ...")
file = open('EncodeFile.p','rb')
encodeListknownWithIds = pickle.load(file)
file.close()
encodeListknown,studentId = encodeListknownWithIds
# print(studentId)
print("Encode file loaded")

modeType = 0
counter = 0


while True:
    success, img = cap.read()

# Size scale Down
    imgS = cv2.resize(img,( 0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162 +480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

# Face Matching and Displaying their Index
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListknown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListknown, encodeFace)
        # print("matches", matches)
        # print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        # print("matchIndex", matchIndex)

        if matches[matchIndex]:
           # print("Known Face Detected")
           # print(studentId[matchIndex])
           y1, x2, y2, x1 = faceLoc
           y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
           bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
           imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
           id = studentId[matchIndex]







    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)




