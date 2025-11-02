import random
import threading
import time
import requests

from constants import *
from detector import Detector
from emulator import Emulator
from basenstreamer import ChunkerStreamer
from message_handler import char_map

pause_event = threading.Event()
pause_event.set()
is_paused_logged = False
is_resumed_logged = True


class Bot:
    is_paused_logged = False
    is_resumed_logged = True
    streamer : ChunkerStreamer

    def __init__(self, player_num):
        self.message_queue = []
        self.incoming_message_queue = []

        self.player_num = player_num

        self.handle_game_step_counter = 0

        self.position_last_trigger_time = {}
        self.position_cooldown = 3  # 1.5 second cooldown

        self.ready_last_place_time = {}
        self.ready_cooldown = 0.4

        self.emulator = Emulator("emulator-5554", "127.0.0.1")
        self.detector = Detector()
        self.streamer = ChunkerStreamer()
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

    def play_action(self, index, tile_x, tile_y):
        card_centre = self._get_card_centre(index)
        tile_centre = self._get_tile_centre(tile_x, tile_y)
        self.emulator.click(*card_centre)
        self.emulator.click(*tile_centre)

    @staticmethod
    def str_to_bin(str_value):
        binary =""
        for c in str_value:
            val = list(char_map.keys())[list(char_map.values()).index(c)]
            bits = bin(val)[2:].zfill(5)
            binary += bits
        return binary

    def step(self):
        #self._handle_play_pause_in_step()

        self.set_state()
        self._handle_game_step()
        self.decode_clock_positions()
        
        data = self.streamer.pop_all()

        
        if data:
            print(f"Data \"{data}\" (chunked format: {ChunkerStreamer.chunk_binary(Bot.str_to_bin(data))}) just read")
            BASE_URL = "http://127.0.0.1:5000/newchar"
            for char in data:
                url = f"{BASE_URL}/{char}"
                try:
                    res = requests.get(url)
                except Exception as e:
                    print("Error:", e)


        res = requests.get("http://127.0.0.1:5000/check_new_message").json()
        #print(res)
        if res["new_data"]:
            binary = self.str_to_bin(res["message"])

            self.message_queue.extend(ChunkerStreamer.chunk_binary(binary))


            print(f"Message \"{res['message']}\" is loaded into the queue, current state: {self.message_queue}")


        

    def _handle_game_step(self):
        print(self.state.screen.name)
        if self.state.screen.name == "in_game":
            if len(self.state.ready) == 0 or len(self.message_queue) == 0:
                #self._log_and_wait("No actions available", self.play_action_delay)
                return

            # Trigger first ready, then return
            for ready in self.state.ready:
                if self._can_trigger_ready(ready):
                    # This is the core logic!
                    index = self.message_queue.pop(0)
                    pos = ALLY_TILES[self.message_queue.pop(0)]
                    self.play_action(ready, *pos)

                    self._log_and_wait(
                        f"Sent data!",
                        self.play_action_delay,
                    )
                    return
        elif self.state.screen.name == "end_of_game":
            self.emulator.click(*self.state.screen.click_xy)
            time.sleep(.5)
        elif self.state.screen.name == "lobby":
            self.emulator.click(446, 139)
            time.sleep(.5)
            if self.player_num == 1:
                self.request_friendly_match()
        elif self.state.screen.name == "can_accept_battle":
            self.emulator.click(*self.state.screen.click_xy)
            time.sleep(.5)


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

    def _can_trigger_ready(self, ready):
        current_time = time.time()
        if ready in self.ready_last_place_time:
            time_since_last_place = current_time - self.ready_last_place_time[ready]
            if time_since_last_place < self.ready_cooldown:
                return False

        self.ready_last_place_time[ready] = current_time
        return True

    def decode_clock_positions(self):
        for p in self.state.clock_positions:
            if not self._can_trigger_position(p.tile_x, p.tile_y):
                continue
            if (p.tile_x, p.tile_y) not in ENEMY_TILES:
                print("Found invalid clock at: "+str(p.tile_x)+" "+str(p.tile_y))
                continue
            current_time = time.time()
            seconds = int(current_time % 60)
            milliseconds = int((current_time % 1) * 1000)
            print(f"{p.tile_x} {p.tile_y}, {seconds}.{milliseconds:03d}, {ENEMY_TILES.index((p.tile_x, p.tile_y))}")

            self.streamer.push(ENEMY_TILES.index((p.tile_x, p.tile_y)))

    def request_friendly_match(self):
        delay = 0.1
        time.sleep(delay)
        self.emulator.click(360, 411)
        time.sleep(delay)
        self.emulator.click(569, 492)
        time.sleep(delay)
        self.emulator.replay_events("select_match.sh")
        #time.sleep(delay)
        self.emulator.click(360, 1030)

    def enqueue_data(self, new_data):
        self.message_queue += new_data

    def run(self):
        try:
            while self.should_run:
                self.step()
            print("Thanks for using CRBAB, see you next time!")
        except KeyboardInterrupt:
            print("Thanks for using CRBAB, see you next time!")

    def stop(self):
        self.should_run = False

player_num = input("Are you player 1 or player 2: ")
test = Bot(1 if player_num == "1" else 2)
test.run()