# ============================================================
# utils/predictor.py
# Modul untuk load model dan melakukan prediksi
# Klasifikasi Kostum Tari Tradisional Jawa Tengah
# ============================================================

import numpy as np
import json
import os
import time
from PIL import Image
import streamlit as st

# Import config
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    CLASS_DISPLAY_NAMES, IMG_SIZE,
    MODEL_FILE, MODEL_FILE_H5,
    CONFIDENCE_HIGH, CONFIDENCE_MEDIUM
)


@st.cache_resource(show_spinner=False)
def load_model(model_dir: str):
    """
    Load model TensorFlow/Keras dengan caching Streamlit.
    Dicoba dari format .keras dulu, fallback ke .h5.

    Args:
        model_dir: Path ke folder yang berisi model

    Returns:
        model: Model Keras yang sudah diload
    """
    import tensorflow as tf

    keras_path = os.path.join(model_dir, MODEL_FILE)
    h5_path    = os.path.join(model_dir, MODEL_FILE_H5)

    if os.path.exists(keras_path):
        model = tf.keras.models.load_model(keras_path)
        return model
    elif os.path.exists(h5_path):
        model = tf.keras.models.load_model(h5_path)
        return model
    else:
        raise FileNotFoundError(
            f"Model tidak ditemukan!\n"
            f"Pastikan file berikut ada di folder '{model_dir}':\n"
            f"  - {MODEL_FILE}  (direkomendasikan)\n"
            f"  - {MODEL_FILE_H5}  (alternatif)"
        )


def load_metadata(model_dir: str) -> dict:
    """
    Load metadata model dari file JSON.

    Args:
        model_dir: Path ke folder model

    Returns:
        dict: Metadata model
    """
    meta_path = os.path.join(model_dir, 'model_metadata.json')
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def preprocess_image(image: Image.Image, target_size: tuple = IMG_SIZE) -> np.ndarray:
    """
    Preprocess gambar untuk input ke model CNN.

    Tahapan:
    1. Konversi ke RGB (handle PNG transparan, grayscale, dll)
    2. Resize ke 224x224 piksel
    3. Normalisasi piksel 0-255 → 0.0-1.0
    4. Tambahkan dimensi batch

    Args:
        image      : PIL Image object
        target_size: Ukuran target (default: 224x224)

    Returns:
        np.ndarray: Array shape (1, 224, 224, 3), tipe float32
    """
    # Konversi ke RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Resize dengan metode LANCZOS (kualitas terbaik)
    image = image.resize(target_size, Image.LANCZOS)

    # Konversi ke numpy array
    img_array = np.array(image, dtype=np.float32)

    # Normalisasi: 0-255 → 0-1
    img_array = img_array / 255.0

    # Tambahkan dimensi batch: (224, 224, 3) → (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def predict(model, image: Image.Image) -> dict:
    """
    Lakukan prediksi klasifikasi kostum tari dari sebuah gambar.

    Args:
        model: Model Keras yang sudah diload
        image: PIL Image object

    Returns:
        dict berisi:
            - predicted_class  : Nama kelas yang diprediksi
            - confidence       : Skor kepercayaan (0-1)
            - confidence_pct   : Skor kepercayaan dalam persen
            - all_probabilities: Dict semua kelas dan probabilitasnya
            - inference_time_ms: Waktu inferensi dalam milidetik
            - confidence_level : 'high', 'medium', atau 'low'
    """
    # Preprocess gambar
    img_array = preprocess_image(image)

    # Ukur waktu inferensi
    start_time = time.time()
    predictions = model.predict(img_array, verbose=0)
    inference_time = (time.time() - start_time) * 1000  # ms

    # Ambil hasil
    pred_idx       = int(np.argmax(predictions[0]))
    confidence     = float(predictions[0][pred_idx])
    predicted_name = CLASS_DISPLAY_NAMES[pred_idx]

    # Semua probabilitas
    all_probs = {
        CLASS_DISPLAY_NAMES[i]: float(predictions[0][i])
        for i in range(len(CLASS_DISPLAY_NAMES))
    }

    # Tentukan level kepercayaan
    if confidence >= CONFIDENCE_HIGH:
        conf_level = 'high'
    elif confidence >= CONFIDENCE_MEDIUM:
        conf_level = 'medium'
    else:
        conf_level = 'low'

    return {
        'predicted_class'  : predicted_name,
        'confidence'       : confidence,
        'confidence_pct'   : confidence * 100,
        'all_probabilities': all_probs,
        'inference_time_ms': inference_time,
        'confidence_level' : conf_level,
        'pred_idx'         : pred_idx,
    }


def get_top_k_predictions(predictions: dict, k: int = 3) -> list:
    """
    Ambil top-k prediksi berdasarkan probabilitas.

    Args:
        predictions: Output dari fungsi predict()
        k          : Jumlah top prediksi yang diambil

    Returns:
        list of tuples: [(class_name, probability), ...]
    """
    sorted_preds = sorted(
        predictions['all_probabilities'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    return sorted_preds[:k]


def validate_image(image: Image.Image) -> tuple[bool, str]:
    """
    Validasi gambar sebelum diprediksi.

    Args:
        image: PIL Image object

    Returns:
        (is_valid: bool, message: str)
    """
    # Cek ukuran minimum
    min_size = 50
    if image.width < min_size or image.height < min_size:
        return False, f"Gambar terlalu kecil. Minimal {min_size}x{min_size} piksel."

    # Cek ukuran maksimum (untuk menghindari memory overflow)
    max_size = 10000
    if image.width > max_size or image.height > max_size:
        return False, f"Gambar terlalu besar. Maksimal {max_size}x{max_size} piksel."

    # Cek mode gambar
    valid_modes = ['RGB', 'RGBA', 'L', 'P', 'CMYK']
    if image.mode not in valid_modes:
        return False, f"Format gambar tidak didukung: {image.mode}"

    return True, "Gambar valid"
