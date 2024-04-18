# import cv2
# import numpy as np
# import sys
# import skimage

# def white_balancing(frame):
#     return skimage.img_as_ubyte((frame*1.0 / np.percentile(frame, 99.4, axis=(0, 1))).clip(0, 1))

import cv2
import numpy as np
import skimage
import os
from skimage import img_as_ubyte

def white_balancing(frame, brightness_factor=0.8):
    # Normalize the frame based on the 99.4th percentile
    normalized_frame = frame * 1.0 / np.percentile(frame, 99.4, axis=(0, 1))
    
    # Clip the values to keep them within the range [0, 1]
    clipped_frame = normalized_frame.clip(0, 1)
    
    # Reduce the brightness by multiplying with a factor less than 1
    adjusted_frame = clipped_frame * brightness_factor
    
    # Convert the floating-point image to 8-bit unsigned byte format
    final_image = img_as_ubyte(adjusted_frame)
    
    return final_image

# def process_directory(input_dir, output_dir):
#     # Ensure output directory exists
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     # Process each file in the directory
#     for filename in os.listdir(input_dir):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#             file_path = os.path.join(input_dir, filename)
#             frame = cv2.imread(file_path)
#             if frame is not None:
#                 processed_image = white_balancing(frame)
#                 output_file_path = os.path.join(output_dir, f"post-{filename}")
#                 cv2.imwrite(output_file_path, processed_image)
#                 print(f"Processed and saved: {output_file_path}")
#             else:
#                 print(f"Error: Image not found or path is incorrect for {filename}")

# # Example usage:
# input_directory = 'input_data'  # Update this path
# output_directory = 'test'  # Update this path
# process_directory(input_directory, output_directory)

