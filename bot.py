import random
import threading
import time

import keyboard
from loguru import logger

from constants import *
from detector import Detector
from emulator import Emulator

pause_event = threading.Event()
pause_event.set()
is_paused_logged = False
is_resumed_logged = True


class Bot:
    is_paused_logged = False
    is_resumed_logged = True

    def __init__(self, config):
        self.message_queue = []
        self.incoming_message_queue = []

        self.visualizer = Visualizer(**config["visuals"])
        self.emulator = Emulator(**config["adb"])
        self.detector = Detector()
        self.state = None
        self.play_action_delay = config.get("ingame", {}).get("play_action", 1)

    @staticmethod
    def _log_and_wait(prefix, delay):
        suffix = ""
        if delay > 1:
            suffix = "s"
        message = f"{prefix}. Waiting for {delay} second{suffix}."
        logger.info(message)
        time.sleep(delay)

    @staticmethod
    def _get_nearest_tile(x, y):
        tile_x = round(((x - TILE_INIT_X) / TILE_WIDTH) - 0.5)
        tile_y = round(
            ((DISPLAY_HEIGHT - TILE_INIT_Y - y) / TILE_HEIGHT) - 0.5
        )
        return tile_x, tile_y

    @staticmethod
    def _get_tile_centre(tile_x, tile_y):
        x = TILE_INIT_X + (tile_x + 0.5) * TILE_WIDTH
        y = DISPLAY_HEIGHT - TILE_INIT_Y - (tile_y + 0.5) * TILE_HEIGHT
        return x, y

    @staticmethod
    def _get_card_centre(card_n):
        x = (
            DISPLAY_CARD_INIT_X
            + DISPLAY_CARD_WIDTH / 2
            + card_n * DISPLAY_CARD_DELTA_X
        )
        y = DISPLAY_CARD_Y + DISPLAY_CARD_HEIGHT / 2
        return x, y

    def set_state(self):
        screenshot = self.emulator.take_screenshot()
        self.state = self.detector.run(screenshot)
        self.visualizer.run(screenshot, self.state)

    def play_action(self, index, position):
        card_centre = self._get_card_centre(index)
        tile_centre = self._get_tile_centre(position.tile_x, position.tile_y)
        self.emulator.click(*card_centre)
        self.emulator.click(*tile_centre)

    def step(self):
        self._handle_play_pause_in_step()

        self.set_state()
        self._handle_game_step()
        self.decode_clock_positions()

    def _handle_game_step(self):
        if len(self.state.ready) == 0 or len(message_queue) == 0:
            self._log_and_wait("No actions available", self.play_action_delay)
            return

        #This is the core logic!
        pos = ALLY_TILES[message_queue.pop()]
        self.play_action(ready[0], *pos)

        self._log_and_wait(
            f"Sent data!",
            self.play_action_delay,
        )

    def decode_clock_positions(self):
        for p in self.state.clock_positions:
            self.incoming_message_queue.add(ENEMY_TILES.indexof((p.tile_x, p.tile_y))
        
    def enqeue_data(self, new_data):
        self.message_queue += new_data

    def fetch_recieved_data(self):
        output = self.incoming_message_queue.copy()
        self.incoming_message_queue = []
        return output

    def run(self):
        try:
            while self.should_run:
                if not pause_event.is_set():
                    time.sleep(0.1)
                    continue

                self.step()
            logger.info("Thanks for using CRBAB, see you next time!")
        except KeyboardInterrupt:
            logger.info("Thanks for using CRBAB, see you next time!")

    def stop(self):
        self.should_run = False
