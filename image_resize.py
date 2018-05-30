from PIL import Image
import argparse
import os
import logging


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--scale", type=float)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    return parser


def open_image(input_image_path):
    original_image = Image.open(input_image_path)
    return original_image.size


def get_ratio(new_size, original_size):
    ratio = (new_size / float(original_size))
    return ratio


def is_ratio_changed(width_original, height_orignal, width, height):
    permissible_error = 0.005
    proportion_change = width / width_original - height / height_orignal
    return abs(proportion_change) > permissible_error


def get_sizes(scale, original_sizes, width=None, height=None):
    width_original, height_original = original_sizes
    if (width and height):
        max_size = (width, height)
        if is_ratio_changed(width_original, height_original, width, height):
            logging.warning("Изображение может быть непропорциональным")
        return max_size
    elif width:
        max_size = (
            width,
            int((get_ratio(width, width_original))*height_original)
        )
        return max_size
    elif height:
        max_size = (
            int((get_ratio(height, height_original))*width_original),
            height
        )
        return max_size
    elif scale:
        max_size = (int(scale*width_original), int(scale*height_original))
        return max_size


def get_output_path():
    if parsargs.output:
        output_dir = parsargs.output
        output_image_path = os.path.join(
            output_dir,
            os.path.splitext(input_image_path)[0]
        )
    elif parsargs.output is None:
        output_dir = os.getcwd()
        output_image_path = os.path.join(
            output_dir,
            os.path.splitext(input_image_path)[0]
        )
    out_image = "{}__{}x{}.jpg".format(
        output_image_path,
        max_size[0],
        max_size[1]
    )
    return out_image


def scale_by_resize(output_image_path, max_size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(max_size, Image.ANTIALIAS)
    resized_image.save(output_image_path)


if __name__ == "__main__":
    parser = create_parser()
    parsargs = parser.parse_args()
    scale, input_image_path, width, height = (
        parsargs.scale,
        parsargs.input,
        parsargs.width,
        parsargs.height
    )

    if not(os.path.exists(parsargs.input)):
        exit("Файла не сущетсвует")
    if scale and (width or height):
        exit("Ошибка!")
    original_sizes = open_image(input_image_path)
    max_size = get_sizes(scale, original_sizes, width, height)
    output_image_path = get_output_path()
    scale_by_resize(output_image_path, max_size)
    print("Готово!")
