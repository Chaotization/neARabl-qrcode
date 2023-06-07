import qrcode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from math import atan2
from colorsys import rgb_to_hls, hls_to_rgb
from qrcodegenerator.custom_image import CustomImage


def generate_qr_code(data, version=None, border=None, box_size=None, icon_path=None, scale=0.2,
                     fill_color_1=None, fill_color_2=None):
    if fill_color_1 is None and fill_color_2 is None:
        fill_color = "black"
    elif fill_color_1 is not None and fill_color_2 is None:
        fill_color = fill_color_1
    elif fill_color_1 is None and fill_color_2 is not None:
        fill_color = fill_color_2
    else:
        color_1 = ImageColor.getrgb(fill_color_1)
        color_2 = ImageColor.getrgb(fill_color_2)
        blended_color = blend_colors(color_1, color_2)
        fill_color = '#{:02x}{:02x}{:02x}'.format(*blended_color)

    qr = qrcode.QRCode(version=version, box_size=box_size, border=border, image_factory=CustomImage)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color="white", body="point",
                        version=version, eye_ball="ball1", eye="eye1")
    img.save('qrcode.png')

    if icon_path:
        logo = Image.open(icon_path)
        logo_width, logo_height = logo.size
        logo_width_scaled = int(logo_width * scale)
        logo_height_scaled = int(logo_height * scale)

        pixel_size = (18 + version * 4 + 3 * border) * box_size

        logo_x = int((pixel_size - logo_width_scaled) / 2)
        logo_y = int((pixel_size - logo_height_scaled) / 2)

        box_width = int(logo_width_scaled * 0.8)
        box_height = logo_height_scaled
        border_size = 3

        box_image = Image.new("RGBA", (box_width, box_height), (255, 255, 255, 255))
        border_image = Image.new("RGBA", (box_width + 2 * border_size, box_height + 2 * border_size),
                                 (255, 255, 255, 255))
        border_image.paste(box_image, (border_size, border_size))

        logo_resized = logo.resize((int(box_width * 1.186), box_height), resample=Image.LANCZOS)

        with img.convert("RGBA") as im:
            im.paste(border_image, (logo_x - border_size, logo_y - border_size), border_image)
            im.paste(logo_resized, (logo_x, logo_y), logo_resized)
            im.save("qrcodex.png")

    return img


def blend_colors(color1, color2):
    # Convert RGB values to floats between 0 and 1
    if color1 == (255, 0, 0) and color2 == (0, 255, 0):
        return (255, 255, 0)
    elif color1 == (0, 255, 0) and color2 == (255, 0, 0):
        return (255, 255, 0)
    else:
        color1 = [x / 255 for x in color1]
        color2 = [x / 255 for x in color2]

        # Convert RGB to HSL
        h1, l1, s1 = rgb_to_hls(*color1)
        h2, l2, s2 = rgb_to_hls(*color2)

        # Compute average hue value
        h = (h1 + h2) / 2

        # Blend saturation and lightness values
        s = (s1 + s2) / 2
        l = (l1 + l2) / 2

        # Convert blended HSL back to RGB
        blended_color = hls_to_rgb(h, l, s)

        # Convert RGB values back to integers between 0 and 255
        blended_color = tuple(int(x * 255) for x in blended_color)
        return blended_color

# def blend_colors(color1, color2):
#     blended_color = (
#         int((color1[0] + color2[0]) / 2),
#         int((color1[1] + color2[1]) / 2),
#         int((color1[2] + color2[2]) / 2)
#     )
#     return blended_color