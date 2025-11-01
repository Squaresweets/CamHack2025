from copy import deepcopy
import os
import time

from loguru import logger

from clashroyalebuildabot.constants import MODELS_DIR
from clashroyalebuildabot.detectors.card_detector import CardDetector
from clashroyalebuildabot.detectors.number_detector import NumberDetector
from clashroyalebuildabot.detectors.screen_detector import ScreenDetector
from clashroyalebuildabot.detectors.unit_detector import UnitDetector
from clashroyalebuildabot.namespaces import State
from error_handling import WikifiedError


class Detector:
    DECK_SIZE = 8

    def __init__(self, cards):
        self.card_detector = ReadyDetector()
        self.clock_detector = ClockDetector(os.path.join(MODELS_DIR, "units_M_480x352.onnx"))

    def run(self, image):
        logger.debug("Setting state...")
        retries = 3
        for attempt in range(retries):
            try:
                ready = self.card_detector.run(image)
                clock_positions = self.clock_detector.run(image)
                
                state = State(ready, clock_positions)
                return state
            except Exception as e:
                logger.error(
                    f"Detection failed on attempt {attempt + 1}: {str(e)}"
                )
                if attempt < retries - 1:
                    time.sleep(1)

        logger.error("All detection attempts failed. Returning default state.")
        return State([], [])
