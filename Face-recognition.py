import face_recognition
import cv2
import csv
import time
from gtts import gTTS
import os

video_capture = cv2.VideoCapture(0)
##video_capture = cv2.flip(video_capture, 0)
#f1_image = face_recognition.load_image_file("sana.jpg")
#f1_face_encoding = face_recognition.face_encodings(f1_image)[0]
f2_image = face_recognition.load_image_file("san.jpg")
f2_face_encoding = face_recognition.face_encodings(f2_image)[0]
f3_image = face_recognition.load_image_file("Dhanu.jpg")
f3_face_encoding = face_recognition.face_encodings(f3_image)[0]

known_face_encodings = [
    #f1_face_encoding,  
    f2_face_encoding,
    f3_face_encoding,
]
known_face_names = [
    #"sana",  
    "sandy",
    "Dhanu",
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
pre_name = "xyz"


list = []

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
   
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                
            face_names.append(name)
            
            if(name != pre_name):
                if(name not in list):
                    print(name)
                    td = time.strftime("%c")
                    with open ('Attendance.csv','a') as fl :
                        writer = csv.writer(fl, delimiter = ',',lineterminator = '\n')
                        writer.writerow([name,td])
                    print(name,td)
                    list.append(name)
                pre_name = name

    process_this_frame = not process_this_frame
    
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
fl.close()
