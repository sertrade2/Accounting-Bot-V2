import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)


def preprocess_image(image: np.ndarray) -> np.ndarray:
    logger.debug("Starting OCR preprocessing")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    gray = cv2.medianBlur(gray, 3)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    logger.debug("OCR preprocessing completed")
    return thresh
