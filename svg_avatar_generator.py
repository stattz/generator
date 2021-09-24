import svgwrite
import random
import math
import uuid

# https://github.com/georgedoescode/splinejs/blob/main/spline.js


def spline(points=[], tension=1):
  size = len(points)

  path = f'M {points[0]} {points[1]}'

  for i in range(0, size, 2):
    x0 = points[(i - 2) % size]
    y0 = points[(i - 1) % size]

    x1 = points[i + 0]
    y1 = points[i + 1]

    x2 = points[(i + 2) % size]
    y2 = points[(i + 3) % size]

    x3 = points[(i + 4) % size]
    y3 = points[(i + 5) % size]

    cp1x = x1 + ((x2 - x0) / 6) * tension
    cp1y = y1 + ((y2 - y0) / 6) * tension

    cp2x = x2 - ((x3 - x1) / 6) * tension
    cp2y = y2 - ((y3 - y1) / 6) * tension

    path += f' C {cp1x} {cp1y} {cp2x} {cp2y} {x2} {y2}'

  return path


class SvgGroupElement:
    def __init__(self, drawing, x_pos, y_pos, rnd):
        self.drawing = drawing
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rnd = rnd
        self.group = None
        self.mask_uri = ''
        self.clip_path_uri = ''

    def get_unique_id(self):
        return uuid.UUID(int=self.rnd.getrandbits(128), version=4)

    def add_mask(self, mask):
        self.mask_id = self.get_unique_id()
        self.mask_uri = f'uri(#{self.mask_id})'
        self.mask = self.drawing.mask(id=self.mask_id)
        self.mask.add(mask)

    def add_clip_path(self, clip_path):
        self.clip_path_id = self.get_unique_id()
        self.clip_path_uri = f'uri(#{self.clip_path_id})'
        self.clip_path = self.drawing.clipPath(id=self.clip_path_id)
        self.clip_path.add(clip_path)

    def add(self, element):
        if self.group is None:
            # clip_path=self.clip_path_uri,
            # mask=self.mask_uri
            self.group = self.drawing.g(
                transform=f'translate({self.x_pos}, {self.y_pos})')

        self.group.add(element)

    def add_circle(self, center, r, **extra):
        self.add(svgwrite.shapes.Circle(center, r, **extra))

    def add_path(self, points, **extra):
        self.add(self.drawing.path(points, **extra))

    def generate(self):
        return self.group


class Eye(SvgGroupElement):
    def __init__(self, drawing, x_pos, y_pos, size, rnd):
        super().__init__(drawing, x_pos, y_pos, rnd)

        self.size = size

    def generate(self):
        self.add_circle(center=(0, 0), r=self.size,
                        stroke='black', fill='white')
        self.add_circle(center=(0, 0), r=self.size/2, fill='black')
        return super().generate()


class Eyes(SvgGroupElement):
    def __init__(self, drawing, x_pos, y_pos, maxWidth, rnd):
        super().__init__(drawing, x_pos, y_pos, rnd)

        self.maxWidth = maxWidth

    def generate(self):
        isCyclops = self.rnd.random() > 0.75

        eyeSize = self.rnd.uniform(self.maxWidth / 2, self.maxWidth)

        if isCyclops:
            eye = Eye(self.drawing, 0, 0, eyeSize, self.rnd)
            self.add(eye.generate())
        else:
            eye = Eye(self.drawing, -1 * self.maxWidth, 0, eyeSize, self.rnd)
            self.add(eye.generate())

            eye = Eye(self.drawing, self.maxWidth, 0, eyeSize, self.rnd)
            self.add(eye.generate())

        return super().generate()


class Face(SvgGroupElement):
    def __init__(self, drawing, x_pos, y_pos, size, rnd):
        super().__init__(drawing, x_pos, y_pos, rnd)

        self.size = size

    def generateFacePoints(self):
        numPoints = self.rnd.randrange(4, 12)
        angleStep = (math.pi * 2) / numPoints

        points = []

        for i in range(numPoints):
            pull = self.rnd.uniform(0.75, 1)

            x = math.cos(i * angleStep) * (self.size * pull)
            y = math.sin(i * angleStep) * (self.size * pull)

            points.append(x)
            points.append(y)

        return spline(points, 1)

    def generate(self):
        self.add_path(self.generateFacePoints(), fill='blue', stroke='black')

        eyes = Eyes(self.drawing, 0, 0, self.size / 3, self.rnd)

        self.add(eyes.generate())

        return super().generate()


class Avatar:
    def __init__(self, data):
        self.rnd = random.Random()

        self.rnd.seed(data)

        self.data = data
        self.dwg = svgwrite.Drawing('avatar.svg', profile='tiny')

    def generate(self):
        face = Face(self.dwg, 100, 100, 50, self.rnd)

        self.dwg.add(face.generate())

        self.dwg.save()
