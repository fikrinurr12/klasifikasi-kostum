# ============================================================
# FILE: utils/model_utils.py
# DESKRIPSI: Fungsi utilitas untuk memuat model dan prediksi
# ============================================================

import numpy as np
import json
import os
import streamlit as st
from PIL import Image


def load_class_mapping(mapping_path):
    """Memuat mapping kelas dari file JSON."""
    if not os.path.exists(mapping_path):
        return None
    with open(mapping_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@st.cache_resource(show_spinner="⏳ Memuat model AI...")
def load_model_cached(model_path, mapping_path):
    """
    Memuat model TensorFlow dengan caching Streamlit.
    Model hanya dimuat sekali dan disimpan di cache.
    
    Returns:
        (bool, model, class_mapping)
    """
    # Import di dalam fungsi agar tidak error jika TF belum install
    try:
        import tensorflow as tf
    except ImportError:
        st.error("TensorFlow tidak terinstall. Jalankan: pip install tensorflow")
        return False, None, None

    # Cek keberadaan file model
    if not os.path.exists(model_path):
        return False, None, None

    # Load class mapping
    class_mapping = load_class_mapping(mapping_path)
    if class_mapping is None:
        # Gunakan default mapping jika file tidak ada
        class_mapping = {
            'class_names': [
                'Tari_Bedhaya', 'Tari_Dolalak', 'Tari_Gambyong',
                'Tari_Golek', 'Tari_Srimpi'
            ],
            'class_labels': {
                'Tari_Bedhaya'  : 'Tari Bedhaya',
                'Tari_Dolalak'  : 'Tari Dolalak',
                'Tari_Gambyong' : 'Tari Gambyong',
                'Tari_Golek'    : 'Tari Golek',
                'Tari_Srimpi'   : 'Tari Srimpi'
            },
            'idx_to_class': {
                '0': 'Tari_Bedhaya',
                '1': 'Tari_Dolalak',
                '2': 'Tari_Gambyong',
                '3': 'Tari_Golek',
                '4': 'Tari_Srimpi'
            },
            'num_classes': 5,
            'img_size': [224, 224]
        }

    # Load model
    try:
        # Coba format .keras terlebih dahulu
        if model_path.endswith('.keras'):
            model = tf.keras.models.load_model(model_path)
        elif model_path.endswith('.h5'):
            model = tf.keras.models.load_model(model_path)
        else:
            model = tf.keras.models.load_model(model_path)

        # Warmup prediction
        dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
        _ = model.predict(dummy, verbose=0)

        return True, model, class_mapping

    except Exception as e:
        st.error(f"Gagal memuat model: {str(e)}")
        return False, None, None


def preprocess_image(image: Image.Image, img_size=(224, 224)) -> np.ndarray:
    """
    Preprocessing gambar sebelum diprediksi:
    1. Resize ke 224x224
    2. Convert ke array numpy
    3. Preprocessing MobileNetV2 (normalisasi [-1, 1])
    
    Args:
        image: PIL Image object
        img_size: tuple ukuran target (default 224x224)
    
    Returns:
        numpy array shape (1, 224, 224, 3)
    """
    try:
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        from tensorflow.keras.preprocessing.image import img_to_array
    except ImportError:
        # Fallback manual normalisasi jika import gagal
        preprocess_input = lambda x: (x / 127.5) - 1.0
        img_to_array = lambda img: np.array(img, dtype=np.float32)

    # Pastikan RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Resize
    image_resized = image.resize(img_size, Image.LANCZOS)

    # Convert ke array
    img_array = img_to_array(image_resized)

    # Preprocess MobileNetV2 (scale ke [-1, 1])
    img_array = preprocess_input(img_array)

    # Tambah dimensi batch
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def predict_image(model, image: Image.Image, class_mapping: dict) -> dict:
    """
    Melakukan prediksi pada satu gambar.
    
    Args:
        model: Model TensorFlow yang sudah dimuat
        image: PIL Image object
        class_mapping: Dictionary mapping kelas
    
    Returns:
        Dictionary berisi hasil prediksi:
        {
            'predicted_class': str,
            'predicted_label': str,
            'confidence': float (0-100),
            'probabilities': list[float],
            'top3': list[dict]
        }
    """
    try:
        # Preprocessing
        img_size = tuple(class_mapping.get('img_size', [224, 224]))
        img_array = preprocess_image(image, img_size)

        # Prediksi
        predictions = model.predict(img_array, verbose=0)[0]

        # Ambil kelas terprediksi
        pred_idx   = int(np.argmax(predictions))
        class_names = class_mapping.get('class_names', [])
        class_labels = class_mapping.get('class_labels', {})

        pred_class = class_names[pred_idx] if pred_idx < len(class_names) else f"class_{pred_idx}"
        pred_label = class_labels.get(pred_class, pred_class)
        confidence = float(predictions[pred_idx]) * 100

        # Top-3 prediksi
        top3_idx = np.argsort(predictions)[::-1][:3]
        top3 = []
        for idx in top3_idx:
            cls   = class_names[idx] if idx < len(class_names) else f"class_{idx}"
            label = class_labels.get(cls, cls)
            top3.append({
                'class'      : cls,
                'label'      : label,
                'probability': float(predictions[idx]) * 100
            })

        return {
            'predicted_class' : pred_class,
            'predicted_label' : pred_label,
            'confidence'      : confidence,
            'probabilities'   : [float(p) for p in predictions],
            'top3'            : top3,
            'pred_idx'        : pred_idx
        }

    except Exception as e:
        st.error(f"Error saat prediksi: {str(e)}")
        return None
