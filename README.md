# ExSample
This is the **unofficial** project page for the ExSample project.
The repository contains the code for the sampling steps in the paper (Algorithm 1).
More technical details can be find in the paper [ExSample: Efficient Searches on Video Repositories through Adaptive Sampling](https://arxiv.org/pdf/2005.09141).

## Requirements
You will need the following installed:

```bash
pip install -r requirements.txt
```
This repository uses [swag](https://github.com/stanford-futuredata/swag-python/) to access video clips.
``` bash
git clone https://github.com/stanford-futuredata/swag-python.git
cd swag-python && pip install -e .
```

## Installation
Install this repository with pip local installation.
```bash
git clone https://github.com/InkosiZhong/ExSample.git
cd ExSample && pip install -e .
```

## Experiments
<div align=center>
<img src="https://s2.loli.net/2024/04/15/fj5uzFbMik3CacB.png" width="600px">
</div>
> Currently, this repository **only** provides routines for **offline query** using `.csv` annotation files.
> If you want to query online with your object detection NN and tracking algorithms, please inherit class `BaseQuery` in `ExSample/query.py` and implement related functions.

### Data Preparation
This repository borrowed the video clips and `.csv` annotation files from [stanford-futuredata](https://github.com/stanford-futuredata).

1. The files can be downloaded from the [Google Drive](https://drive.google.com/drive/folders/1riFVI6QZGf8X6lyFphyRighAYMDTAH4Z?usp=sharing).

2. Modify `-v` and `-c` in the `ExSample/examples/archie.sh`.

### Run Routine
This routine will query `bicycle` objects in the Archie dataset with `chunks=16` and `limit=3000`.
```bash
sh ExSample/examples/archie.sh
```
The script will output the objects, frame indices and other metrics.
```bash
frame-id:
[0] 731072 [1] 439370 [2] 417376 ...

objects:
[0] Object(label=bicycle bbox=Bbox(2280, 1865, 2538, 2000) conf=1.00 track_id=266371)
[1] Object(label=bicycle bbox=Bbox(2361, 1873, 2596, 2010) conf=0.94 track_id=160599)
[2] Object(label=bicycle bbox=Bbox(2020, 1958, 2287, 2105) conf=0.99 track_id=152919)
...

ExSample Offline Query
------------------------  --
nb_find                    3000
nb_samples                 8673
```

### Custom Query
Check the following arguments to run a custom query on your dataset:
```bash
usage: offline_query.py [-h] --video-path VIDEO_PATH --csv-path CSV_PATH
                        --query-objects QUERY_OBJECTS [QUERY_OBJECTS ...]
                        [--nb-chunks NB_CHUNKS] --limit LIMIT
                        [--union-find UNION_FIND]

ExSample Offline Query

optional arguments:
  -h, --help            show this help message and exit
  --video-path VIDEO_PATH, -v VIDEO_PATH
                        path of the video
  --csv-path CSV_PATH, -c CSV_PATH
                        path of the csv file
  --query-objects QUERY_OBJECTS [QUERY_OBJECTS ...], -o QUERY_OBJECTS [QUERY_OBJECTS ...]
                        object labels for query
  --nb-chunks NB_CHUNKS, -n NB_CHUNKS
                        number of the chunks, default is 16
  --limit LIMIT, -l LIMIT
                        number of the samples to find
  --union-find UNION_FIND
                        whether to use union-find for discrimination, default
                        is True

```