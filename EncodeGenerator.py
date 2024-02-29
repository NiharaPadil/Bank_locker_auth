import cv2
import face_recognition
import pickle
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://bank-locker-authentication-default-rtdb.firebaseio.com/",
    'storageBucket': "bank-locker-authentication.appspot.com"  # Corrected bucket name
})

# Importing the Students images into a list
folderPath = "Images"
pathList = os.listdir(folderPath)
# print(pathList)
imgList = []
StudentsId = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    # print(path)
    # print(os.path.splitext(path)[0])
    StudentsId.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()  # No need to specify the bucket name here
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(StudentsId)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding started...")
encodeListKnown = findEncodings(imgList)
print(encodeListKnown)
encodeListKnownWithID = [encodeListKnown, StudentsId]
print("Encoding Complete")

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithID, file)
file.close()
print("file saved")
