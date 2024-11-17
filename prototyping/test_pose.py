import cv2
import mediapipe as mp
import numpy as np

from calc_angle import *

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
video_path = "test_paddle2.mp4"

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(video_path)

if cap.isOpened() == False:
    print("Error opening video stream or file")
    raise TypeError

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

outdir = "C:\\Users\\iainj\\Documents\\McMaster\\Lvl 5\\SFWRBME 5P06\\Capstone\\Testing"
inputflnm = "test_paddle2.mp4"

inflnm, inflext = inputflnm.split('.')
out_filename = f'{outdir}{inflnm}_annotated.{inflext}'
out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))


## Array for tracking landmarks
wrist1_positions = []
wrist2_positions = []

canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    
    ## Track positions
    try:
        landmarks = results.pose_landmarks.landmark

        ## Left
        wrist1 = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        elbow1 = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        shoulder1 = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]


        ## Right
        wrist2 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        elbow2 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        shoulder2 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        elbow1_angle = calculate_angle(wrist1, elbow1, shoulder1)
        elbow2_angle = calculate_angle(wrist2, elbow2, shoulder2)

        cv2.putText(image, str(elbow1_angle), tuple(np.multiply(elbow1, [640,480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AAA)

        print(landmarks)

    except:
        pass

    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # ## Top hand
    # wrist1_x = int(wrist1.x * image.shape[1])
    # wrist1_y = int(wrist1.y * image.shape[0])

    # wrist1_positions.append((wrist1_x, wrist1_y))

    # ## Bottom hand
    # wrist2_x = int(wrist2.x * image.shape[1])
    # wrist2_y = int(wrist2.y * image.shape[0])

    # wrist2_positions.append((wrist2_x, wrist2_y))

    # for i in range(1,len(wrist1_positions)):
    #     cv2.line(image, wrist1_positions[i-1], wrist1_positions[i], (0,255,0), 2)
    #     cv2.line(canvas, wrist1_positions[i-1], wrist1_positions[i], (0,255,0), 2)
    # for i in range(1,len(wrist2_positions)):
    #     cv2.line(image, wrist2_positions[i-1], wrist2_positions[i], (255,0,0), 2)
    #     cv2.line(canvas, wrist2_positions[i-1], wrist2_positions[i], (255,0,0), 2)
    
    cv2.imshow('Test Pose Detect', cv2.flip(image, 2))
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break
    out.write(image)

cv2.imwrite("wrist_paths2.png", canvas)
pose.close()
cap.release()
out.release()
