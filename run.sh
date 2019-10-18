#!/bin/bash
#

# Apache 2.0

# Begin configuration section

#nj=20
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
   echo "main options (for others, see top of script file)"
   echo "  --stage <stage>                                  # Processing Stage"
   echo "  --config <config-file>                           # config containing options"
   echo "  --nj <nj>                                        # number of parallel jobs"
   echo "  --cmd (utils/run.pl|utils/queue.pl <queue opts>) # how to run jobs."
   echo "                                                   # from parent dir of <decode-dir>' (opt.)"
   echo "  --acwt <float>                                   # select acoustic scale for decoding"
   exit 1;
fi

rec_path=$1
lyrics_path=$2
out_dir=$3
testset=$4

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

mfccdir="mfcc_"$testset

echo; echo "===== Starting at  $(date +"%D_%T") ====="; echo

echo "---- DATASET : $testset ----"

if [[ $stage -le 0 ]]; then

  python3 local/prepare_data_general.py $rec_path $lyrics_path $testset data
  #if  [ "$testset" == 'hansen' ]; then
    #python3 local/prepare_data_hansen.py $rec_path $lyrics_path $testset data
  #else
    #python3 local/prepare_data_general.py $rec_path $lyrics_path $testset data
  3fi
  
fi


# Features Extraction
if [[ $stage -le 2 ]]; then

  echo
  echo "============================="
  echo "---- MFCC FEATURES EXTRACTION ----"
  echo "=====  $(date +"%D_%T") ====="

  for datadir in $testset; do
    utils/fix_data_dir.sh data/$datadir
    steps/make_mfcc.sh --cmd "$train_cmd" --nj $nj data/${datadir} exp/make_mfcc/${datadir} $mfccdir
    steps/compute_cmvn_stats.sh data/${datadir}
    utils/fix_data_dir.sh data/$datadir
  done
fi

#Forced Alignment
if [[ $stage -le 3 ]]; then

    #steps/align_si.sh --nj $nj --cmd "$train_cmd"  \
     #data/${testset} data/lang exp/tri3b exp/tri3_ali_${testset}
  if [ "$testset" == 'hansen' ]; then
    steps/align_fmllr.sh  --cmd "$train_cmd" \
     data/${testset} data/lang exp/tri3b_cleaned exp/tri3b_fmllr_ali_cleaned_${testset} || exit 1;
  else
    local/align_fmllr_mirex.sh  --cmd "$train_cmd" \
     data/${testset} data/lang exp/tri3b_cleaned exp/tri3b_fmllr_ali_cleaned_${testset} || exit 1;
  fi      
fi

#Format Alignments (Phonemes -> Pronunciation -> Words)
if [[ $stage -le 4 ]]; then

  [ -d $out_dir ] || mkdir "$out_dir"
  save_dir=$out_dir/${testset}
  [ -d $save_dir ] || mkdir "$save_dir"
  ali_dir=exp/tri3b_fmllr_ali_cleaned_${testset}/
  segments_path='data/'${testset}'/segments'
  lexicon_path='data/local/dict/lexicon.txt'

  echo "Extracting alignments & Formatting them for visualization and evaluation"
  for i in  exp/tri3b_fmllr_ali_cleaned_${testset}/ali.*.gz;
  do $KALDI_ROOT/src/bin/ali-to-phones --ctm-output exp/tri3b_cleaned/final.mdl \
  ark:"gunzip -c $i|" -> ${i%.gz}.ctm;
  done;

  echo "Split alignments per recording -> Convert phonemes to words -> Reformat timestamps"
  python3 local/alignment2words_general.py $ali_dir $save_dir $segments_path $lexicon_path
  #if [ "$testset" == 'hansen' ]; then
    #python3 local/alignment2words_hansen.py $ali_dir $save_dir $segments_path $lexicon_path
  #else
    #python3 local/alignment2words_general.py $ali_dir $save_dir $segments_path $lexicon_path
  #fi
fi
