from keras.models import load_model
import cv2
import numpy as np
import os
import time
import mediapipe as mp
from mediapipe.python.solutions import holistic
mp_drawing=mp.solutions.drawing_utils   #holistic model
mp_holistic=mp.solutions.holistic       #drawing utilities
def mediapipe_detection(image,model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #color conversion BGR to RGB
    image.flags.writeable = False                   #Image is no longer writeable
    results = model.process(image)                  # make prediction
    image.flags.writeable = True                    #image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  #color conversion again RGB to BGR
    return image,results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)  # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)  # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) #Draw right hand connections

def draw_style_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                              mp_drawing.DrawingSpec(color=(175,13,13), thickness=1, circle_radius=1),   #color dot
                              mp_drawing.DrawingSpec(color=(0,0,0), thickness=1, circle_radius=1)    #color line
                              )
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(178,16,16), thickness=2, circle_radius=4),   #color dot
                              mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2)    #color line
                              )
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=1),   #color dot
                              mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2)    #color line
                              )
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=1),   #color dot
                              mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2)    #color line
                              )

def extract_keypoints(results):
    pose = np.array([[res.x,res.y,res.y,res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x,res.y,res.y] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x,res.y,res.y] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x,res.y,res.y] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose,face,lh,rh])
actions=np.array(['Aausadi','Ambulance','Bathroom','Be Careful','Bleeding','Call','Dhanebad','Doctor','Dont Understand','Eklopan',
                  'Emergency','Firstaid','Good Morning','Happy','Heart_attack','Hello','Help','Hospital','Name','Need','Nice To Meet You',
                  'Oxygen','Pain','Please','Police','Relax','Sign','Slowly','Sorry','What','Yes','You'])
# Provide the path to your saved model
model_path = r'C:\Users\Dell\Desktop\New folder\combinebilstm.h5'
# model_path = r'C:\Users\Dell\Downloads\1-7.h5'

# Load the model
loaded_model = load_model(model_path)
sequence = []
sentence = []
predictions = []
threshold = 0.9

cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        # Read feed
        ret, frame = cap.read()
        # make detections
        image, results = mediapipe_detection(frame, holistic)
        print(results)

        # Draw landmarks
        # draw_landmarks(image, results)  # default landmarks in face hand

        draw_style_landmarks(image, results)  # customized landmarks in face and hand

        # prediction logic
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        # sequence.insert(0, keypoints)
        sequence = sequence[-60:]
        
        if len(sequence) == 60:
            res = loaded_model.predict(np.expand_dims(sequence, axis=0))[0]
            # print(actions[np.argmax(res)])
            # print("Confidence values:", res)
            print("Predicted Action:", actions[np.argmax(res)])
            predictions.append(np.argmax(res))

            # visualization logic
            if np.unique(predictions[-20:])[0]==np.argmax(res):
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                        else:
                            sentence.append(actions[np.argmax(res)])

            if len(sentence) > 5:
                sentence = sentence[-5:]

        # viz probabilities
            # image = prob_viz(res,actions,image,colors)

        # image = cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
        image = cv2.putText(image, ' '.join(sentence), (3, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                            cv2.LINE_AA)
        # show to screen
        image = cv2.flip(image, 1)
        cv2.imshow('OPENCV FEED', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
