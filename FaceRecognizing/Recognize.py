import face_recognition
import cv2
from threading import Thread
from time import sleep
import numpy as np
import os

haarcascades_path = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(haarcascades_path)

# Global
players_faces = []
players_names = []

players = {}

frame_thickness = 3
font_thickness = 2
tolerance = 0.6
green = [0, 255, 0]
blue = [255, 0, 0]
red = [0, 0, 255]

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255,255,255)
lineType = 2

class Player:
    def __init__(self, img, name):
        self.recording = False
        self.name = name
        self.img = face_recognition.load_image_file(img)
        self.face = face_recognition.face_encodings(self.img)[0]
        self.face_bounding_boxes = face_recognition.face_locations(self.img)

        self.SaveFace()

    def SaveFace(self):
        if len(self.face_bounding_boxes) > 1 or len(self.face_bounding_boxes) < 1:
            quit('Please choose a picture with only one face')

        players_names.append(self.name)
        players_faces.append(self.face)

    def DrawFrame(self, color, text, face_location):
        # Draw rect around known face
        self.top_left = (face_location[3], face_location[0])
        self.bottom_right = (face_location[1], face_location[2])

        cv2.rectangle(self.frame, self.top_left, self.bottom_right, color, frame_thickness)

        # Draw name in beneath of known face
        self.top_left = (face_location[3], face_location[2])
        self.bottom_right = (face_location[1], face_location[2] + 22)

        cv2.rectangle(self.frame, self.top_left, self.bottom_right, color, cv2.FILLED)

        cv2.putText(self.frame, text, (face_location[3] + 10, face_location[2] + 15), font, fontScale, fontColor, lineType)

    def IsPlayer(self):
        self.location_face = face_recognition.face_locations(self.frame)
        self.encoding = face_recognition.face_encodings(self.frame, self.location_face)
        #self.faces = face_cascade.detectMultiScale(self.gray, 1.1, 4)

        for self.face_encoding, self.face_location in zip(self.encoding, self.location_face):
            self.results = face_recognition.compare_faces(players_faces, self.face_encoding, tolerance)
            self.isme = face_recognition.compare_faces([self.face], self.face_encoding, tolerance)
            self.match = None

            if True in self.results and self.isme == [False]:
                self.match = players_names[self.results.index(True)]

                self.DrawFrame(green, str(self.match), self.face_location)

            elif True in self.results and self.isme == [True]:
                self.match = players_names[self.results.index(True)]

                self.DrawFrame(red, str(self.match), self.face_location)

            else:
                self.DrawFrame(blue, 'Unknown', self.face_location)

    def LiveFace(self):
        self.cam = cv2.VideoCapture(0)

        self.recording = True

        while self.recording:
            # Read the frame
            self._, self.frame = self.cam.read()

            # Convert to grayscale
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # Detect the faces
            self.IsPlayer()

            # Display
            cv2.imshow('frame', self.frame)

            # Stop if escape key is pressed
            self.key = cv2.waitKey(1) & 0xff
            if self.key == 27:
                break
        self.cam.release()
        cv2.destroyAllWindows()

    def __del__(self):
        # Release the VideoCapture object
        print('Finished')

def CreateNew(player_img, player_name):
    try:
        name_p = ('player' + str(len(players_names) + 1))
        players[name_p] = Player(player_img, player_name)

    except:
        print('Looks like something went wrong, maybe try another picture.')

name = 'Me'
path = 'path to image'
CreateNew(path, name)

players.get('player1').LiveFace()
