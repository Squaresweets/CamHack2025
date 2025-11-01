import random
import threading
import time

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

    def __init__(self):
        self.message_queue = []
        self.incoming_message_queue = []

        self.position_last_trigger_time = {}
        self.position_cooldown = 1.5  # 1.5 second cooldown

        self.emulator = Emulator("emulator-5554", "127.0.0.1")
        self.detector = Detector()
        self.state = None
        self.play_action_delay = 0.1
        self.should_run = True

    @staticmethod
    def _log_and_wait(prefix, delay):
        suffix = ""
        if delay > 1:
            suffix = "s"
        message = f"{prefix}. Waiting for {delay} second{suffix}."
        print(message)
        time.sleep(delay)

    @staticmethod
    def _get_nearest_tile(x, y):
        # Note, this is x and y in device coords, not screenshot coords
        # If in screenshot coords, must resize first
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

    def play_action(self, index, position):
        card_centre = self._get_card_centre(index)
        tile_centre = self._get_tile_centre(position.tile_x, position.tile_y)
        self.emulator.click(*card_centre)
        self.emulator.click(*tile_centre)

    def step(self):
        #self._handle_play_pause_in_step()

        self.set_state()
        self._handle_game_step()
        self.decode_clock_positions()

    def _handle_game_step(self):
        if len(self.state.ready) == 0 or len(self.message_queue) == 0:
            #self._log_and_wait("No actions available", self.play_action_delay)
            return

        #This is the core logic!
        pos = ALLY_TILES[self.message_queue.pop()]
        self.play_action(self.state.ready[0], *pos)

        self._log_and_wait(
            f"Sent data!",
            self.play_action_delay,
        )

    def _can_trigger_position(self, tile_x, tile_y):
        """Check if a position can trigger based on cooldown timer"""
        current_time = time.time()
        position_key = (tile_x, tile_y)

        # Check if position has been triggered before
        if position_key in self.position_last_trigger_time:
            time_since_last_trigger = current_time - self.position_last_trigger_time[position_key]
            if time_since_last_trigger < self.position_cooldown:
                return False

        # Update last trigger time
        self.position_last_trigger_time[position_key] = current_time
        return True

    def decode_clock_positions(self):
        for p in self.state.clock_positions:
            if not self._can_trigger_position(p.tile_x, p.tile_y):
                #print(f"Position ({p.tile_x}, {p.tile_y}) on cooldown, skipping")
                continue
            if (p.tile_x, p.tile_y) not in ENEMY_TILES:
                print("Found invalid clock at: "+str(p.tile_x)+" "+str(p.tile_y))
                continue
            current_time = time.time()
            seconds = int(current_time % 60)
            milliseconds = int((current_time % 1) * 1000)
            print(f"{p.tile_x} {p.tile_y}, {seconds}.{milliseconds:03d}")
            self.incoming_message_queue.append(ENEMY_TILES.index((p.tile_x, p.tile_y)))

        
    def enqueue_data(self, new_data):
        self.message_queue += new_data

    def fetch_received_data(self):
        output = self.incoming_message_queue.copy()
        self.incoming_message_queue = []
        return output

    def run(self):
        try:
            while self.should_run:
                self.step()
            print("Thanks for using CRBAB, see you next time!")
        except KeyboardInterrupt:
            print("Thanks for using CRBAB, see you next time!")

    def stop(self):
        self.should_run = False


test = Bot()
test.run()