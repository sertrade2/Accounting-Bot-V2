# ocr/preprocess.py

import cv2
import numpy as np
from PIL import Image


class ImagePreprocessor:

    @staticmethod
    def preprocess(pil_image: Image.Image) -> Image.Image:

        img = np.array(pil_image)

        # grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # contrast
        gray = cv2.equalizeHist(gray)

        # denoise
        gray = cv2.fastNlMeansDenoising(gray)

        # skew correction
        gray = ImagePreprocessor._deskew(gray)

        return Image.fromarray(gray)

    @staticmethod
    def _deskew(image):

        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)

        return cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
