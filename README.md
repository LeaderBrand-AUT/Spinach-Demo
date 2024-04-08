# Spinach_Demo

How to run:
 - Active virtual environment
    - Windows: .\venv\Scripts\activate
    - macos: source venv/bin/activate

 - install requirements
    - pip install -r requirements.txt

## Classification Model
To use the classifier, please populate the ./spinach_training directory with images. Run scripts/resize_training_data.py to resize the images to the correct size, and then run the create_model.py file. Test scripts currently exist in the root directory to evaluate the model, and make predictions.