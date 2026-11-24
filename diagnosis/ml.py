import os
import tensorflow as tf
import tensorflow_hub as hub
import tf_keras as tfk
import numpy as np
from django.conf import settings

def load_model(model_path):
    print(f"Loading saved model from: {model_path}...")
    model = tfk.models.load_model(model_path,
                                custom_objects={"KerasLayer": hub.KerasLayer})
    return model

def process_image(image_path, img_size=224):
    """
    Turns the image into a Tensor.
    """
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, size = [img_size, img_size])

    return image

def get_image_label(image_path, label):
  return process_image(image_path), label

def create_data_batches(X, y=None, batch_size=32, valid_data=False, test_data=False):
    if test_data:
        print("Creating test data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X)))
        data_batch = data.map(process_image).batch(batch_size)
        return data_batch
    elif valid_data:
        print("Creating validation data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X),
                                                   tf.constant(y)))
        data_batch = data.map(get_image_label).batch(batch_size)
        return data_batch
    else:
        print("Creating training data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X),
                                                   tf.constant(y)))
        data = data.shuffle(buffer_size=len(X))
        data = data.map(get_image_label)
        data_batch = data.batch(batch_size)
    return data_batch

def get_pred_label(preds):
    """
    Turns an array of prediction probabilities into a label.
    """
    labels = ['normal', 'pneumonia']
    classes = np.unique(labels)
    return classes[np.argmax(preds)]

MODEL_PATH = os.path.join(settings.BASE_DIR, 'diagnosis', 'models', '20260122-06061769064826-full-model-mobilenetv2-Adam.h5')

_ai_model = None

def get_ai_model():
    global _ai_model
    if _ai_model is None:
        print("Loading ML model...")
        try:
            _ai_model = load_model(MODEL_PATH)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Failed to load model: {e}")
    return _ai_model

def calculate_xray_probability(img_path):
    model = get_ai_model()
    if model is None:
        return "Model Error", 0.0
    data = create_data_batches([img_path], test_data=True)

    prediction = model.predict(data)
    label = get_pred_label(prediction[0])
    probability = np.max(prediction) * 100

    return label, probability