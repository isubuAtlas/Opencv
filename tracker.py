import config
import math

class Tracker:
    def __init__(self):
        self.last_position = None
        self.missing_frames = 0

    def update(self, x, y):

        if self.last_position is None:
            self.last_position = (x, y)
            return x, y

        last_x, last_y = self.last_position

        distance = math.sqrt((x - last_x)**2 + (y - last_y)**2)

        if distance < config.MAX_DISTANCE:
            self.last_position = (x, y)
            self.missing_frames = 0
        else:
            self.missing_frames += 1

            if self.missing_frames > config.MAX_MISSING:
                self.last_position = None
                return None

        return self.last_position