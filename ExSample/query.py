from typing import List, Callable
from tqdm import tqdm
from ExSample.discriminator import Discriminator
from ExSample.sampler import Sampler
from ExSample.utils import Object
from ExSample.data import VideoDataset
from ExSample.chunk import Chunk

class BaseQuery:
    def __init__(self, video_fp: str, nb_chunks: int, discrim_use_union_find: bool=False):
        self.vid = VideoDataset(video_fp, self.frame_transform_fn)
        self.discrim = Discriminator(self.is_same_object, use_union_find=discrim_use_union_find)
        self.detector = self.get_detector()
        self.vid_len = len(self.vid)
        chunk_size = self.vid_len // nb_chunks
        chunks = []
        for i in range(nb_chunks):
            chunk_start = i * chunk_size
            if i == nb_chunks - 1:
                chunk_size = self.vid_len - chunk_start
            chunks.append(Chunk(chunk_start, chunk_size))
        self.sampler = Sampler(chunks=chunks, alpha0=0.1, beta0=1)
        self.set_chunk_distribution()

    def is_same_object(self, frame_id1: int, det1: Object, frame_id2: int, det2: Object) -> bool:
        '''
        Determine whether two objects belong to the same target
        '''
        raise NotImplementedError
    
    def get_detector(self):
        '''
        Get the object detection model
        '''
        return None
    
    def frame_transform_fn(self) -> Callable:
        '''
        Transform the frame format or attributes
        '''
        return lambda x: x
    
    def set_chunk_distribution(self):
        '''
        Set the initial distribution of each chunk
        '''
        pass

    def compute_frame(self, frame_id: int) -> List[Object]:
        '''
        Compute the given frame and return the detected result
        Example:
            rgb_frame = self.vid[frame_id]
            dets = self.detector(rgb_frame)
            return dets
        '''
        raise NotImplementedError

    def run(self, limit: int):
        ans = []
        ans_frame_id = []
        nb_samples = 0
        tbar = tqdm(total=limit, desc='Sampling')
        while len(ans) < limit and nb_samples < self.vid_len:
            # 1) choice of chunk and frame
            j, frame_id = self.sampler.sample()
            # 2) io,decode,detect,match
            dets = self.compute_frame(frame_id)
            # d0 are the unmatched dets
            # d1 are dets with only one match
            d0, d1, matches = self.discrim.get_matches(frame_id, dets)
            # 3) update state
            self.sampler.update_chunk_distribution(j, d0, d1)
            self.discrim.add(frame_id, dets, matches)
            ans += d0
            if len(d0) > 0:
                ans_frame_id.append(frame_id)
                tbar.update(len(d0))
            nb_samples += 1
        return ans, ans_frame_id, nb_samples