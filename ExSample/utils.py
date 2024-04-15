import numpy as np
from tabulate import tabulate 

class Bbox:
    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def crop(self, frame: np.ndarray) -> np.ndarray:
        return frame[self.ymin:self.ymax, self.xmin:self.xmax, :]
    
    def __repr__(self) -> str:
        return f'Bbox({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})'

class Object:
    def __init__(self, 
                 bbox: Bbox, 
                 label: int, 
                 conf: float, 
                 track_id: int=None, 
                 frame: np.ndarray=None):
        self.bbox = bbox
        self.label = label
        self.conf = conf
        self.track_id = track_id
        if frame is not None:
            self.pixels = self.bbox.crop(frame)

    def __repr__(self) -> str:
        ret = f'Object(label={self.label} bbox={self.bbox} conf={self.conf:.2f}'
        if self.track_id is not None:
            ret += f' track_id={self.track_id})'
        else:
            ret += ')'
        return ret
    
def show_result(data, header):
    headers = [header, '']
    for k, v in data.items():
        if k == 'objects':
            print(f'{k}:' + '\n' + '\n'.join([f'[{i}] '+ str(x) for i, x in enumerate(v)]) + '\n')
        elif k == 'frame-id':
            print(f'{k}:' + '\n' + ' '.join([f'[{i}] '+ str(x) for i, x in enumerate(v)]) + '\n')
    tab_data = [(k, v) for k, v in data.items() if not isinstance(v, list)]
    print(tabulate(tab_data, headers=headers))