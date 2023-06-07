import qrcode
from PIL import Image
from qrcode.image.pil import PilImage
from PIL import ImageDraw
from PIL import ImageColor
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
        # Combine the two colors into a new color using the "screen" blending mode
        color_1 = ImageColor.getrgb(fill_color_1)
        color_2 = ImageColor.getrgb(fill_color_2)
        blended_color = blend_colors(color_1, color_2)
        fill_color = '#{:02x}{:02x}{:02x}'.format(*blended_color)

    qr = qrcode.QRCode(version=version, box_size=box_size, border=border, image_factory=PilImage)
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
    blended_color = (
        int((color1[0] + color2[0]) / 2),
        int((color1[1] + color2[1]) / 2),
        int((color1[2] + color2[2]) / 2)
    )
    return blended_color