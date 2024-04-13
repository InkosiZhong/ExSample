from typing import List
from ExSample.query import BaseQuery
from ExSample.utils import Object
from ExSample.data import CSVDataset

class OfflineQuery(BaseQuery):
    def __init__(self, video_fp: str, csv_fp: str, query_objs: List[str], nb_chunks: int, discrim_use_union_find: bool):
        self.csv_fp = csv_fp
        self.query_objs = query_objs
        super().__init__(video_fp, nb_chunks, discrim_use_union_find)

    def is_same_object(self, frame_id1: int, det1: Object, frame_id2: int, det2: Object) -> bool:
        '''
        Determine whether two objects belong to the same target
        '''
        return frame_id1 != frame_id2 and det1.track_id == det2.track_id
    
    def get_detector(self):
        '''
        Get the object detection model
        '''
        return CSVDataset(self.csv_fp, len(self.vid))
    
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
        objs: List[Object] = self.detector[frame_id]
        valid_objs = []
        for obj in objs:
            if obj.label in self.query_objs:
                valid_objs.append(obj)
        return valid_objs