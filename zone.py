import struct


class Zone:
    def __init__(self, shape):
        self.shape = shape

    def save(self):
        return struct.pack('<iiii', *self.shape)

    @staticmethod
    def load(data):
        return Zone(struct.unpack('<iiii', data))

    def collide(self, other):
        return self.shape[2] >= other.shape[0] and other.shape[2] >= self.shape[0]\
            and self.shape[3] >= other.shape[1] and other.shape[3] >= self.shape[1]

    def contains(self, point):
        return self.shape[0] <= point[0] and self.shape[1] <= point[1]\
            and point[0] <= self.shape[2] and point[1] <= self.shape[3]
