# vis-a2

TCSVT 2017 Clustervision Visual Supervision of Unsupervised Clustering

Stability score

## Usage

Usage: `python stability.py <input-file> [<threshold> <search> <lowest-k> <highest-k>]`

input-file: input file name, each line in the file represents a point. The X-coordinate and Y-coordinate is separated by a space. Use t4.8k.dat as an example.
              
threshold:  the threshold for stable cluster. Default: 17

search:     whether to show the statistics for different thresholds (on|off). Default: off

lowest-k:   parameters k as in k-means. Default: 2

highest-k:  parameters k as in k-means. Default: 20. The program will run all k from <lowest-k> to <highest-k>

### Run simple example

`python stability.py t4.8k.dat`

`python stability.py t4.8k.dat 17 off 2 20`

### Run with Bob Ross painting

Usage: `python stability_tsne.py <input-file> [<threshold> <search> <lowest-k> <highest-k>]`

`python stability_tsne.py paint.csv`

`python stability_tsne.py paint.csv 4 off 2 5`
