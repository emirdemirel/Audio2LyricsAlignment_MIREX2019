#export KALDI_ROOT=`pwd`/../../..
#export KALDI_ROOT=/home/emir/QMUL/gitRepos/kaldi
#Modify and uncomment below to automatically run kaldi binaries
#KALDI_ROOT='/path/to/kaldi'
[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh
export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh
export LC_ALL=C

