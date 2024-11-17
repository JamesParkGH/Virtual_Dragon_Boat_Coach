import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

from calc_angle import *

class PoseEstimation:
    def __init__(self,video_name):
        self.model = YOLO('yolov8n-pose.pt')
        self.active_keypoints = [5,7,9]
        self.video_path = video_name
        self.scale = 1/2
        current_fps = 30
        desired_fps = 10
        self.skip_factor = current_fps // desired_fps

    def analyze_pose(self,show_angle=False):
        if show_angle:
            plt.ion()
            fig, ax = plt.subplots()
            angle = 0
            angles = []
            time = []

        frame_count = 0
        frame_arm_only = 126
        color = (255,255,0)

        cv2.namedWindow("Keypoints", cv2.WINDOW_NORMAL)
        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            # if frame_count % self.skip_factor != 0:
            #     continue

            # height, width, _ = frame.shape
            # window_width = int(frame.shape[1]* self.scale)
            # window_height = int(frame.shape[0]* self.scale)
            # cv2.resizeWindow("KeyPoints", window_width, window_height)

            results = self.model(frame)
            keypoints = results[0].keypoints.xy.cpu().numpy()[0]

            ## Draw points
            for i in range(len(self.active_keypoints)-1):
                pt1 = tuple(keypoints[self.active_keypoints[i]].astype(int))
                pt2 = tuple(keypoints[self.active_keypoints[i+1]].astype(int))
                cv2.line(frame, pt1, pt2, color, 3)
                cv2.circle(frame, pt1, 5, color, -1)

            if show_angle:
                angle = calculate_angle(keypoints[self.active_keypoints[0]],keypoints[self.active_keypoints[1]],keypoints[self.active_keypoints[2]])
                cv2.putText(frame, f"{round(angle)}", (270,1500), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5, cv2.LINE_AA)

                angles.append(angle)
                time.append(frame_count)
                ax.plot(time, angles, marker='o', color="blue")
                plt.xlabel('Time')
                plt.ylabel('Angle')
                plt.title('Angle vs. Time')
                plt.draw()
                plt.pause(.05)
        
            cv2.imshow("KeyPoints", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()



def run_analyze_pose(show_angle):
    estimation = PoseEstimation('test_paddle3.mp4')
    estimation.analyze_pose(show_angle=show_angle)

if __name__ == '__main__':
    run_analyze_pose(show_angle=True)