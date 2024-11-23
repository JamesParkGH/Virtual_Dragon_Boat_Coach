import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

from calc_angle import *

class PoseEstimation:
    def __init__(self,video_name):
        self.model = YOLO('yolov8n-pose.pt')
        self.bottom_arm_keypoints = [6,8,10]
        self.hinge_keypoints = [6,12,14]
        self.spine_keypoints = [4,6,12]
        self.video_path = video_name
        self.scale = 1/2
        current_fps = 30
        desired_fps = 10
        self.skip_factor = current_fps // desired_fps

    def analyze_pose(self,show_angle=False):
        if show_angle:
            plt.ion()
            fig, axs = plt.subplots(2,2)
            bottom_elbow_angle = 0
            hinge_angle = 0
            spine_angle = 0
            bottom_elbow_angles = []
            hinge_angles = []
            spine_angles = []
            time = []

        frame_count = 0
        frame_arm_only = 126
        color1 = (255,255,0)
        color2 = (255,0,255)
        color3 = (0,0,255)

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
            ## Edit for drawing distinct lines
            for i in range(len(self.bottom_arm_keypoints)-1):
                pt1 = tuple(keypoints[self.bottom_arm_keypoints[i]].astype(int))
                pt2 = tuple(keypoints[self.bottom_arm_keypoints[i+1]].astype(int))
                cv2.line(frame, pt1, pt2, color1, 3)
                cv2.circle(frame, pt1, 5, color1, -1)
            
            for i in range(len(self.hinge_keypoints)-1):
                pt1 = tuple(keypoints[self.hinge_keypoints[i]].astype(int))
                pt2 = tuple(keypoints[self.hinge_keypoints[i+1]].astype(int))
                cv2.line(frame, pt1, pt2, color2, 3)
                cv2.circle(frame, pt1, 5, color2, -1)

            for i in range(1):
                pt1 = tuple(keypoints[self.spine_keypoints[i]].astype(int))
                pt2 = tuple(keypoints[self.spine_keypoints[i+1]].astype(int))
                cv2.line(frame, pt1, pt2, color3, 3)
                cv2.circle(frame, pt1, 5, color3, -1)

            if show_angle:
                bottom_elbow_angle = calculate_angle(keypoints[self.bottom_arm_keypoints[0]],keypoints[self.bottom_arm_keypoints[1]],keypoints[self.bottom_arm_keypoints[2]])
                hinge_angle = calculate_angle(keypoints[self.hinge_keypoints[0]],keypoints[self.hinge_keypoints[1]],keypoints[self.hinge_keypoints[2]])
                spine_angle = calculate_angle(keypoints[self.spine_keypoints[0]],keypoints[self.spine_keypoints[1]],keypoints[self.spine_keypoints[2]])
                # cv2.putText(frame, f"{round(bottom_elbow_angle)}", (270,1500), cv2.FONT_HERSHEY_SIMPLEX, 5, color1, 5, cv2.LINE_AA)
                # cv2.putText(frame, f"{round(hinge_angle)}", (270,1500), cv2.FONT_HERSHEY_SIMPLEX, 5, color2, 5, cv2.LINE_AA)

                bottom_elbow_angles.append(bottom_elbow_angle)
                hinge_angles.append(hinge_angle)
                spine_angles.append(spine_angle)
                time.append(frame_count)
                ## Elbow plot
                axs[0,0].plot(time, bottom_elbow_angles, color="blue")
                axs[0,0].axhline(y = 150, color = 'cyan', linestyle = '-')
                axs[0,0].axhline(y = 110, color = 'cyan', linestyle = '-')

                ## Hinge plot
                axs[0,1].plot(time, hinge_angles, color="orange")
                axs[0,1].axhline(y = 80, color = 'r', linestyle = '-')

                ## Spine/Neck plot
                axs[1,0].plot(time, spine_angles, color="magenta")
                axs[1,0].axhline(y = 120, color = 'r', linestyle = '-')

                
                # plt.axhline(y = 150, color = 'cyan', linestyle = '-')
                # plt.axhline(y = 110, color = 'cyan', linestyle = '-')
                # plt.xlabel('Time')
                # plt.ylabel('Angle')
                # plt.title('Angle vs. Time')
                plt.draw()
                plt.pause(.05)
        
            cv2.imshow("KeyPoints", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        plt.ioff()
        axs[0,0].plot(time, bottom_elbow_angles, color="blue", label="Elbow angle")
        axs[0,0].axhline(y = 150, color = 'cyan', linestyle = '-')
        axs[0,0].axhline(y = 110, color = 'cyan', linestyle = '-')
        axs[0,0].set_title("Elbow Angle vs. Time")


        ## Hinge plot
        axs[0,1].plot(time, hinge_angles, color="orange", label="Hinge angle")
        axs[0,1].axhline(y = 80, color = 'r', linestyle = '-')
        axs[0,1].set_title("Hinge Angle vs. Time")

        ## Spine/Neck plot
        axs[1,0].plot(time, spine_angles, color="magenta", label="Neck angle")
        axs[1,0].axhline(y = 120, color = 'r', linestyle = '-')
        axs[1,0].set_title("Neck Angle vs. Time")

        # plt.xlabel('Time')
        # plt.ylabel('Angle')
        # plt.title('Angles vs. Time')
        # plt.legend()
        plt.show()

        cap.release()
        cv2.destroyAllWindows()



def run_analyze_pose(show_angle):
    estimation = PoseEstimation('test_paddle8.mp4')
    estimation.analyze_pose(show_angle=show_angle)

if __name__ == '__main__':
    run_analyze_pose(show_angle=True)