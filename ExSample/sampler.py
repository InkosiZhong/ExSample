import numpy as np
from typing import List, Tuple
from ExSample.utils import Object
from ExSample.chunk import Chunk

class Sampler:
    def __init__(self, chunks: List[Chunk], alpha0: float=0.1, beta0: float=1):
        self.chunks = chunks
        self.M = len(chunks)
        self.N1 = [0] * self.M
        self.n = [0] * self.M
        self.base_param = [(alpha0, beta0) for _ in range(self.M)]
    
    def sample(self) -> Tuple[int, int]:
        vals = np.zeros(self.M)
        for j in range(self.M):
            alpha0, beta0 = self.base_param[j]
            val = np.random.gamma(self.N1[j] + alpha0, 1 / (self.n[j] + beta0))
            vals[j] = val
        order = np.argsort(vals)[::-1]
        for j_star in order:
            if self.chunks[j_star].can_sample():
                frame_id = self.chunks[j_star].sample()
                return j_star, frame_id
        raise RuntimeError('No more frames can be sampled.')

    def update_chunk_distribution(self, j: int, d0: List[Object], d1: List[Object]):
        self.N1[j] += len(d0) - len(d1)
        self.n[j] += 1

    def set_chunk_distribution(self, j: int, alpha: float, beta: float):
        self.base_param[j] = (alpha, beta)