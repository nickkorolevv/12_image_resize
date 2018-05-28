from PIL import Image
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--scale", type=float)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    return parser


def scale_image(input_image_path, output_image_path, scale):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    print("Исходное изображение {}x{}".format(width, height))
    new_size = (int(scale*width), int(scale*height))
    resized_image = original_image.resize(new_size, Image.ANTIALIAS)
    out_image_path = "{}{}x{}.jpg".format(
        output_image_path,
        new_size[0],
        new_size[1]
    )
    resized_image.save(out_image_path)
    scaled_image = Image.open(out_image_path)
    new_width, new_height = scaled_image.size
    print("Формат полученного изображения {}x{}".format(new_width, new_height))


def scale_by_wh(input_image_path, output_image_path, width, height):
    original_image = Image.open(input_image_path)
    width_original, height_original = original_image.size
    print("Исходное изображение {}x{}".format(width_original, height_original))
    max_size = (width, height)
    print("Возможно изображение будет непропорциальным")
    resized_image = original_image.resize(max_size, Image.ANTIALIAS)
    out_image_path = "{}{}x{}.jpg".format(
        output_image_path,
        max_size[0],
        max_size[1]
    )
    resized_image.save(out_image_path)
    scaled_image = Image.open(out_image_path)
    width, height = scaled_image.size
    print("Формат полученного изображения {}x{}".format(width, height))


def resize_image(input_image_path, output_image_path, width=None, height=None):
    original_image = Image.open(input_image_path)
    width_original, height_original = original_image.size
    print("Исходное изображение {}x{}".format(width_original, height_original))
    if width:
        max_size = (width, height_original)
    elif height:
        max_size = (width_original, height)
    else:
        raise RuntimeError("Ширина или высота не заданы!")
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    out_image_path = "{}{}x{}.jpg".format(
        output_image_path,
        max_size[0],
        max_size[1]
    )
    original_image.save(out_image_path)
    scaled_image = Image.open(out_image_path)
    width, height = scaled_image.size
    print("Формат полученного изображения {}x{}".format(width, height))


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args()
    scale = namespace.scale
    input_image_path = namespace.input
    width = namespace.width
    height = namespace.height
    if namespace.output is None:
        output_image_path = "{}__".format(input_image_path[:-4])
    output_image_path = "{}\{}__".format(
        namespace.output,
        input_image_path[:-4]
    )
    if (scale and width and height):
        exit("Ошибка")
    if scale:
        scale_image(input_image_path, output_image_path, scale)
    elif (width and height):
        scale_by_wh(input_image_path, output_image_path, width, height)
    elif (width or height):
        resize_image(input_image_path, output_image_path, width, height)
