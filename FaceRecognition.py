import face_recognition
import cv2
import numpy as np
import pickle

from Database import Database
from Customer import Customer


class FaceRecognition:
    def __init__(self, ip_camera=None):
        # self.known_faces = known_faces
        # self.known_names = known_names
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.db = Database("spxcafecopy.db")
        self.__test = ""



        if ip_camera:
            self.video_capture = cv2.VideoCapture(ip_camera)
        else:
            self.video_capture = cv2.VideoCapture(0)

        self.known_faces = []
        self.known_names = []


    def reset(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.known_names = []
        self.known_faces = []
        self.process_this_frame = True


    def recognize_faces(self, customerIds=None):
        if customerIds is None:
            customerIds = Customer.getAllCustomerIds()

        self.reset()
        self.load_known_faces(customerIds)
        

        frame_count = 0  # Add a frame counter
        process_every_N_frames = 5  # Change this to process fewer or more frames


        while True:
            for _ in range(5):
                self.video_capture.read()

            ret, frame = self.video_capture.read()

            if ret and frame_count % process_every_N_frames == 0:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]

                self.face_locations = face_recognition.face_locations(small_frame)
                self.face_encodings = face_recognition.face_encodings(small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_faces, face_encoding, tolerance=0.4)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(self.known_faces, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]

                    self.face_names.append(name)

            frame_count += 1

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, str(name), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if ret:
                cv2.imshow('Video', frame)

            if self.face_names:
                # print(self.face_names[0])
                self.video_capture.release()
                cv2.destroyAllWindows()
                return self.face_names[0]

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()

    def load_known_faces(self, customerIds):
        for customerId in customerIds:
            sql = f"""
            SELECT
                face
            FROM
                customers
            WHERE
                customerId = {customerId}
            """
            result = self.db.dbGetData(sql)
            # print(result)
            if result is not None:
                face_blob = result[0]['face']
                face = pickle.loads(face_blob)
                # face_encoding = face_recognition.face_encodings(face)[0]  # Get the face encoding
                self.known_faces.append(face)
                self.known_names.append(customerId)

        print(self.known_names)

    def __capture_face(self):
        while True:
            ret, frame = self.video_capture.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)

            for (top, right, bottom, left) in face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                return frame, (top, right, bottom, left)  # Return the entire frame and the face's location

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




    def add_face(self, customerId):
        print("Adding face...")
        face, face_locations = self.__capture_face()

        face_encoding = face_recognition.face_encodings(face, [face_locations])[0]

        face_blob = pickle.dumps(face_encoding)
        conn = self.db.dbConnect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE customers SET face = ? WHERE customerId = ?", (face_blob, customerId))
            conn.commit()
            conn.close()

        self.video_capture.release()
        cv2.destroyAllWindows()





    def repeat_recognise(self, customerIds=None, maximum=10):
        if customerIds is None:
            customerIds = Customer.getAllCustomerIds()
        for _ in range(maximum):
            print(_)
            self.video_capture = None
            self.video_capture = cv2.VideoCapture(0)
            id = self.recognize_faces(customerIds)
            if id != "Unknown":
                return id
        return None


def main():
    # face_recog = FaceRecognition(ip_camera="http://192.168.1.11:8080/video")
    face_recog = FaceRecognition()

    # face = face_recog.recognize_faces([7])
    # face_recog.add_face(2)
    # id = face_recog.recognize_faces([7])
    a = input()
    id = face_recog.repeat_recognise([2])
    print("Found face")
    print(id)



if __name__ == "__main__":
    main()
