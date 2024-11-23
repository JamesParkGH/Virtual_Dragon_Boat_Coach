from download_video import *
from yolo_pose import *

def main():
    action = input("Enter '1' to use a video from your computer, '2' to download a video, or '3' to upload a video: ").strip()

    if action == '1':
        file_path = input("Enter the full path to the video file you want to use: ")
        estimation = PoseEstimation(file_path)
        estimation.analyze_pose(show_angle=True)
    elif action == '2':
        video_name = input("Enter the file name of the video you want to download: ")
        output_directory = input("Enter the destination directory to save the downloaded video: ").strip()
        
        output_file_path = f"{output_directory}/{video_name}.mp4"

        download_video(video_name, output_file_path)
        
        estimation = PoseEstimation(output_file_path)
        estimation.analyze_pose(show_angle=True)
    elif action == '3':
        file_path = input("Enter the full path to the video file you want to upload: ")
        upload_photo(file_path)
    else:
        print("Invalid input. Please type '1' for local video, '2' for download, or '3' for upload.")

if __name__ == "__main__":
    main()
