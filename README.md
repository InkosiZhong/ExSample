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
> Currently, this repository **only** provides routines for **offline query** using `.csv` annotation files.
> If you want to query online with your object detection NN and tracking algorithms, please inherit class `BaseQuery` in `ExSample/query.py` and implement related functions.

### Data Preparation
This repository borrowed the video clips and `.csv` annotation files from [stanford-futuredata](https://github.com/stanford-futuredata).

1. The files can be downloaded from the [Google Drive](https://drive.google.com/drive/folders/1riFVI6QZGf8X6lyFphyRighAYMDTAH4Z?usp=sharing).

2. Modify `video_fp` and `csv_fp` in the `ExSample/examples/archie.py`.

### Run Query
```bash
time python ExSample/examples/archie.py
```
The script will output the objects, frame indices and other metrics.
```bash
frame_id:
[0] 408432

objects:
[0] Object(label=car bbox=Bbox(2306, 1124, 2709, 1374) conf=0.99 track_id=150174)
[1] Object(label=car bbox=Bbox(3648, 1574, 3836, 1816) conf=0.97 track_id=150211)
[2] Object(label=car bbox=Bbox(3203, 811, 3530, 1015) conf=0.95 track_id=150205)

Archie
----------  --
nb_find      3
nb_samples   2
```