import os
from download_video import *
from yolo_pose import *

def main():
    while True:
        try:
            action = input(
                "Enter:\n"
                "'1' to use a video from your computer,\n"
                "'2' to download a video,\n"
                "'3' to upload a video,\n"
                "'4' to exit.\n"
                "Your choice: "
            ).strip()

            if action == '1':
                video_name = input("Enter the name of the video: ").strip()
                # Construct the full file path in the same directory as main.py
                current_directory = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(current_directory, f"{video_name}.mp4")

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"No such file: {file_path}")

                estimation = PoseEstimation(file_path)
                estimation.analyze_pose(show_angle=True)
            elif action == '2':
                video_name = input("Enter the name of the video to analyze: ").strip()

                # Save to the same folder as main.py
                current_directory = os.path.dirname(os.path.abspath(__file__))
                output_file_path = os.path.join(current_directory, f"{video_name}.mp4")

                print(f"Downloading video to: {output_file_path}")
                download_video(video_name, output_file_path)

                estimation = PoseEstimation(output_file_path)
                estimation.analyze_pose(show_angle=True)
            elif action == '3':
                file_path = input("Enter the full path to the video file you want to upload: ").strip()
                upload_photo(file_path)
            elif action == '4':
                print("Exiting the program.")
                break
            else:
                raise ValueError("Invalid input. Please enter a number between 1 and 4.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Returning to options...\n")
        except ValueError as e:
            print(f"Error: {e}")
            print("Returning to options...\n")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Returning to options...\n")

if __name__ == "__main__":
    main()
