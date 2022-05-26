import face_recognition as fr
import face_recognition
import pickle
import os
import cv2
import numpy as np
from time import sleep
import json


def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}
    directory = os.getcwd() +  "/backend/face_rec/faces"
    directory.replace("\\","/")
    for dirpath, dnames, fnames in os.walk(directory):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                print(f)
                face = fr.load_image_file(directory + "/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    directory = os.getcwd() +  "/backend/face_rec/faces/"
    directory.replace("\\","/")
    face = fr.load_image_file(directory + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im, faces):
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    #faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    #img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #img = img[:,:,::-1]
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
        '''
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)
        '''

    # Display the resulting image
    '''
    while True:

        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names 
    '''
    print(face_names, im)
    return face_names


def face_rec():
    
    # faces = get_encoded_faces()
    # my_encodings = open('my_encodings','wb')
    # pickle.dump(faces,my_encodings)

    # directory = os.getcwd() +  "/backend/face_rec/inputs"
    # directory.replace("\\","/")
    # my_faces = []
    # for item in os.listdir(directory):
    #     input_dir = directory + "/"
    #     my_faces += classify_face(input_dir+item)
    # attendance_record = dict()

    # directory = os.getcwd() +  "/backend/face_rec/faces"
    # directory.replace("\\","/")
    # for name in os.listdir(directory):
    #     attendance_record[name[0:-4]] = False

    # for name in my_faces:
    #     attendance_record[name] = True

    # print(attendance_record)
    # return json.dumps(attendance_record)
    my_faces = []
    count = 0
    '''
    faces = get_encoded_faces()
    my_encodings = open('my_encodings', 'wb')
    pickle.dump(faces, my_encodings)
    '''
    my_encodings = open('my_encodings', 'rb')
    faces = pickle.load(my_encodings)
    my_encodings.close()
    
    directory = os.getcwd() +  "/backend/face_rec/inputs"
    directory.replace("\\","/")
    for item in os.listdir(directory):
        input_dir = directory + "/"
        curr_face = classify_face(input_dir+item,faces)
        if(len(curr_face) >0 and curr_face[0][0:-4] == item[0:-8]):
            print("correct!")
            count += 1
        my_faces += curr_face
        
    attendance_record = dict()
    attendance_record['Unknown'] = False
    attendance_record_count = dict()
    attendance_record_count['Unknown'] = 0

    directory = os.getcwd() +  "/backend/face_rec/faces"
    directory.replace("\\","/")
    for name in os.listdir(directory):
        attendance_record[name[0:-4]] = False
        attendance_record_count[name[0:-4]] = 0
    my_faces_dict = set()
    for name in my_faces:
        my_faces_dict.add(name)
    for name in my_faces:
        #print(name)
        if(attendance_record_count[name] > 5 or name == 'Unknown'):
            continue
        attendance_record_count[name] += 2
        print(name,attendance_record_count[name])
        if(attendance_record_count[name] > 3):
            attendance_record[name] = True

        for name2 in my_faces_dict:
            attendance_record_count[name2] = max(attendance_record_count[name2]-1,0)
    print(attendance_record)
    print(count)
    return json.dumps(attendance_record)

