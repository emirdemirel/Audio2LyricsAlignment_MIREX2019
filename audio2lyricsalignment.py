import os,sys
import subprocess, shlex
import argparse


def main(args):
    
    rec_path = args.rec_path
    lyrics_path = args.lyrics_path
    out_dir = args.out_dir
    db_name = args.db_name
    
    #You can change the stage of the whole process if you want
    #Stage 1 : Data Preparation
    #Stage 2 : Feature Extraction
    #Stage 3 : Forced Alignment
    #Stage 4 : Data Reformat & Post-process  
    stage = 0
    #Command the run the alignment pipeline
    cmd_run='./run.sh ' + rec_path + ' ' + lyrics_path + ' ' + out_dir + ' ' + db_name #+ ' --stage ' + str(stage)
    print(cmd_run)

    subprocess.call(shlex.split(cmd_run))
    #run_shell(cmd_run)
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("rec_path", type=str, help="Path to target audio recording", default="wav")
    parser.add_argument("lyrics_path", type=str, help="Path to lyrics (.txt) file for corresponding audio recording", default="lyrics")
    parser.add_argument("out_dir", type=str, help="Path where the output alignment files will be saved", default ="alignments")
    parser.add_argument("db_name", type=str, help="name of the dataset", default ="hansen")

    args = parser.parse_args()
    main(args)
    

