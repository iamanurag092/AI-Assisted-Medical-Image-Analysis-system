import os
import numpy as np
from flask import Flask, request, render_template
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

# Initialize Flask app
app = Flask(__name__)

# Load the trained model (Ensure the model is uploaded in the correct directory on the server)
model = load_model('pneumonia_detector_efficientnet.keras')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file from the form
        img_file = request.files['file']
        
        # Ensure the file is uploaded
        if img_file:
            # Save the image temporarily in the 'uploads' directory
            img_path = os.path.join('./uploads', img_file.filename)
            img_file.save(img_path)

            # Preprocess the uploaded image
            img = load_img(img_path, target_size=(224, 224))  # Resize to 224x224 for EfficientNetB0
            img_array = img_to_array(img) / 255.0  # Normalize the image
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

            # Make a prediction using the model
            prediction = model.predict(img_array)

            # Determine the prediction result
            result = 'Pneumonia' if prediction > 0.5 else 'Normal'

            # Return the result to the user
            return render_template('upload.html', prediction=result)

    # Render the HTML page for the user to upload a file
    return render_template('upload.html')

if __name__ == "__main__":
    # Ensure the uploads folder exists
    if not os.path.exists('./uploads'):
        os.makedirs('./uploads')

    # Run the Flask app on port 80 (or any other available port)
    app.run(debug=True, host='0.0.0.0', port=80)
