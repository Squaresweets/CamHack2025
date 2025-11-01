from copy import deepcopy
import os
import time

from loguru import logger

from constants import *
from ready_detector import ReadyDetector
from clock_detector import  ClockDetector
from state import *


class Detector:
    DECK_SIZE = 8

    def __init__(self):
        self.card_detector = ReadyDetector()

    def run(self, image):
        logger.debug("Setting state...")
        retries = 3
        for attempt in range(retries):
            try:
                ready = self.card_detector.run(image)
                clock_positions = ClockDetector.identify_clocks(image)
                
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
