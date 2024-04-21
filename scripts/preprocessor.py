from .preprocessing import image_resize, white_balance

def preprocessor(frame):
    # preprocessing steps
    resized_frame = image_resize.resize_frame(frame)
    white_balanced = white_balance.white_balancing(resized_frame)

    # return processed frame
    return white_balanced