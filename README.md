# vis-a2

TCSVT 2017 Clustervision Visual Supervision of Unsupervised Clustering

Stability score

## Usage


Usage: `python stability.py <input-file> [<threshold> <search> <lowest-k> <highest-k>]`

input-file: input file name, each line in the file represents a point. You can use the clustering dataset in assignment 1 (t4.8k.dat for example), or use the Bob Ross painting dataset
              
threshold:  the threshold for stable cluster. Default: 17

search:     whether to show the statistics for different thresholds (on|off). Default: off

lowest-k:   parameters k as in k-means. Default: 2

highest-k:  parameters k as in k-means. Default: 20. The program will run all k from <lowest-k> to <highest-k>


### Run simple example

`python stability.py t4.8k.dat`

`python stability.py t4.8k.dat 17 off 2 20`

### Run with Bob Ross painting


`python stability.py paint.csv`

`python stability.py paint.csv 4 off 2 5`

### Deprecated code

`stability.py` now contains both programms `stability_a1` and `stability_tsne.py`