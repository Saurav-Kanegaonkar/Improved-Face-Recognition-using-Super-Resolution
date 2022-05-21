import cv2
import os
# Load the cascade
def roi():
    directory = os.getcwd() +  "/backend/face_images"
    directory.replace("\\","/")
    path = directory
    directory = os.getcwd() +  "/backend/regionOfInterest/haarcascade_frontalface_default.xml"
    directory.replace("\\","/")
    face_cascade = cv2.CascadeClassifier(directory)

    # To capture video from webcam. 
    cap = cv2.VideoCapture(0)
    i = 0

    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        cropped_image = img
        # cropped_image = img
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            # cv2.rectangle(cropped_image, (x, y), (x+w, y+h), (255, 0, 0), 0)
            if i%50 == 0 and len(faces) > 0:
                faces = cropped_image[y-10:y + h + 10, x-10:x + w + 10]
                # cv2.imshow("face", faces)
                name = "face" + str(i) + ".jpg"
                cv2.imwrite(os.path.join(path,name), faces)
        
        i += 1
        # Display
        cv2.imshow('img', cropped_image)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
    # Release the VideoCapture object
    cap.release()
if __name__ == "__main__":
    roi()