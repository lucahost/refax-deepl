import cv2
import numpy as np
import matplotlib.pyplot as plt
from .config import app_config as config

lastImg = None


def radarChartImage(values):
    global lastImg
    if values is None:
        return lastImg

    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(config.class_names), endpoint=False)

    fig = plt.figure(figsize=(8, 8))
    plt.subplot(polar=True)
    plt.plot(label_loc, values, label='xyz')
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=config.class_names)
    plt.legend()

    fig.canvas.draw()

    # convert canvas to image
    lastImg = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    lastImg = lastImg.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    lastImg = cv2.cvtColor(lastImg, cv2.COLOR_RGB2BGR)
    lastImg = cv2.resize(lastImg, dsize=config.predControlSize, interpolation=cv2.INTER_CUBIC)
    return lastImg, config.radar_control_upper_left


def barImage(values):
    global lastImg
    if values is None:
        return lastImg

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = ['0', '1', '2', '3', '4', '5', '6', '7']
    students = values
    ax.bar(langs, students)
    fig.canvas.draw()

    # convert canvas to image
    lastImg = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    lastImg = lastImg.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    lastImg = cv2.cvtColor(lastImg, cv2.COLOR_RGB2BGR)
    lastImg = cv2.resize(lastImg, dsize=config.predControlSize, interpolation=cv2.INTER_CUBIC)
    return lastImg
