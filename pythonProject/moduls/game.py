from datetime import datetime
from .config import class_names
from PIL import Image, ImageDraw

class SingleBarControl:
    border = 5

    def __init__(self):
        self.value = 0
        self.label = '-----'

        self.max = 0.5
        self.bar_size = (200, 30)
        self.control_size = (300, 30)
        self.border = 5


    def get(self):
        im = Image.new('RGB', self.control_size, (128, 128, 128))
        draw = ImageDraw.Draw(im)

        inner_width = self.bar_size[0] - 2 * self.border
        width = inner_width * self.value / self.max
        labelWidth = self.control_size[0] - self.bar_size[0]
        draw.rectangle((self.border + labelWidth, self.border, self.bar_size[0] - self.border + labelWidth,
                        self.bar_size[1] - self.border), outline=(255, 255, 255))
        draw.rectangle(
            (self.border + labelWidth, self.border, self.border + width + labelWidth, self.bar_size[1] - self.border),
            fill=(255, 0, 0))

        draw.text((self.border, 5), self.label, (255, 255, 255))  # ,font=font)
        return im

    def update(self,value,label):
        self.value = value
        self.label = label

class Game:
    def __init__(self):
        self.end_time = None
        self.start_time = None
        self.challenges = class_names
        self.predictions = []
        self.score_global = 0
        self.score_current_challenge = 0
        self.current_challenge_number = 0
        self.current_challenge = ''
        self.scores = []
        # config
        self.config_duration_one_challenge = 10

        # controls
        self.current_score_control = SingleBarControl()
        self.global_score_control = SingleBarControl()

    def start(self):
        self.start_time = datetime.now()
        self.current_challenge = self.challenges[0]

    def add_prediction(self, prediction):
        if prediction is None:
            return
        if len(prediction) == 0:
            return
        self.set_end()
        x = self.current_challenge_number
        self.set_current_challenge()
        self.predictions.append((self.current_challenge, prediction))
        self.calculate_scores()

        if x != self.current_challenge_number:
            return
    def getInfoText(self):
        if self.start_time is None:
            return
        if self.end_time is not None:
            return "You finished the Game"
        return "show " + self.current_challenge + "!"

    def get_controls(self):
        self.current_score_control.update(self.score_current_challenge,self.current_challenge)
        self.global_score_control.update(self.score_global, 'Global')
        return self.current_score_control.get(), self.global_score_control.get()

    # private
    def calculate_scores(self):
        if self.end_time is not None:
            return

        challenges = set(map(lambda x: x[0], self.predictions))
        grouped = [[y for y in self.predictions if y[0] == x] for x in challenges]

        # score_global
        self.scores = [ChallengeScore(prediction) for prediction in grouped]
        score_sum = sum([score.score for score in self.scores])
        self.score_global = score_sum / len(self.challenges)

        # score_current_challenge
        current = None
        for score in self.scores:
            if score.challenge == self.current_challenge:
                current = score
        self.score_current_challenge = current.score

    def set_current_challenge(self):
        if self.end_time is not None:
            return

        duration_since_start = datetime.now() - self.start_time
        self.current_challenge_number = int(duration_since_start.total_seconds() / self.config_duration_one_challenge)
        self.current_challenge = self.challenges[self.current_challenge_number]


    def set_end(self):
        if self.end_time is not None:
            return

        duration_since_start = datetime.now() - self.start_time
        if duration_since_start.total_seconds() > (len(self.challenges) * self.config_duration_one_challenge):
            self.end_time = datetime.now()
            print("Ende")


class ChallengeScore:
    def __init__(self, predictions):
        self.challenge = predictions[0][0]
        challenge_number = class_names.index(self.challenge)
        values = [x[1][challenge_number] for x in predictions]
        self.score = sum(values) / len(values)


testData = [('0', 0.5), ('0', 0.2), ('0', 0.4), ('1', 0.6), ('1', 0.7)]
