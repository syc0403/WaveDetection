import warnings
import os
from ultralytics import YOLO

# Ignore warnings
warnings.filterwarnings('ignore')

def process_videos_in_folder(folder_path, model):
    # Get all video files in the folder
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov'))]  # Modify this based on the types of video files you have
    
    # Loop through each video file
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        print(f"Processing video: {video_path}")
        
        # Use the YOLO model to make predictions on the video
        model.predict(source=video_path,
                      imgsz=640,
                      project='runs/detect',
                      name='exp',
                      save=True)
        print(f"Finished processing: {video_file}")

if __name__ == '__main__':
    # Load your trained YOLO model
    model = YOLO('runs/train/YOLOv6n/weights/best.pt')  # Select your model.pt path
    
    # Define the folder containing the videos
    folder_path = 'video'  # Replace with the actual path of your video folder
    
    # Process all videos in the folder
    process_videos_in_folder(folder_path, model)
