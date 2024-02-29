import os
import pickle
from datetime import datetime

import numpy as np
import cvzone
import cv2
import face_recognition

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

<<<<<<< HEAD

<<<<<<< HEAD
<<<<<<< HEAD
=======
print("hi Nihara ")
print("hi lima")

>>>>>>> 6af6d12dd3d0c8d8275109854575bc42c11df58d
=======
>>>>>>> 10fc7e37100708f541be4280d25eb624074202de
=======
>>>>>>> nihara
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://bank-locker-authentication-default-rtdb.firebaseio.com/",
    'storageBucket': "bank-locker-authentication.appspot.com"  # Corrected bucket name
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# print(len(imgModeList))

# Load the encoding file
print("Loading encoded file")
file = open("EncodeFile.p", 'rb')
encodeListKnownWithID = pickle.load(file)
file.close()
encodeListKnown, StudentsId = encodeListKnownWithID
# print(StudentsId)
print("Encoding file loaded")

modeType = 0
counter = 0
id = -1
imStudent=[]

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("matchIndex", matchIndex)

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            if matches[matchIndex]:
                print("Known face Detected")
                print(StudentsId[matchIndex])
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0, colorC=(0, 255, 0))
                id = StudentsId[matchIndex]
                print(id)

                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading",(275,400))
                    cv2.imshow("Bank Locker User Identification", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                #Get the Data
                studentsInfo = db.reference(f"Auth_ppl/{id}").get()
                print(studentsInfo)

                #Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                #Update the data of login
                datetimeObject = datetime.strptime(studentsInfo['last_login'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed= (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)

                if secondsElapsed>30:

                    ref = db.reference(f'Auth_ppl/{id}')
                    studentsInfo['tot_login']+=1
                    ref.child('tot_login').set(studentsInfo['tot_login'])
                    ref.child('last_login').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modeType=3
                    counter=0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType!=3:

                if 10<counter<20:
                    modeType = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


                if counter<=10:


                    cv2.putText(imgBackground, str(studentsInfo['tot_login']), (861, 125),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                    # cv2.putText(imgBackground, str(studentsInfo['last_login']), (910, 625),
                    #            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentsInfo['Acc_num']), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    (w, h), _ = cv2.getTextSize(studentsInfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentsInfo['Name']), (808 + offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imStudent_resized = cv2.resize(imStudent, (216, 216))
                    imgBackground[175:175 + 216, 909:909 + 216] = imStudent_resized

            counter += 1
            if counter>=20:
                counter=0
                modeType=0
                studentsInfo=[]
                imStudent=[]
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType=0
        counter=0

    #cv2.imshow("Webcam", img)
    cv2.imshow("Bank Locker User Identification", imgBackground)

    #ESC key ,shut down window
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()