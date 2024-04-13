import numpy as np

class Chunk:
    def __init__(self, start_id: int, length: int):
        self.start_id = start_id
        self.length = length
        self.vis = set()
        self.nb_samples = 0

    def sample(self) -> int:
        frame_id = -1
        while True:
            frame_id = self.start_id + np.random.randint(0, self.length)
            if frame_id not in self.vis:
                break
        self.vis.add(frame_id)
        self.nb_samples += 1
        return frame_id

    def can_sample(self) -> bool:
        return self.nb_samples < self.length