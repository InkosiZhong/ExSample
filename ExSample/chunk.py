import numpy as np

class Chunk:
    def __init__(self, start_id: int, length: int, random_plus: bool=False):
        self.start_id = start_id
        self.length = length
        self.vis = set()
        self.nb_samples = 0
        self.random_plus = random_plus
        self.tile_vis = np.array([False])
        self.tile_len = length

    def sample(self) -> int:
        if self.random_plus:
            return self._random_plus_sample()
        else:
            return self._random_sample()
    
    def _random_sample(self) -> int:
        frame_id = -1
        while True:
            frame_id = self.start_id + np.random.randint(0, self.length)
            if frame_id not in self.vis:
                break
        self.vis.add(frame_id)
        self.nb_samples += 1
        return frame_id
    
    def _random_plus_sample(self) -> int:
        if len(self.vis) == len(self.tile_vis):
            n_tiles = min(2 * len(self.tile_vis), self.length)
            self.tile_vis = np.array([False] * n_tiles)
            self.tile_len = self.length // len(self.tile_vis)
            for x in self.vis:
                tile = min((x - self.start_id) // self.tile_len, len(self.tile_vis) - 1)
                self.tile_vis[tile] = True
        unseen_tiles = np.where(self.tile_vis == False)[0]
        tile = np.random.choice(unseen_tiles)
        self.tile_vis[tile] = True
        frame_id = self.start_id + np.random.randint(tile * self.tile_len, (tile + 1) * self.tile_len)
        self.vis.add(frame_id)
        return frame_id

    def can_sample(self) -> bool:
        return self.nb_samples < self.length
    
if __name__ == '__main__':
    chunk = Chunk(0, 10, False)
    print('random:', [chunk.sample() for _ in range(10)])
    chunk = Chunk(0, 10, True)
    print('random+:', [chunk.sample() for _ in range(10)])