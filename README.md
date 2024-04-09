# Spinach_Demo

How to run:
 - Active virtual environment
    - Windows: .\venv\Scripts\activate
    - macos: source venv/bin/activate

 - install requirements
    - pip install -r requirements.txt

## Classification Model
To use the classifier, please populate the ./spinach_training directory with images. Run scripts.model_training.resize_training_data.py to resize the images to the correct size, and then run the scripts.model_trainign.create_model.py file. Test scripts exist in the scripts.test module to evaluate the model, and make predictions.

Note: to run python files in the command line, use the -m flag. Example: '*python -m scripts.test.classify.py*'