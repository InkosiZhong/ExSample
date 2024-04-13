from typing import List
import swag
import numpy as np
import json
import cv2
import pandas as pd
from collections import defaultdict
from ExSample.utils import Bbox, Object

class VideoDataset:
    def __init__(self, video_fp: str, transform_fn=lambda x: x):
        self.video_fp = video_fp
        self.transform_fn = transform_fn
        self.cap = swag.VideoCapture(self.video_fp)
        self.video_metadata = json.load(open(self.video_fp + '.json', 'r'))
        self.cum_frames = np.array(self.video_metadata['cum_frames'])
        self.cum_frames = np.insert(self.cum_frames, 0, 0)
        self.length = self.cum_frames[-1]
        self.current_idx = 0

    def transform(self, frame: np.ndarray) -> np.ndarray:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.transform_fn(frame)
        return frame

    def seek(self, idx: int):
        if self.current_idx != idx:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx - 1)
            self.current_idx = idx

    def read(self) -> np.ndarray:
        _, frame = self.cap.read()
        frame = self.transform(frame)
        self.current_idx += 1
        return frame

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, idx: int) -> np.ndarray:
        self.seek(idx)
        frame = self.read().cuda()
        return frame

class CSVDataset:
    def __init__(self, labels_fp: str, length: int):
        df = pd.read_csv(labels_fp)
        frame_to_rows = defaultdict(list)
        for row in df.itertuples():
            bbox = Bbox(int(row.xmin), int(row.ymin), int(row.xmax), int(row.ymax))
            obj = Object(
                    bbox=bbox, 
                    label=row.object_name, 
                    conf=row.confidence, 
                    track_id=row.ind, 
                    frame=None
                )
            frame_to_rows[row.frame].append(obj)
        labels = []
        for frame_idx in range(length):
            labels.append(frame_to_rows[frame_idx])
        self.labels = labels

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx) -> List[Object]:
        return self.labels[idx]