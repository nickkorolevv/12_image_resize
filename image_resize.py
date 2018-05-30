from PIL import Image
import argparse
import os


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--scale", type=float)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    return parser


def check_input(parsargs):
    if not(parsargs.height or parsargs.width or parsargs.scale):
        return None
    else:
        return parsargs

def check_path():
    pass

def get_original_sizes():
    return orig_img.size


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
        created_size = (width, height)
        if is_ratio_changed(orig_img.size[0], orig_img.size[1], width, height):
            print("Изображение может быть непропорциональным")
        return created_size
    elif width:
        created_size = (
            width,
            int((get_ratio(width, width_original))*height_original)
        )
        return created_size
    elif height:
        created_size = (
            int((get_ratio(height, height_original))*width_original),
            height
        )
        return created_size
    elif scale:
        created_size = (int(scale*width_original), int(scale*height_original))
        return created_size


def get_output_path(created_size, output_dir):
    if output_dir:
        output_image_path = os.path.join(
            output_dir,
            os.path.splitext(input_image_path)[0]
        )
    elif output_dir is None:
        output_dir = os.getcwd()
        output_image_path = os.path.join(
            output_dir,
            os.path.splitext(input_image_path)[0]
        )
    out_image = "{}__{}x{}.jpg".format(
        output_image_path,
        created_size[0],
        created_size[1]
    )
    return out_image


def change_image(output_image_path, created_size):
    resized_image = orig_img.resize(created_size, Image.ANTIALIAS)
    resized_image.save(output_image_path)


if __name__ == "__main__":
    parser = create_parser()
    parsargs = parser.parse_args()
    scale, input_image_path, output_dir = (parsargs.scale, parsargs.input, parsargs.output)
    width, height = (parsargs.width, parsargs.height)
    orig_img = Image.open(input_image_path)
    if check_input(parsargs) is None:
        exit("Параметры не введены")
    if output_dir and not(os.path.isdir(output_dir)):
        exit("Такой директории не существует")
    if not(os.path.exists(parsargs.input)):
        exit("Файла не сущетсвует")
    if scale and (width or height):
        exit("Ошибка! Невозможно задать высоту, ширину и масштаб одновременно")
    created_size = get_sizes(scale, orig_img.size, width, height)
    output_image_path = get_output_path(created_size, output_dir)
    change_image(output_image_path, created_size)
    print("Готово!")
