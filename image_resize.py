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


def check_args(height, width, scale, output_dir, input_image_path, parser):
    if not(height or width or scale):
        parser.error("Параметры не введены")
    if output_dir and not (os.path.isdir(output_dir)):
        parser.error("Такой директории не существует")
    if not (os.path.exists(input_image_path)):
        parser.error("Файла не сущетсвует")
    if scale and (width or height):
        parser.error(
            "Ошибка! Невозможно задать высоту, ширину и масштаб одновременно"
        )


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
        target_size = (width, height)
        return target_size
    elif width:
        target_size = (
            width,
            int((get_ratio(width, width_original))*height_original)
        )
        return target_size
    elif height:
        target_size = (
            int((get_ratio(height, height_original))*width_original),
            height
        )
        return target_size
    elif scale:
        target_size = (int(scale*width_original), int(scale*height_original))
        return target_size


def get_output_path(target_size, output_dir, input_image_path):
    extension = os.path.splitext(input_image_path)[1]
    if output_dir is None:
        output_dir = os.getcwd()
    output_image_path = os.path.join(
        output_dir,
        os.path.splitext(input_image_path)[0]
    )
    out_image = "{}__{}x{}{}".format(
        output_image_path,
        target_size[0],
        target_size[1],
        extension
    )
    return out_image


def resize_image(output_image_path, target_size):
    resized_image = orig_img.resize(target_size, Image.ANTIALIAS)
    resized_image.save(output_image_path)


if __name__ == "__main__":
    parser = create_parser()
    parsargs = parser.parse_args()
    scale, input_image_path, output_dir = (
        parsargs.scale,
        parsargs.input,
        parsargs.output
    )
    width, height = (parsargs.width, parsargs.height)
    check_args(height, width, scale, output_dir, input_image_path, parser)
    orig_img = Image.open(input_image_path)
    if width and height:
        if is_ratio_changed(orig_img.size[0], orig_img.size[1], width, height):
            print("Изображение может быть непропорциональным")
    target_size = get_sizes(scale, orig_img.size, width, height)
    output_image_path = get_output_path(
        target_size,
        output_dir,
        input_image_path
    )
    resize_image(output_image_path, target_size)
    print("Готово!")
