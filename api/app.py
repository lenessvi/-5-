from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
import io

app = Flask(__name__)

# Загружаем модель Keras
model = tf.keras.models.load_model('Ну тут модель сами вставите, файлы есть')

# Классы эмоций
CLASSES = ['angry', 'sad', 'happy', 'relax']

# Предобработка изображения
def preprocess_image(image):
    image = image.resize((224, 224))  # адаптируй под размер своей модели
    image = np.array(image) / 255.0   # нормализация
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream).convert('RGB')
    image_array = preprocess_image(image)

    # Предсказание
    prediction = model.predict(image_array)
    predicted_idx = np.argmax(prediction)
    emotion = CLASSES[predicted_idx]

    return jsonify({'emotion': emotion})

if __name__ == '__main__':
    app.run(debug=True)
