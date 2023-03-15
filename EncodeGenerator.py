import cv2
import face_recognition
import pickle
import os
import dlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendacerealtime-8a824-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendacerealtime-8a824.appspot.com"
})

# importing images of person
folderPath = 'Images'
PathList = os.listdir(folderPath)
#print(PathList)
imgList = []
studentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

#print(studentIds)

def findEncodings(ImagesList):
    encodeList = []
    for img in ImagesList:
# Converting Image color BGR TO RGB
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("Encoding started ...")
encodeListknown = findEncodings(imgList)
encodeListknownWithIds = [encodeListknown,studentIds]
#print(encodeListknownWithIds)
print("Encoding complete")

# saving encodings in a pickle file
file = open("EncodeFile.p",'wb')
pickle.dump(encodeListknownWithIds,file)
file.close()
print("File saved")