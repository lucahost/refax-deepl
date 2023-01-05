from datetime import datetime
from moduls.config import app_config
from moduls.game.control import GameControl
from moduls.game.score import Score

config = app_config.game_config


def position_is_within_rectangle(pos, rect):
    return rect[0][0] < pos[0] < rect[1][0] and rect[0][1] < pos[1] < rect[1][1]


def is_control_touched(drag_pos, control_rect):
    if drag_pos is None:
        return False
    return position_is_within_rectangle(drag_pos, control_rect)


class Game:
    def __init__(self):
        self.game_data = GameData()
        self.predictions = []
        self.game_control = GameControl()
        self.control_rectangle = config.game_control_config.rectangle

    def reinit(self):
        self.game_data = GameData()
        self.predictions = []
        self.game_control = GameControl()
        self.control_rectangle = config.game_control_config.rectangle

    def start_if_touched(self, index_fingers):
        index_finger1, index_finger2 = index_fingers
        if is_control_touched(index_finger1, self.control_rectangle) \
                and (not self.game_data.is_started() or self.game_data.has_ended()):
            self.start()
        if is_control_touched(index_finger2, self.control_rectangle) \
                and (not self.game_data.is_started() or self.game_data.has_ended()):
            self.start()

    def start(self):
        self.reinit()
        self.game_data.set_start()

    def add_prediction(self, prediction):
        if not self.game_data.is_started():
            return
        if prediction is None \
                or len(prediction) == 0 \
                or self.game_data.has_ended():
            return

        self._set_end()
        self._set_current_challenge()
        self.predictions.append((self.game_data.current_challenge, prediction))
        self._calculate_score()

    def get_control(self):
        return self.game_control.get(self.game_data)

    # private
    def _calculate_score(self):
        if self.game_data.has_ended():
            return
        score = Score(self.predictions, len(self.game_data.challenges), self.game_data.current_challenge)
        self.game_data.set_score(score)

    def _set_current_challenge(self):
        if self.game_data.has_ended():
            return
        duration_since_start = datetime.now() - self.game_data.start_time
        current_challenge_number = int(duration_since_start.total_seconds() / config.duration_one_challenge)
        current_challenge = self.game_data.challenges[current_challenge_number]
        self.game_data.set_current_challenge(current_challenge)

    def _set_end(self):
        self.game_data.set_end()


class GameData:
    def __init__(self):
        self.challenges = app_config.class_names
        self.start_time = None
        self.end_time = None
        self.current_challenge = ''
        self.score = Score([], len(self.challenges), self.current_challenge)
        self.remaining_seconds = 0

    def set_score(self, score):
        self.score = score

    def set_start(self):
        self.start_time = datetime.now()
        self.current_challenge = self.challenges[0]

    def set_current_challenge(self, current_challenge):
        self.current_challenge = current_challenge
        self.remaining_seconds = self.get_remaining_seconds()

    def set_end(self):
        if self.end_time is not None:
            return
        duration_since_start = datetime.now() - self.start_time
        if duration_since_start.total_seconds() > (len(self.challenges) * config.duration_one_challenge):
            self.end_time = datetime.now()

    def has_ended(self):
        return self.end_time is not None

    def is_started(self):
        return self.start_time is not None

    def get_remaining_seconds(self):
        duration_since_start = datetime.now() - self.start_time
        current_challenge_number = int(duration_since_start.total_seconds() / config.duration_one_challenge)
        return config.duration_one_challenge - int(duration_since_start.total_seconds() - config.duration_one_challenge * current_challenge_number)
