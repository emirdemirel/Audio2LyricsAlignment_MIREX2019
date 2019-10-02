# Audio2LyricsAlignment_MIREX2019
Repository prepared for the MIREX 2019 - Audio-to-Lyrics Alignment Challenge

## Installation


## How to run

Run the following python script in this repository for generating the word-level alignments for the Hansen Dataset

```
rec_path=/path/to/test/audio/recording              ### PATH TO AUDIO RECORDING
lyrics_path=/path/to/test/data/lyrics               ### PATH TO LYRICS FILE (.txt)
dataset=hansen                                      ### NAME OF THE DATASET
out_dir=alignments                                  ### NAME OF THE OUTPUT DIRECTORY TO SAVE THE OUTPUT ALIGNMENTS

python audio2lyricsalignment.py $rec_path $lyrics_path $dataset $out_dir
```
To generate alignments for other datasets, set the dataset variable with the corresponding name

Jamendo : ```dataset=jamendo```
Gracenote : ```dataset=gracenote```
Mauch : ```dataset=mauch```
