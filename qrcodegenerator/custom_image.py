try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image
    import ImageDraw

import math
import random
import qrcode.image.base


class CustomImage(qrcode.image.base.BaseImage):
    kind = 'PNG'

    def new_image(self, **kwargs):
        back_color = kwargs.get('back_color', 'white')
        fill_color = kwargs.get('fill_color', 'black')
        self.body = kwargs.get('body', 'square')
        self.version = kwargs.get('version', 3)
        self.eye = kwargs.get('eye', 'eye0')
        self.eye_ball = kwargs.get('eye_ball', 'ball0')

        if fill_color.lower() != 'black' or back_color.lower() != 'white':
            if back_color.lower() == 'transparent':
                mode = 'RGBA'
                back_color = None
            else:
                mode = 'RGB'
        else:
            mode = '1'
            if fill_color.lower() == 'black': fill_color = 0
            if back_color.lower() == 'white': back_color = 255

        img = Image.new(mode, (self.pixel_size, self.pixel_size), back_color)
        self.fill_color = fill_color
        self.idr = ImageDraw.Draw(img)
        return img

    def drawrect(self, row, col):
        star = [(0.5, 0), (0.677, 0.29), (0.975, 0.345), (0.785, 0.593), (0.809, 0.91),
                  (0.5, 0.8), (0.191, 0.91), (0.215, 0.593), (0.025, 0.345), (0.323, 0.29)]

        if (row == 3 and col == 3) or (row == 3 and col == (17 + self.version * 4 - 4)) or (
                row == (17 + self.version * 4 - 4) and col == 3):
            if self.eye_ball == 'ball0':
                x = (col + self.border) * self.box_size - self.box_size
                y = (row + self.border) * self.box_size - self.box_size
                self.idr.rectangle([(x, y), (x + self.box_size * 3, y + self.box_size * 3)], fill=self.fill_color)
            elif self.eye_ball == 'ball1':
                x = (col + self.border) * self.box_size - self.box_size
                y = (row + self.border) * self.box_size - self.box_size
                self.idr.ellipse([(x, y), (x + self.box_size * 3, y + self.box_size * 3)], fill=self.fill_color)
            elif self.eye_ball == 'ball2':
                x = (col + self.border) * self.box_size - self.box_size
                y = (row + self.border) * self.box_size - self.box_size
                coords = self.calculate_regular_pentagon_coords(x, y, self.box_size * 3)
                self.idr.polygon(coords, fill=self.fill_color)

            elif self.eye_ball == 'ball3':
                x = (col + self.border) * self.box_size - self.box_size
                y = (row + self.border) * self.box_size - self.box_size
                coords = self.calculate_regular_hexagon_coords(x, y, self.box_size * 3)
                self.idr.polygon(coords, fill=self.fill_color)

        elif (row, col) in [(2, 2), (3, 2), (4, 2),
                            (2, 3), (2, 4), (4, 4),
                            (3, 4), (4, 3),
                            ((17 + self.version * 4) - 2, 2), ((17 + self.version * 4) - 3, 2),
                            ((17 + self.version * 4) - 4, 2),
                            ((17 + self.version * 4) - 2, 3), ((17 + self.version * 4) - 2, 4),
                            ((17 + self.version * 4) - 4, 4),
                            ((17 + self.version * 4) - 3, 4), ((17 + self.version * 4) - 4, 3),
                            ((17 + self.version * 4) - 5, 2), ((17 + self.version * 4) - 5, 3),
                            ((17 + self.version * 4) - 5, 4), ((17 + self.version * 4) - 3, 3),
                            (2, (17 + self.version * 4) - 2), (3, (17 + self.version * 4) - 2),
                            (4, (17 + self.version * 4) - 2),
                            (2, (17 + self.version * 4) - 3), (2, (17 + self.version * 4) - 4),
                            (4, (17 + self.version * 4) - 4),
                            (3, (17 + self.version * 4) - 4), (4, (17 + self.version * 4) - 3),
                            (2, (17 + self.version * 4) - 5), (3, (17 + self.version * 4) - 5),
                            (4, (17 + self.version * 4) - 5), (3, (17 + self.version * 4) - 3)]:
            pass

        elif (row < 7 and col < 7) or (row < 7 and col > (17 + self.version * 4 - 8)) or (
                row > (17 + self.version * 4 - 8) and col < 7):
            if self.eye == 'eye0':
                x = (col + self.border) * self.box_size
                y = (row + self.border) * self.box_size
                self.idr.rectangle([(x, y), (x + self.box_size, y + self.box_size)], fill=self.fill_color)
            elif self.eye == 'eye1':
                x = (col + self.border) * self.box_size
                y = (row + self.border) * self.box_size
                self.idr.ellipse([(x, y), (x + self.box_size, y + self.box_size)], fill=self.fill_color)
            elif self.eye == 'eye2':
                x = (col + self.border) * self.box_size
                y = (row + self.border) * self.box_size
                coords = self.calculate_regular_pentagon_coords(x, y, self.box_size)
                self.idr.polygon(coords, fill=self.fill_color)
            elif self.eye == 'eye3':
                x = (col + self.border) * self.box_size
                y = (row + self.border) * self.box_size
                coords = self.calculate_regular_hexagon_coords(x, y, self.box_size)
                self.idr.polygon(coords, fill=self.fill_color)

        else:
            if self.body == 'square':
                x = (col + self.border) * self.box_size
                y = (row + self.border) * self.box_size
                self.idr.rectangle([(x, y), (x + self.box_size, y + self.box_size)], fill=self.fill_color)
            elif self.body == 'point':
                x = (col + self.border) * self.box_size
                y = (row + self.border) * self.box_size
                self.idr.ellipse([(x, y), (x + self.box_size, y + self.box_size)], fill=self.fill_color)
            elif self.body == 'star':
                x = (col + self.border) * self.box_size
                y = (row + self.border) * self.box_size
                coords = [(int(x + p[0] * self.box_size), int(y + p[1] * self.box_size)) for p in star]
                self.idr.polygon(coords, fill=self.fill_color)

            elif self.body == 'irregular_square':
                x = (col + self.border) * self.box_size
                y = (row + self.border) * self.box_size
                coords = self.calculate_irregular_square_coords(x, y, self.box_size * 3)
                self.idr.polygon(coords, fill=self.fill_color)

    def calculate_regular_pentagon_coords(self, x, y, side_length):
        coords = []
        angle = -math.pi / 2  # Starting angle at the top vertex of the pentagon

        for _ in range(5):
            px = x + side_length / 2 + math.cos(angle) * side_length / 2
            py = y + side_length / 2 + math.sin(angle) * side_length / 2
            coords.append((int(px), int(py)))

            angle += (2 * math.pi) / 5  # Increment angle by 72 degrees (2*pi/5 radians)
        return coords

    def calculate_regular_hexagon_coords(self, x, y, side_length):
        coords = []
        angle = -math.pi / 2  # Starting angle at the top vertex of the hexagon

        for i in range(6):
            if i == 0 or i == 5:
                px = x + side_length / 2
                py = y
            elif i == 1 or i == 4:
                px = x + side_length
                py = y + side_length / 2
            elif i == 2 or i == 3:
                px = x + side_length / 2
                py = y + side_length

            coords.append((int(px), int(py)))

            angle += (2 * math.pi) / 6  # Increment angle by 60 degrees (2*pi/6 radians)

        return coords

    def calculate_irregular_square_coords(self, x, y, size):
        # Calculate the coordinates for an irregular square shape
        coords = [
            (x + size * 0.5, y),
            (x + size, y + size * 0.25),
            (x + size, y + size * 0.75),
            (x + size * 0.5, y + size),
            (x, y + size * 0.75),
            (x, y + size * 0.25)
        ]
        return coords

    def save(self, stream, format=None, **kwargs):
        if format is None:
            format = kwargs.get('kind', self.kind)
        if 'kind' in kwargs:
            del kwargs['kind']
        self._img.save(stream, format=format, **kwargs)

    def __getattr__(self, name):
        return getattr(self._img, name)
