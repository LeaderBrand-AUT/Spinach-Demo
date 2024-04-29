from PIL import Image                                              
import os, sys        
from ..preprocessor import preprocessor
import cv2          

def process_images_in_directory(input_dir, output_dir):
    """
    Processes all videos in a directory and its subdirectories and save them in a different directory.
    
    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory where resized images will be saved.
        new_width (int): New width of the resized images.
        new_height (int): New height of the resized images.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through input directory and its subdirectories
    for root, dirs, files in os.walk(input_dir):
        # Create corresponding subdirectories in output directory
        rel_path = os.path.relpath(root, input_dir)
        output_subdir = os.path.join(output_dir, rel_path)
        os.makedirs(output_subdir, exist_ok=True)
        
        # Process files in the current directory
        for file in files:
            print(file)
            # Check if the file is an image
            if file.lower().endswith(('.mov')):
                vid_path = os.path.join(root, file)
                print(f"Processing {vid_path}")

                video_capture = cv2.VideoCapture(vid_path)

                # Get the frame rate of the video
                fps = video_capture.get(cv2.CAP_PROP_FPS)

                # Initialize variables
                frame_number = 0
                success = True

                while success:
                    # Set the frame position to the corresponding second
                    video_capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_number * fps))
                    
                    # Read the frame
                    success, frame = video_capture.read()
                    
                    if success:                
                        # process the image
                        processed_image = preprocessor(frame)
                        
                        # Save the processed image
                        output_path = os.path.join(output_subdir, file + "_frame" + str(frame_number) + '.jpg')
                        cv2.imwrite(output_path, processed_image)
                        print(f"Processed image saved: {output_path}")
                    
                    # Move to the next second
                    frame_number += 1
                
                # Release the video capture object
                video_capture.release()

# Example usage:
input_directory = "spinach_training"
output_directory = "spinach_training_processed"

process_images_in_directory(input_directory, output_directory)