# pip install ultralytics
import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

from calc_angle import *
from download_video import *

class PoseEstimation:
    def __init__(self,video_name):
        self.model = YOLO('yolov8n-pose.pt')
        self.bottom_arm_keypoints = [5,7,9]
        self.hinge_keypoints = [5,11,13]
        self.spine_keypoints = [3,5,11]
        self.video_path = video_name
        self.scale = 1/2
        current_fps = 30
        desired_fps = 10
        self.skip_factor = current_fps // desired_fps

    def analyze_pose(self, show_angle=False):
        if show_angle:
            plt.ion()
            fig, axs = plt.subplots(2, 2)
            fig.suptitle("Angle Plot After Applying Gaussian Filter", fontsize=16)
            bottom_elbow_angles = []
            hinge_angles = []
            spine_angles = []
            time = []

        frame_count = 0
        color1 = (255, 255, 0)
        color2 = (255, 0, 255)
        color3 = (0, 0, 255)

        cv2.namedWindow("Keypoints", cv2.WINDOW_NORMAL)
        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % self.skip_factor != 0:
                continue

            results = self.model(frame)
            keypoints = results[0].keypoints.xy.cpu().numpy()[0]

            # Draw keypoints and lines
            for i in range(len(self.bottom_arm_keypoints) - 1):
                pt1 = tuple(keypoints[self.bottom_arm_keypoints[i]].astype(int))
                pt2 = tuple(keypoints[self.bottom_arm_keypoints[i + 1]].astype(int))
                cv2.line(frame, pt1, pt2, color1, 3)
                cv2.circle(frame, pt1, 5, color1, -1)

            for i in range(len(self.hinge_keypoints) - 1):
                pt1 = tuple(keypoints[self.hinge_keypoints[i]].astype(int))
                pt2 = tuple(keypoints[self.hinge_keypoints[i + 1]].astype(int))
                cv2.line(frame, pt1, pt2, color2, 3)
                cv2.circle(frame, pt1, 5, color2, -1)

            for i in range(1):
                pt1 = tuple(keypoints[self.spine_keypoints[i]].astype(int))
                pt2 = tuple(keypoints[self.spine_keypoints[i + 1]].astype(int))
                cv2.line(frame, pt1, pt2, color3, 3)
                cv2.circle(frame, pt1, 5, color3, -1)

            if show_angle:
                bottom_elbow_angle = calculate_angle(
                    keypoints[self.bottom_arm_keypoints[0]],
                    keypoints[self.bottom_arm_keypoints[1]],
                    keypoints[self.bottom_arm_keypoints[2]]
                )
                hinge_angle = calculate_angle(
                    keypoints[self.hinge_keypoints[0]],
                    keypoints[self.hinge_keypoints[1]],
                    keypoints[self.hinge_keypoints[2]]
                )
                spine_angle = calculate_angle(
                    keypoints[self.spine_keypoints[0]],
                    keypoints[self.spine_keypoints[1]],
                    keypoints[self.spine_keypoints[2]]
                )

                bottom_elbow_angles.append(bottom_elbow_angle)
                hinge_angles.append(hinge_angle)
                spine_angles.append(spine_angle)
                time.append(frame_count)

            cv2.imshow("Keypoints", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Smooth the data using Gaussian filter
        bottom_elbow_angles_smooth = gaussian_filter1d(bottom_elbow_angles, sigma=2)
        hinge_angles_smooth = gaussian_filter1d(hinge_angles, sigma=2)
        spine_angles_smooth = gaussian_filter1d(spine_angles, sigma=2)

        plt.ioff()

        # Plot smoothed data
        axs[0, 0].plot(time[:len(bottom_elbow_angles_smooth)], bottom_elbow_angles_smooth, color="cyan")
        axs[0, 0].axhline(y=150, color='red', linestyle='-', label='Upper Threshold for Elbow Angle')
        axs[0, 0].axhline(y=110, color='blue', linestyle='-', label='Lower Threshold for Elbow Angle')
        axs[0, 0].set_title("Elbow Angle vs. Time")
        axs[0, 0].legend()

        axs[0, 1].plot(time[:len(hinge_angles_smooth)], hinge_angles_smooth, color="magenta")
        axs[0, 1].axhline(y=80, color='red', linestyle='-', label='Upper Threshold for Hinge Angle')
        axs[0, 1].set_title("Hinge Angle vs. Time")
        axs[0, 1].legend()

        axs[1, 0].plot(time[:len(spine_angles_smooth)], spine_angles_smooth, color="red")
        axs[1, 0].axhline(y=120, color='red', linestyle='-', label='Upper Threshold for Neck Angle')
        axs[1, 0].set_title("Neck Angle vs. Time")
        axs[1, 0].legend()

        plt.show()

        cap.release()
        cv2.destroyAllWindows()


def run_analyze_pose(show_angle):
    video_name = input("Enter the name of the video to download and process: ")
    output_file_path = f"{video_name}.mp4"
    download_video(video_name, output_file_path)
    estimation = PoseEstimation(output_file_path)
    estimation.analyze_pose(show_angle=True)

if __name__ == '__main__':
    run_analyze_pose(show_angle=True)