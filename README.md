# vis-a2

Author: Tien-Hsuan Wu, Zhiyong Wu

TCSVT 2017 Clustervision Visual Supervision of Unsupervised Clustering (Ng, et al., 2017)

In this project, we evaluate k-means clutering results by varying the parameter k, and compute the stability scores. For
two data point, the stability score is higher if they belong to the same cluster in most of the clustering results. The
result is visualized in 2D space. (See the conclusion section in the aforementioned paper.)

## Requirements
* python: 3.5
* scikit-learn: 0.19.0
* pyqt: 5
* rtree: 0.8.2
* matplotlib: 2.1.0
* numpy: 1.11.1
* pandas: 0.20.3

## Useful files included

**stability.py**: core to compute the stability metrics and produce output figures 

t4.8k.dat, paint.csv: input files for stability.py

**viewer.py**: gui to display the figures produced by viewer

new_paint.png, new_t4.8k.png, original_paint.png, original_t4.8k.png: files required to run viewer.py

**prototype.pdf**, **viewer_example.png**: snapshots of stability.py, viewer.py

## Usage

1. Find Stability

Usage: `python stability.py <input-file> [<threshold> <search> <lowest-k> <highest-k>]`

input-file: input file name, each line in the file represents a point. You can use the clustering dataset in assignment 1 (t4.8k.dat for example), or use the Bob Ross painting dataset
              
threshold:  the threshold for stable cluster. Default: 17

search:     whether to show the statistics for different thresholds (on|off). Default: off

lowest-k:   parameters k as in k-means. Default: 2

highest-k:  parameters k as in k-means. Default: 20. The program will run all k from <lowest-k> to <highest-k>

2. Run Viewer

Command: `python viewer.py`

Files required (all files can be produced by `stability.py`, renaming may be required): 

original_t4.8k.png: The original visualized data of t4.8k.png

new_t4.8k.png: The result after finding stability index of t4.8k.png

original_paint.png: The original visualized data of the painting dataset using t-SNE projection

new_paint.png: The result after finding stability index of painting dataset


### Run simple example

`python stability.py t4.8k.dat`

`python stability.py t4.8k.dat 17 off 2 20`

### Run with Bob Ross painting


`python stability.py paint.csv`

`python stability.py paint.csv 4 off 2 5`

### Deprecated code

`stability.py` now contains both programms `stability_a1` and `stability_tsne.py`