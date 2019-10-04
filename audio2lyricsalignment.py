import os,sys
import subprocess, shlex
import argparse


def main(args):
    
    rec_path = args.rec_path
    lyrics_path = args.lyrics_path
    out_dir = args.out_dir
    db_name = args.db_name
    
    #Retrieve directory paths to recordings and lyrics to link for the pipeline processing --> Linking may not be necessary / TODO!!!
    #rec_dir = '/'.join(rec_path.split('/')[:-1]) 
    #lyrics_dir = '/'.join(lyrics_path.split('/')[:-1]) 
    
    #You can change the stage of the whole process if you want
    #To skip Data Preparation set stage = ...
    #To skip Feature Extraction set stage = ...
    #To skip .... (TODO)
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
    parser.add_argument("db_name", type=str, help="name of the dataset", default ="hansen")
    parser.add_argument("out_dir", type=str, help="Path where the output alignment files will be saved", default ="alignments")
    #parser.add_argument("db_path", type=str, help="Path to JamendoLyrics repository")

    args = parser.parse_args()
    main(args)
    

