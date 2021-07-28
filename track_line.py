class TrackLine:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return '(({}, {}), ({}, {}))'.format(self.x1, self.y1, self.x2, self.y2)

    def point_one(self):
        return self.x1, self.y1

    def point_two(self):
        return self.x2, self.y2

    def get_length(self):
        return self.x2 - self.x1