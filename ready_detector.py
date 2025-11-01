import os

import numpy as np
from PIL import Image
from scipy.optimize import linear_sum_assignment

from constants import CARD_CONFIG


class ReadyDetector:
    def __init__(self, grey_std_threshold=5):
        self.grey_std_threshold = grey_std_threshold

    def _detect_if_ready(self, crops):
        ready = []
        for i, crop in enumerate(crops[1:]):
            std = np.mean(np.std(np.array(crop), axis=2))
            if std > self.grey_std_threshold:
                ready.append(i)
        return ready

    def run(self, image):
        crops = [image.crop(position) for position in CARD_CONFIG]
        ready = self._detect_if_ready(crops)
        return ready
