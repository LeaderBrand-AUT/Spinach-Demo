import os, cv2
import constants

def check_image_dimensions(input_dir):
    # Iterate through input directory and its subdirectories
    for root, dirs, files in os.walk(input_dir):
        # Process files in the current directory
        for file in files:
            img_path = os.path.join(root, file)

            img = cv2.imread(img_path)

            if img is None:
                print(f"cannot read image {img_path}")

            height, width = img.shape[:2]

            if (height != constants.IMAGE_HEIGHT or width != constants.IMAGE_WIDTH):
                print(f"{img_path} is not the right size.")

input_dir = "spinach_training_processed"

check_image_dimensions(input_dir=input_dir)