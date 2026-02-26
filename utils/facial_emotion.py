from deepface import DeepFace
import numpy as np
from PIL import Image

def detect_emotion_from_image(image):
    """
    Takes a Streamlit camera image and returns dominant emotion
    """

    try:
        # Convert UploadedFile to PIL Image
        pil_image = Image.open(image)

        # Convert PIL to numpy array
        img = np.array(pil_image)

        # Analyze emotion
        result = DeepFace.analyze(
            img,
            actions=['emotion'],
            enforce_detection=False
        )

        emotion = result[0]['dominant_emotion']
        return emotion

    except Exception as e:
        return "Unknown"
