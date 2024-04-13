import os
from ExSample.examples.offline_query import OfflineQuery
from ExSample.utils import show_result

if __name__ == '__main__':
    root = '/home/inkosizhong/Lab/VideoQuery'
    query = OfflineQuery(
            #video_fp=os.path.join(root, 'datasets/blazeit/svideo/archie-day/2018-04-10'),
            video_fp=os.path.join(root, 'datasets/archie-day/2018-04-10'),
            csv_fp=os.path.join(root, 'datasets/blazeit/filtered/archie-day/archie-day-2018-04-10.csv'),
            query_objs=['car'],
            discrim_use_union_find=True,
            nb_chunks=16
        )
    ans, ans_frame_id, nb_samples = query.run(limit=30000)
    show_result(dict(frame_id=ans_frame_id, objects=ans, nb_find=len(ans), nb_samples=nb_samples), header='Archie')