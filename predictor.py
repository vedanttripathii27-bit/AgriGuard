import numpy as np
import tensorflow as tf
from PIL import Image

MODEL_PATH = "models/agri_guard_best.keras"
IMG_SIZE = (224, 224)

CLASS_NAMES = [
    "Apple___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Strawberry___Leaf_scorch",
    "Tomato___Early_blight",
    "Tomato___Target_Spot",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading AgriGuard AI model...")
        _model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False
        )
        print("AgriGuard AI model loaded successfully!")

    return _model


def predict_disease(image):

    model = get_model()

    image = image.convert("RGB")
    image = image.resize(IMG_SIZE)

    img_array = np.array(
        image,
        dtype=np.float32
    )

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    predictions = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = int(
        np.argmax(predictions[0])
    )

    confidence = float(
        predictions[0][predicted_index] * 100
    )

    raw_class = CLASS_NAMES[predicted_index]

    if "___" in raw_class:
        crop, disease = raw_class.split(
            "___",
            1
        )
    else:
        crop = raw_class
        disease = "Unknown"

    crop = crop.replace("_", " ")
    disease = disease.replace("_", " ")

    return {
        "crop": crop,
        "disease": disease,
        "confidence": confidence,
        "raw_class": raw_class
    }