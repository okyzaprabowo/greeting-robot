import face_recognition
import cv2
import numpy as np
from gtts import gTTS
import os
import subprocess
import threading

def greeting():
    os.system('afplay nama.mp3')

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
image = []
encoding_image = []

for
# okyza_image = face_recognition.load_image_file("img/biru.jpg")
# okyza_face_encoding = face_recognition.face_encodings(okyza_image)[0]

yuyun_image = face_recognition.load_image_file("img/bu-yuyun.png")
yuyun_face_encoding = face_recognition.face_encodings(yuyun_image)[0]

ksas_image = face_recognition.load_image_file("img/kyai_said_aqil_siradj.jpg")
ksas_face_encoding = face_recognition.face_encodings(ksas_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    # okyza_face_encoding,
    yuyun_face_encoding,
    ksas_face_encoding 
]
known_face_names = [
    # "Okyza",
    "Yuyun",
    "Kyai Said"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
yuyun = 0
okyza = 0
tamu = 0
ksas = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Tamu"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            if(name=='Tamu'):
                if(tamu==0):
                    text = 'Assalamualaikum Tamu STMIK Amik Bandung'
                    tts = gTTS(text, 'id')
                    tts.save('nama.mp3')
                    # thread1 = threading.Thread(target = greeting)
                    # thread1.start()
                    # p = subprocess.Popen(["afplay ", "nama.mp3"], stdout=subprocess.PIPE, shell=True)
                    os.system('afplay tamu.mp3')
                    tamu = tamu + 1
                    print(tamu)
            elif(name=='Kyai Said Aqil Siroj'): 
                if(ksas==0):
                    text = 'Assalamualaikum ' + name
                    tts = gTTS(text, 'id')
                    # tts.save('nama.mp3')
                    # thread1 = threading.Thread(target = greeting)
                    # thread1.start()
                    # os.system('afplay nama.mp3')
                    ksas = ksas + 1
                    print("Kyai Said Aqil Siradj ", ksas)
            # elif(name=='Yuyun'):
            #     if(yuyun==0):
            #         # text = 'Assalamualaikum ' + name
            #         # tts = gTTS(text, 'id')
            #         # tts.save('nama.mp3')
            #         # thread1 = threading.Thread(target = greeting)
            #         # thread1.start()
            #         # os.system('afplay nama.mp3')
            #         yuyun = yuyun + 1
            #         print("yuyun ", yuyun)
            # elif(name=='Okyza'): 
            #     if(okyza==0):
            #         text = 'Assalamualaikum ' + name
            #         tts = gTTS(text, 'id')
            #         tts.save('nama.mp3')
            #         # thread1 = threading.Thread(target = greeting)
            #         # thread1.start()
            #         # p = subprocess.Popen(["afplay ", "nama.mp3"], stdout=subprocess.PIPE, shell=True)
            #         # os.system('afplay nama.mp3')
            #         okyza = okyza + 1
            #         print("okyza ", okyza)
            

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()