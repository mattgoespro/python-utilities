import os
import sys
from argparse import ArgumentParser

from PIL import Image


def convert_image_to_ico(
    input_path: str,
    output_file_name: str,
    output_dir: str,
):
    if not input_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        raise ValueError(
            f"Input image file must be a PNG, JPG, JPEG, BMP, or GIF file.\nGot: {os.path.split(".")[1]}"
        )

    img = Image.open(input_path)

    # ICO format requires an image of size (width, height) <= (256, 256)
    img = img.convert("RGBA")
    img_width = img.width
    img_height = img.height

    if img_width != img_height:
        raise ValueError("Image width and height must be equal.")

    if img.width > 256 or img.height > 256:
        img.thumbnail((256, 256))

    ico_output_file_path = os.path.join(output_dir, output_file_name)

    img.save(
        ico_output_file_path,
        format="ICO",
        sizes=[(img.width, img.height)],
    )

    return ico_output_file_path


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Convert an image to ICO format",
        add_help=True,
        usage="python image-to-ico.py -i <input_image_path> [-d <output_dir_path> -o <output_file_name>]",
    )
    parser.add_argument(
        "-i", help="Input image file path.", required=True, type=str, dest="image_input_path"
    )
    parser.add_argument(
        "-d",
        dest="ico_output_dir_path",
        type=str,
        help="Output directory.",
    )
    parser.add_argument(
        "-o",
        type=str,
        dest="ico_output_file_path",
        help="Output icon file name.",
    )

    args = parser.parse_args()
    print(args)

    input_image_path = args.image_input_path
    output_dir_path = args.ico_output_dir_path
    output_file_path = args.ico_output_file_path

    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Image file not found: {input_image_path}")

    if output_dir_path is None:
        output_dir_path = os.path.dirname(input_image_path)
    elif not os.path.exists(output_dir_path):
        raise FileNotFoundError(f"Output directory not found: {output_dir_path}")
    elif not os.path.isdir(output_dir_path):
        raise NotADirectoryError(f"Output path is not a directory: {output_dir_path}")

    if output_file_path is None:
        output_dir = os.path.dirname(input_image_path)
        input_image_name = os.path.basename(input_image_path).split(".")[0]
        output_file_path = os.path.join(output_dir, f"{input_image_name}.ico")

    try:
        converted_file_path = convert_image_to_ico(
            input_path=input_image_path,
            output_file_name=output_file_path,
            output_dir=output_dir_path,
        )

        print("Conversion successful.")
        print(f"ICO file saved to: {converted_file_path}")
        sys.exit(0)
    except Exception as error:
        print("Conversion failed.")
        print(f"Error: {error}")
        sys.exit(1)
