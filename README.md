# Audio2LyricsAlignment_MIREX2019

Repo for the MIREX 2019 - Audio-to-Lyrics Alignment Challenge. If you intend to use the code in your project, please cite our work as follows:

```
@inproceedings{demirel2019mirex,
  title={MIREX 2019 - Audio-to-Lyrics Alignment Challenge},
  year={2019},
  booktitle={International Society for Music Information Retrieval (ISMIR) in Delft, NL},
  author={Demirel, Emir}
}
```
## Requirements

Python 3.6.x or higher

Operating system : Ubuntu 16.04 or higher

## Installation

To successfully run the main alignment script in this repository, please follow the step-by-step installation instructions below :

### 0) Clone repository

  Navigate to the directory that you want to download this repository. 
  ```
   WORKSPACE=your/working/directory
   cd $WORKSPACE
   ```
   Then clone the repository
   ```
   git clone https://github.com/emirdemirel/Audio2LyricsAlignment_MIREX2019.git
   ```


### 1) Set up a new virtual environment for this project

It would be safer to create a virtual environment to run and execute the scripts in this repository. 
   - You can create your own virtual environment as follows:
   ```
   virtual_environment_name=Audio2Lyrics
   python3 -m venv $virtual_environment_name
   ```
   Then activate the virtual environment:
   ```
   source Audio2Lyrics/bin/activate
   ```
   - One can use Anaconda to create a virtual environment as well. For more info regarding creating environments using Anaconda, please refer to https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands

### 2) Install Kaldi ASR Toolkit

Kaldi (http://kaldi-asr.org/) is one of the most comprehensive open source toolkits available for research, which is the main tool used in this project. 
   - To install the toolkit, first clone the repository from here: https://github.com/kaldi-asr/kaldi
   - Once download is complete, navigate to the directory where you cloned Kaldi. This README explains how to build the toolkit. If you want to follow the installation instructions, run ```./INSTALL``` in the main directory of Kaldi.
   - From the main directory, navigate to ``` /tools```. To check the prerequisites for Kaldi, first run
   
  ```
  extras/check_dependencies.sh
  ```
and see if there are any system-level installations you need to do  

   - When the dependencies are installed, run
   ```
   make 
   ```
   (OPTIONAL) If you have multiple cores in your machine and want to speed things up, you can do so by running
   ``` 
   make -j 4`
   ```
where ``` j ``` indicates number of jobs in parallel.

  - NOTE : At this stage, you may need to install other external packages required by Kaldi, like ``` srilm``` and ``` phonetisaurus```. For that, run below lines:
       - For SRILM: ``` extras/install_srilm.sh```
       - For Phonetisaurus ```extras/install_phonetisaurus.sh ```
  - When this is complete, navigate to ``` /src ``` from the main directory of Kaldi. Then run
  ```
  ./configure --shared
  make depend -j 8
  make -j 8
  ```
  If there are no errors, the Kaldi ASR Toolkit is successfully installed.
  
### 3) Install Python requirements

  Navigate to the directory of this repository
  ```
  cd Audio2LyricsAlignment_MIREX2019
  ```
  
  While your virtual environment is active, run the following to install all the python dependencies:
  
   ```
   pip install -r requirements.txt
   ```
  
  

## How to run
First, export the path of your Kaldi Toolkit installation by running the line below with your own kaldi path. (If you don't want to do this each time you start working in repository, copy the line below and add it on the top line in ``` path.sh ``` .)
```
export KALDI_ROOT=/path/to/kaldi
```
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
   - When the program is executed and completed successfully, the alignments will be stored in ```alignments/$dataset/$rec_id``` directory (where ``` rec_id ``` is the recording ID).

   - Extracted features are stored in ```mfcc_${dataset}/ ```

   - (IMPORTANT) To generate alignments for other datasets, set the dataset variable with the corresponding name

Jamendo : ```dataset=jamendo```
Gracenote : ```dataset=gracenote```
Mauch : ```dataset=mauch```
