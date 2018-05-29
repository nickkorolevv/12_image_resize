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


def get_sizes(input_image_path, width, height, scale):
    original_image = Image.open(input_image_path)
    width_original, height_original = original_image.size
    if (width and height):
        max_size = (width, height)
        logging.warning("Изображение может быть непропорциональным")
        return max_size
    elif width:
        max_size = (width, height_original)
        return max_size
    elif height:
        max_size = (width_original, height)
        return max_size
    elif scale:
        max_size = (int(scale*width_original), int(scale*height_original))
        return max_size


def scale_by_resize(output_image_path, max_size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(max_size, Image.ANTIALIAS)
    out_image_path = "{}{}x{}.jpg".format(
        output_image_path,
        max_size[0],
        max_size[1]
    )
    resized_image.save(out_image_path)


def scale_by_thumbnail(output_image_path, max_size):
    original_image = Image.open(input_image_path)
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    out_image_path = "{}{}x{}.jpg".format(
        output_image_path,
        max_size[0],
        max_size[1]
    )
    original_image.save(out_image_path)


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args()
    scale, input_image_path, width, height = (
        namespace.scale,
        namespace.input,
        namespace.width,
        namespace.height
    )
    if not(os.path.exists(namespace.input)):
        exit("Файла не сущетсвует")
    if namespace.output is None:
        output_dir = os.getcwd()
        output_image_path = os.path.join(
            output_dir,
            os.path.splitext(input_image_path)[0]
        )
    else:
        output_dir = namespace.output
        output_image_path = os.path.join(
            output_dir,
            os.path.splitext(input_image_path)[0]
        )
    if not(os.path.isdir(output_dir)):
        exit("Директории не существует")
    max_size = get_sizes(input_image_path, width, height, scale)
    if (width and height) or scale:
        if (width and height and scale):
            exit("Ошибка!")
        scale_by_resize(output_image_path, max_size)
    elif (width or height):
        scale_by_thumbnail(output_image_path, max_size)
