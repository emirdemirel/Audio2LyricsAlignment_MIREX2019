# -*- coding: utf-8 -*-

import os, sys, hashlib, io, re
import string
import sys
import pandas as pd
import argparse
import subprocess
from os.path import join, exists
from pydub import AudioSegment
from pydub.silence import detect_nonsilent



class Recording:
    def __init__(self, rec_path, lyrics_path, workspace, name):
        self.segments = []
        self.spk2gender = []
        self.text = []
        self.utt2spk = []
        self.wavscp = []
        self.rec_path = rec_path
        self.lyrics_path = lyrics_path
        self.workspace = workspace
        self.out_dir = join('data',name)
        self.regex = re.compile("[^a-zA-Z']")
        self.dataset_name = name

    def add_utterance(self, rec):
        
        audio_format = rec.split('.')[-1]
        rec_id = rec.split('.'+audio_format)[0]  
        lyrics_path = self.lyrics_path 
        
        if self.dataset_name == 'jamendo':
            lyrics_path = lyrics_path.replace('raw','words') ### ONLY IF WORDS FILE PROVIDED, THIS IS USEFUL FOR TEXT PROCESSING
            spk = rec_id.split('_-_')[0]
        else:    
            spk = 'singer_0' #SPEAKER ID IS NOT IMPORTANT FOR THIS TASK BUT IT IS REQUIRED FOR DATA PROCESSING IN Kaldi FRAMEWORK

        gender = 'F'           
        wavpath = join('wav',rec)
        
        lyrics_file = io.open(lyrics_path, mode="r", encoding="utf-8")
        text = ''
        for line in lyrics_file.readlines():
            words_per_segment = str(line).replace("b'","").replace("\\xe2\\x80\\x99","'").replace('b"',"")[:-1].replace('(',"").replace(')',"").replace('–',"").replace('…',"").replace('...',"").replace('  ',' ').replace("”","").replace('“',"").replace('.',"").replace('***',"").replace("\xa0","").replace('-',"").replace('_',"")
            if words_per_segment.strip():
                words_split = list(filter(None, words_per_segment.split(' ')))
                words_split_no_number = []
                for i in range(len(words_split)):
                    if not words_split[i].isdigit():
                        words_split_no_number.append(words_split[i])
                        text = text + ' ' + words_split[i]
        text = text[1:].upper()
        
        start= 0.00
        end = self._get_duration()
        
        utt_id = rec_id  # WE DON'T SEGMENT SONGS FOR THE OTHER DATASETS

        self._add_segment(utt_id, rec_id, start, end)
        self._add_spk2gender(spk, gender)
        self._add_text(utt_id, text)
        self._add_utt2spk(utt_id, spk)
        self._add_wavscp(rec_id, self.rec_path)

    def _get_duration(self):
        #this function is necessary for creating the segments file
        audio = AudioSegment.from_file(self.rec_path)
        return len(audio)/1000 #from ms to sec
        
    def _retrieve_vocal_segment(self, silence_threshold):

	# This function is written for retrieving the start and end times of the vocal segment in the full songs
        # using an open-source source separation algorithm. 
        # It will be used in the later versions of the alignment toolkit! 

        print('Separating Vocals from Original Audio to Retrieve Vocal Segment')
        
        input_file = self.rec_path
        output_ss = 'separated_vocals'
        sample_rate = 16000

        separate_vocals.run_separation(input_file, output_ss, sample_rate)

        filename_separated = self.rec_path.split('/')[-1].replace('.wav','_vocals.wav')
        separeted_vocals_path = join(output_ss,filename_separated)
   
        ### Segment vocal parts
        recording = AudioSegment.from_file(separeted_vocals_path,format='wav', frame_rate = sample_rate)

        nonsil_segments = detect_nonsilent(recording,silence_thresh=silence_threshold)
        print(nonsil_segments)
        start_nonsil_segment = (nonsil_segments[0] - 1000)/1000 # begin segment one second ahead then convert to sec
        end_nonsil_segment = (nonsil_segments[-1] + 1000)/1000 # end segment one second later then convert to sec

        # Remove separated vocals audio file to save space
        os.remove(separeted_vocals_path)
        
        return start_nonsil_segment,end_nonsil_segment

    def _add_segment(self, utt_id, rec_id, start, end):
        self.segments.append("{} {} {:.3f} {:.3f}".format(utt_id, rec_id, start, end))

    def _add_spk2gender(self, spk, gender):
        self.spk2gender.append("{} {}".format(spk, gender.lower()))

    def _add_text(self, utt_id, text):
        self.text.append("{} {}".format(utt_id, text))

    def _add_utt2spk(self, utt_id, spk):
        self.utt2spk.append("{} {}".format(utt_id, spk))

    def _add_wavscp(self, rec_id, wavpath):
        self.wavscp.append("{} sox {} -G -t wav -r 16000 -c 1 - remix 1 |".format(rec_id, wavpath))

    def _write_file(self, outfile, list_data):
        list_data = list(set(list_data))
        with open(outfile, "w") as f:
            for line in list_data:
                f.write("{}\n".format(line))

    def save(self):
        if not exists(self.out_dir):
            os.makedirs(self.out_dir)
        self._write_file(join(self.out_dir, "spk2gender"), sorted(self.spk2gender))
        self._write_file(join(self.out_dir, "text"), sorted(self.text))
        self._write_file(join(self.out_dir, "wav.scp"), sorted(self.wavscp))
        self._write_file(join(self.out_dir, "utt2spk"), sorted(self.utt2spk))
        self._write_file(join(self.out_dir, "segments"), sorted(self.segments))
        
        
def main(args):
    
    rec_path = args.rec_path
    lyrics_path = args.lyrics_path
    workspace = args.workspace
    name = args.name
    filename = rec_path.split('/')[-1]

    recording = Recording(rec_path,lyrics_path,workspace,name)
    recording.add_utterance(filename)
    recording.save()
        
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("rec_path", type=str, help="Path to audio recording")
    parser.add_argument("lyrics_path", type=str, help="Path to lyrics file")
    parser.add_argument("name", type=str, help="name of the dataset", default ="hansen")
    parser.add_argument("workspace", type=str, help="Path where the output files will be saved", default ="data")

    args = parser.parse_args()
    main(args)
