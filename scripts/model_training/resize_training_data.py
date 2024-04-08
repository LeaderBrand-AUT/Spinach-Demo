from PIL import Image                                              
import os, sys        
import constants     
import cv2          

def resize_images_in_directory(input_dir, output_dir, new_width, new_height):
    """
    Resize all images in a directory and its subdirectories and save them in a different directory.
    
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
            # Check if the file is an image
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                # Read the image
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)
                
                # Resize the image
                resized_img = cv2.resize(img, (new_width, new_height))
                
                # Save the resized image
                output_path = os.path.join(output_subdir, file)
                cv2.imwrite(output_path, resized_img)
                print(f"Resized image saved: {output_path}")

# Example usage:
input_directory = "spinach_training"
output_directory = "spinach_training_processed"

resize_images_in_directory(input_directory, output_directory, constants.IMAGE_WIDTH, constants.IMAGE_HEIGHT)