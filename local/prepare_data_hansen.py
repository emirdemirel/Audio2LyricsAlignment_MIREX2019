# -*- coding: utf-8 -*-

import re, os
import pandas as pd
import argparse
from os.path import join, exists



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
        self.spk_id = 0
        self.dataset_name=name

    def add_utterance(self, rec):
        
        audio_format = rec.split('.')[-1]
        rec_id = rec.split('.'+audio_format)[0]  
        lyrics_path = self.lyrics_path 
        print(type(lyrics_path))
        
        sentence_file = join(lyrics_path.split('.txt')[0] +'_sents.txt')
        
        gender = 'F'           
        spk = 'singer_'+str(self.spk_id)
        #wavpath = join('wav_hansen',rec)
        
        sentence_file = pd.read_csv(sentence_file, header=None, sep='\t')
        #print(sentence_file)
        for i in range(len(sentence_file)):
            text = sentence_file.iloc[i,2]
            #text = sentence_file.iloc[i,2].replace("b'","").replace("\\xe2\\x80\\x99","'").replace('b"',"")[:-1].replace('(',"").replace(')',"").replace('–',"").replace('…',"").replace('...',"").replace('  ',' ').replace("”","").replace('“',"").replace('.',"").replace('***',"").replace("\xa0","").replace('-',"").replace('_',"")
            start = sentence_file.iloc[i,0]
            end = sentence_file.iloc[i,1]
            utt_id = rec_id.split('_')[0]+'_segment_0'+str(i)
            
            self._add_segment(utt_id, rec_id, start, end)
            self._add_spk2gender(spk, gender)
            self._add_text(utt_id, text)
            self._add_utt2spk(utt_id, spk)
            self._add_wavscp(rec_id, self.rec_path)     
            print(text)
        self.spk_id = self.spk_id + 1
            
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
    #acapella = args.acappella
    
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
    #parser.add_argument("acappella", type=str, help="Set true to align acappella recordings", default=True)

    args = parser.parse_args()
    main(args)
