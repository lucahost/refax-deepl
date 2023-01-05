german_moods = {
    'Neutral': 'neutral',
    'Happy': 'gluecklich',
    'Sad': 'traurig',
    'Surprise': 'ueberrascht',
    'Fear': 'aengstlich',
    'Disgust': 'angewidert',
    'Anger': 'wuetend',
    'Contempt': 'verachtend',
    '': ''
}


class AppConfig:
    def __init__(self):
        class_names = ['Neutral', 'Happy', 'Sad', 'Surprise', 'Fear', 'Disgust', 'Anger', 'Contempt']

        self.class_names = sorted(class_names)
        self.app_size = (2000, 1000)
        self.predControlSize = (400, 400)
        self.radar_control_upper_left = (0, 0)
        self.game_config = GameConfig(self.app_size)


class GameConfig:
    def __init__(self, app_size):
        self.duration_one_challenge = 6
        self.game_control_config = GameControlConfig(app_size)


class GameControlConfig:
    def __init__(self, app_size):
        control_top_distance = 10
        label_height = 50
        space = 5
        width = 800

        self.text_color = (0, 0, 255)
        self.background_color = (255, 255, 255)
        self.single_bar_control_config = SingleBarControlConfig(width)
        single_bar_height = self.single_bar_control_config.height
        self.upper_left_current = (0, label_height + space)
        self.upper_left_total = (0, label_height + single_bar_height + space)

        height = label_height + space + self.single_bar_control_config.bar_size[1] * 2
        self.control_size = (width, height)
        self.upper_left = self.get_upper_left(app_size, control_top_distance)
        lower_right = (self.upper_left[0] + width, self.upper_left[1] + height)
        self.rectangle = (self.upper_left, lower_right)

    def get_upper_left(self, app_size, control_top_distance):
        x_for_middle = int(app_size[0] / 2 - self.control_size[0] / 2)
        return x_for_middle, control_top_distance


class SingleBarControlConfig:
    def __init__(self, main_width):
        label_width = 100
        self.text_color = (0, 0, 255)
        self.background_color = (255, 255, 255)
        self.bar_box_color = (0, 0, 0)
        self.bar_color = (255, 0, 0)
        self.height = 30
        self.max_value = 0.5
        self.border = 5
        self.bar_size = (main_width - label_width, self.height)
        self.size = (main_width, self.height)


app_config = AppConfig()
