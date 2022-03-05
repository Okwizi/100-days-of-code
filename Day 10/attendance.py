# Import dependencies
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'images'  # Images' folder name
images = []  # List for all images
allNames = []  # List of names of images
imgPath = os.listdir(path)   # Show images in folder 'images'
print("All photos accounted for...")

# for loop to extract name string from images
for cl in imgPath:
    current = cv2.imread(f'{path}/{cl}')
    images.append(current)
    allNames.append(os.path.splitext(cl)[0])
print("Photo names generated...")


# Encoder function to encode images (face recognition)
def encoder(photos):
    encode_list = []
    for image in photos:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(image)[0]
        encode_list.append(encoding)
    return encode_list


# Compile accepted images into a new list 'chosen'
# !! If an image is not in the compiled list, then image was rejected by the encoder function above
chosen = encoder(images)


# Attendance marking function into csv file
def attendance(names):
    with open('attendance.csv', 'r+') as f:
        name_list = []
        data_list = f.readlines()
        print(data_list)
        for line in data_list:
            entry = line.split(',')
            name_list.append(entry[0])
        if names not in name_list:
            now = datetime.now()
            date = now.strftime('%H: %M: %S')
            f.writelines(f'\n{names}, {date}')


# Camera setup
print("Starting Camera...")
print("!! Press 'q' to close the camera...")
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()

    # Camera frame resize
    img = img[120:120 + 400, 120:120 + 400, :]

    # Image resizing
    photo = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)

    # Locations for face
    faceCurrent = face_recognition.face_locations(photo)
    encodeCurrent = face_recognition.face_encodings(photo, faceCurrent)

    # Rectangle and name set up on recognition
    for encodeFace, face in zip(encodeCurrent, faceCurrent):
        match = face_recognition.compare_faces(chosen, encodeFace)
        distance = face_recognition.face_distance(chosen, encodeFace)
        matchIndex = np.argmin(distance)
        print(distance)

        if match[matchIndex]:
            name = allNames[matchIndex].upper()
            print(name)
            y1, y2, x1, x2 = face
            y1, y2, x1, x2 = y1*4, y2*4, x1*4, x2*4
            # Colors are in GBR format
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 102, 51), 1)
            cv2.rectangle(img, (x1, y2-20), (x2, y2), (255, 102, 51), cv2.FILLED)
            cv2.putText(img, name, (x1-160, y2+7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (225, 204, 102), 2)

            # Mark attendance using attendance function
            attendance(name)
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

print("Attendance marked :))")
