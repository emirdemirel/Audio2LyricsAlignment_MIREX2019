#!/bin/bash

# Begin configuration section

nj=1
stage=0

source "Audio2Lyrics/bin/activate"

if [ $# != 4 ]; then
   echo "Usage: $0 [options] <rec_path> <lyrics_path> <out_dir> <db_name>"
   echo ""
   echo ""
   echo ""
   echo ""
   echo ""
   echo ""
   echo ""
   echo ""
   echo "main options"
   echo "  <rec_path>                                                 # Path to recording "
   echo "  <lyrics_path>                                              # Path to Lyrics file"
   echo "  <out_dir>                                                  # output directory to put final alignments files"
   echo "  <db_name>                                                   # name of the database"
   echo ""   
   exit 1;
fi

rec_path=$1
lyrics_path=$2
out_dir=$3
testset=$4

rec_filename=${rec_path##*/}
rec_id=${rec_filename%*".wav"}
#echo $rec_id
datadir=data/$testset/$rec_id


. ./path.sh
. ./cmd.sh

echo "Using steps and utils from WSJ recipe"
[[ ! -L "steps" ]] && ln -s $KALDI_ROOT/egs/wsj/s5/steps
[[ ! -L "utils" ]] && ln -s $KALDI_ROOT/egs/wsj/s5/utils

# End configuration section
. ./utils/parse_options.sh
# Exit on error
set -e 
# CHECK NECESSARY TOOLS - This script also needs the phonetisaurus g2p, srilm, sox
./local/check_tools.sh || exit 1


echo; echo "===== Starting at  $(date +"%D_%T") ====="; echo

echo "============================="
echo "---- DATASET : $testset ----"
echo "============================="

if [[ $stage -le 1 ]]; then

  echo
  echo "============================="
  echo "---- DATA PREPARATION ----"
  echo "============================="
  echo
  python3 local/prepare_data_general.py $rec_path $lyrics_path $testset data/$testset/$rec_id

fi


mfccdir="mfcc_${testset}"/$rec_id
# Features Extraction
if [[ $stage -le 2 ]]; then

  echo
  echo "============================="
  echo "---- MFCC FEATURES EXTRACTION ----"
  echo "============================="
  echo



  utils/fix_data_dir.sh $datadir
  steps/make_mfcc.sh --cmd "$train_cmd" --nj $nj $datadir exp/make_mfcc/${rec_id} $mfccdir
  steps/compute_cmvn_stats.sh ${datadir}
  utils/fix_data_dir.sh $datadir

fi

ali_dir=exp/tri3b_fmllr_ali_cleaned_${testset}/${rec_id}/

#Forced Alignment
if [[ $stage -le 3 ]]; then

  echo
  echo "============================="
  echo "---- ALIGNMENT ----"
  echo "============================="
  echo

  local/align_fmllr_mirex.sh  --cmd "$train_cmd" \
    $datadir data/lang exp/tri3b_cleaned $ali_dir || exit 1;

fi

#Format Alignments (Phonemes -> Pronunciation -> Words)
if [[ $stage -le 4 ]]; then

  echo
  echo "============================="
  echo "---- POST-PROCESS & REFORMAT DATA ----"
  echo "============================="
  echo

  [ -d $out_dir ] || mkdir "$out_dir"
  dataset_dir=$out_dir/$testset 
  [ -d $dataset_dir ] || mkdir "$dataset_dir"
  #save_dir=$dataset_dir/$rec_id
  save_dir=$dataset_dir/
  [ -d $save_dir ] || mkdir "$save_dir"
  segments_path=$datadir'/segments'

  lexicon_path='data/local/dict/lexicon.txt'

  echo "Extracting alignments & Formatting them for visualization and evaluation"
  for i in  ${ali_dir}/ali.*.gz;
  do $KALDI_ROOT/src/bin/ali-to-phones --ctm-output exp/tri3b_cleaned/final.mdl \
  ark:"gunzip -c $i|" -> ${i%.gz}.ctm;
  done;

  echo "Split alignments per recording -> Convert phonemes to words -> Reformat timestamps"
  python3 local/alignment2words_general.py $ali_dir $save_dir $segments_path $lexicon_path

fi
