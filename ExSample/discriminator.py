import random
from typing import Any, List, Tuple, Callable
from ExSample.utils import Object
    
class UnionFind:
    def __init__(self):
        self.data = []
        self.parent = []
        self.size = []

    def add(self, x: Any) -> int:
        self.data.append(x)
        i = len(self.parent)
        self.parent.append(i)
        self.size.append(1)
        return i

    def union(self, i: int, j: int):
        p1 = self.find(i)
        p2 = self.find(j)
        if p1 != p2:
            self.parent[p1] = p2
            self.size[p2] += self.size[p1]

    def find(self, i: int) -> int:
        while i != self.parent[i]:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i
    
    def count(self, i: int) -> int:
        p = self.find(i)
        return self.size[p]
    
    def __iter__(self):
        self.i_iter = 0
        return self
    
    def __next__(self):
        if self.i_iter < len(self.data):
            result = self.data[self.i_iter]
            self.i_iter += 1
            return result
        else:
            raise StopIteration

class Discriminator:
    def __init__(self, is_same_object: Callable, use_union_find=False):
        self.records = UnionFind() if use_union_find else []
        self.use_union_find = use_union_find
        self.is_same_object = is_same_object

    def get_matches(self, frame_id: int, dets: List[Object]) -> Tuple[List[Object], List[Object], List[int]]:
        d0 = [] # d0 are the unmatched dets
        d1 = [] # d1 are dets with only one match
        matches = [None] * len(dets)
        for i, det1 in enumerate(dets):
            cnt = 0
            if self.use_union_find:
                self.records.add((frame_id, det1))
            for j, (record_id, det2) in enumerate(self.records):
                if self.is_same_object(frame_id, det1, record_id, det2):
                    matches[i] = j
                    if self.use_union_find:
                        cnt = self.records.count(j)
                        break
                    else:
                        cnt += 1
            if cnt == 0:
                d0.append(det1)
            elif cnt == 1:
                d1.append(det1)
        return d0, d1, matches

    def add(self, frame_id: int, dets: List[Object], matches: List[int]):
        if self.use_union_find:
            for det, j in zip(dets, matches):
                i = self.records.add((frame_id, det))
                if j != None:
                    self.records.union(i, j)
        else:
            self.records += [(frame_id, det) for det in dets]