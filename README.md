# Audio2LyricsAlignment_MIREX2019
Repository prepared for the MIREX 2019 - Audio-to-Lyrics Alignment Challenge

## Installation

To successfully run the main alignment script in this repository, please follow the step-by-step installation instructions below :

### 1) Install Kaldi ASR Toolkit

Kaldi (http://kaldi-asr.org/) is one of the most comprehensive open source toolkits available for research, which is the main tool used in this project. 
   - To install the toolkit, first clone the repository from here: https://github.com/kaldi-asr/kaldi

## How to run

Run the following python script in this repository for generating the word-level alignments for the Hansen Dataset

```
rec_path=/path/to/test/audio/recording              ### PATH TO AUDIO RECORDING
lyrics_path=/path/to/test/data/lyrics               ### PATH TO LYRICS FILE (.txt)
dataset=hansen                                      ### NAME OF THE DATASET
out_dir=alignments                                  ### NAME OF THE OUTPUT DIRECTORY TO SAVE THE OUTPUT ALIGNMENTS

python audio2lyricsalignment.py $rec_path $lyrics_path $dataset $out_dir
```
To learn more about the usage of the ``` audio2lyricsalignment.py ``` script, please use the guideline below:

```
usage: audio2lyricsalignment.py [-h] rec_path lyrics_path db_name out_dir

positional arguments:
  rec_path     Path to target audio recording
  lyrics_path  Path to lyrics (.txt) file for corresponding audio recording
  db_name      name of the dataset
  out_dir      Path where the output alignment files will be saved

optional arguments:
  -h, --help   show this help message and exit

```

To generate alignments for other datasets, set the dataset variable with the corresponding name

Jamendo : ```dataset=jamendo```
Gracenote : ```dataset=gracenote```
Mauch : ```dataset=mauch```
