import PIL.Image
import cv2
from PIL import Image, ImageDraw
from moduls.config import app_config, german_moods
from numpy import asarray

config = app_config.game_config.game_control_config




class GameControl:
    def __init__(self):
        self.total_str = '0'
        self.current_score_control = SingleBarControl()
        self.global_score_control = SingleBarControl()

    def get(self, game_data):
        score = game_data.score
        self.total_str = str(int(game_data.score.global_score * 1000)) +'/1000'
        current_text = german_moods[score.current_challenge]
        self.current_score_control.update(score.current_score, current_text )
        self.global_score_control.update(score.global_score, 'Total: ' + self.total_str)

        im = Image.new('RGB', config.control_size, config.background_color)
        ImageDraw.Draw(im)
        im = asarray(im).copy()

        text_height = self._put_info_text_on_image(game_data,im) + 25
        if not game_data.is_started():
            im = im[0:int(text_height),0:config.control_size[0]]

        current_control = (self.current_score_control.get(), config.upper_left_current)
        total_control = (self.global_score_control.get(), config.upper_left_total)
        add_image(current_control, im)
        add_image(total_control, im)
        return im, config.upper_left

    def _put_info_text_on_image(self,game_data,im):
        font = cv2.FONT_HERSHEY_SIMPLEX
        game_text = self._get_info_text(game_data)
        textsize = cv2.getTextSize(game_text, font, 1, 2)[0]
        x_middle = int((im.shape[1] - textsize[0]) / 2)
        cv2.putText(im, game_text, (x_middle, 25), font, 1, config.text_color, 2)
        return textsize[1]

    def _get_info_text(self, game_data):
        if game_data.start_time is None:
            return 'Zeigefinger hier zum starten'
        if game_data.has_ended():
            return "Fertig - Endergebnis: " + self.total_str
        return "schau " + german_moods[game_data.current_challenge] + "!" + ' ' + str(game_data.remaining_seconds)


class SingleBarControl:
    def __init__(self):
        self.value = 0
        self.label = '-----'

    def get(self):
        _config = config.single_bar_control_config

        im = Image.new('RGB', _config.size, _config.background_color)
        draw = ImageDraw.Draw(im)

        inner_width = _config.bar_size[0] - 2 * _config.border
        width = inner_width * self.value / _config.max_value
        if width > inner_width:
            width = inner_width

        label_width = _config.size[0] - _config.bar_size[0]
        draw.rectangle(
            (_config.border + label_width, _config.border, _config.bar_size[0] - _config.border + label_width,
             _config.bar_size[1] - _config.border), outline=_config.bar_box_color)
        draw.rectangle(
            (_config.border + label_width, _config.border, _config.border + width + label_width,
             _config.bar_size[1] - _config.border),
            fill=_config.bar_color)

        text = ' ' + self.label
        draw.text((_config.border, 5), text, _config.text_color)
        return im

    def update(self, value, label):
        self.value = value
        self.label = label


def add_image(control, background):
    _background = background
    if control is None:
        return
    img = control[0]
    startpoint = control[1]
    if img is None:
        return


    size = img.size if type(img) == PIL.Image.Image else (img.shape[1], img.shape[0])
    x = startpoint[0]
    y = startpoint[1]
    try:
        background[y: size[1] + y, x:size[0] + x] = img
        return background
    except:
        print('add_image error')
        print(img)
        return _background


