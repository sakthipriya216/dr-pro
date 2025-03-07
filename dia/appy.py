from flask import Flask, request, render_template
import os
import tensorflow as tf
import cv2
import numpy as np

app = Flask(__name__)

# Load your trained model
MODEL_PATH = 'dr_model.h5'
model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/', methods=['GET'])
def index():
    # Render an HTML form to upload the image
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # The file is saved temporarily for prediction
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        
        img = cv2.imread(filepath)
        RGBImg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        RGBImg= cv2.resize(RGBImg,(224,224))
        image = np.array(RGBImg) / 255.0
        new_model = tf.keras.models.load_model("dr_model.h5")
        predict=new_model.predict(np.array([image]))
        per=np.argmax(predict,axis=1)
        os.remove(filepath)
        if per==1:
            return 'No DR'
        else:
            return 'DR'
        
        # Clean up: remove the uploaded file after prediction
        

if __name__ == '__main__':
    app.run(debug=True)
