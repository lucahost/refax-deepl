import numpy as np
from pathlib import Path
import os
import shutil
import glob

pwd = os.getcwd()
dataset = f"{pwd}/train_set"
target_dir = f"{dataset}_keras"
classes = ["0", "1", "2", "3", "4", "5", "6", "7"]
number_images_to_process_per_class = 150_000

if not Path(dataset + "/images").is_dir():
    raise NotADirectoryError("images dir not found")

if not Path(dataset + "/annotations").is_dir():
    raise NotADirectoryError("annotations dir not found")

# ensure target dir and throw if it already exists
if Path(target_dir).is_dir():
    raise FileExistsError("Target dir already exists. Exiting")

Path(target_dir).mkdir(parents=True, exist_ok=True)

annotations_dir = dataset + "/annotations"

# load filenames of all expressions
expressions = glob.glob(f"{annotations_dir}/*_exp.npy", recursive=False)
# empty dictionary with classes as keys and filenames as values
classified_images = {key: list() for key in classes}

print("working through a total of " + str(len(expressions)) + " images")

# iterate filenames of expressions
for (i, image_expression_filename) in enumerate(expressions):

    if i % 100 == 0:
        # print percentage of expression progress
        print('Progress: {:.2f}'.format(i / len(expressions) * 100))

    # load from numpy file
    image_expression = np.load(image_expression_filename)
    # get first value (there is only one in this case)
    image_expression_val = image_expression.flat[0]
    # if it's not one of the defined discrete expressions abort here
    if int(image_expression_val) > 7:
        continue
    # add to the dictionary
    # {
    #   "0": ["filename1", "filename2", ...],
    #   "1": ["filename3", "filename4", ...],
    # }
    classified_images[image_expression_val].append(image_expression_filename)
    #if len(classified_images[image_expression_val]) < number_images_to_process_per_class:
    #    classified_images[image_expression_val].append(image_expression_filename)

# iterate all classes (0-7)
for class_key in classified_images.keys():
    # /abc/val_set_keras/0
    target_dir_class = target_dir + "/" + class_key
    Path(target_dir_class).mkdir(parents=True, exist_ok=True)
    # iterate expressions per class
    # expression_image_file = /abc/val_set/annotations/1234_exp.npy
    for expression_image_file in classified_images[class_key]:
        # image_filename = /abc/val_set/annotations/1234.jpg
        image_filename = expression_image_file[:-8] + ".jpg"
        # image_filename = /abc/val_set/images/1234.jpg
        image_filename = image_filename.replace("/annotations/", "/images/")
        # target_filename = 1234
        target_filename = Path(image_filename).stem
        # target_file = /abc/val_set_keras/0/1234.jpg
        target_file = f'{target_dir}/{class_key}/{target_filename}.jpg'
        shutil.copy(image_filename, target_file)
