import os,sys,re,glob, codecs, itertools
import argparse
import numpy as np
import pandas as pd


def read_phnsfile(ali_dir):
    phns = []
    with open(ali_dir + 'phones.txt', 'r') as p:
        for line in p.read().splitlines():
            phn = line.split(' ')[0]
            ind = line.split(' ')[1]
            phns.append({'phn':phn,'ind' :ind})
    return phns        


def load_lexicon(path):
    lex = {}
    with codecs.open(path, "rb", "utf-8") as f:
        for line in f:
            line = line.strip()
            columns = line.split(" ",1)
            word = columns[0]
            pron = columns[1]
            try:
                lex[pron].append(word)
            except:
                lex[pron] = list()
                lex[pron].append(word)
    return lex            

def merge_alignments_ctm(ali_dir):
    colnames=['name', 'segment', 'start', 'dur','phn'] 
    
    aligns = []
    for dirs, subdirs, files in os.walk(ali_dir):
        for file in files:
            if file.endswith('.ctm'):
                f = pd.read_csv(os.path.join(ali_dir,file), delimiter = ' ', header = None, names = colnames)
                aligns.append(f)

    return(pd.concat(aligns,axis=0))  
    

def retrieve_segment_start_time(segments,rec_alignments):
    segments = pd.read_csv('data/jamendo/segments', header = None, delimiter = ' ')
    for i in range(len(segments)):
        if segments.iloc[i,0] == rec_alignments.iloc[0,0]:
            return(segments.iloc[i,2])


def sort_segments(rec_alignments):

    for i in range(len(rec_alignments)):
        num_segment = int(rec_alignments.iloc[i,1])
        rec_alignments.iloc[i,1] = num_segment
    rec_alignments = rec_alignments.sort_values(['segment','start']) 
    rec_alignments = rec_alignments.drop('segment',axis=1)

    return rec_alignments    

def segments_to_dict(segments):
    segments_dict = segments.to_dict('index')
    for i in range(len(segments_dict)):
        new_key = segments_dict[i][0]
        segments_dict[new_key] = segments_dict[i]
        del segments_dict[i]
    return segments_dict    

def phon2pron(phn_file):
    pron=[]
    rec_id = phn_file.iloc[0][0]
    prons_list = []

    lines = phn_file.values.tolist()

    for line in lines:
        phon_pos=line[3]
        if phon_pos == "SIL":
            phon_pos = "SIL_S"
        phon_pos=phon_pos.split("_")
        phon=phon_pos[0]
        pos=phon_pos[1]
        if pos == "B":
            start=line[1]
            pron.append(phon)
        if pos == "S":
            start=line[1]
            end=line[2]
            pron.append(phon)
            txt = ' '.join(pron) +' '+ str(start) + ' ' + str(end)
            prons_list.append(txt)
            pron=[]
        if pos == "E":
            end=line[2]
            pron.append(phon)
            txt = ' '.join(pron) +' '+ str(start) + ' ' + str(end)
            prons_list.append(txt)
            pron=[]
        if pos == "I":
            pron.append(phon)

    return rec_id, prons_list                


def pron2word(rec_id, prons_list, lexicon, save_dir,text_path):
    
    word_ali = codecs.open(os.path.join(save_dir,rec_id.split('.tx')[0]+'.final.txt'), "wb", "utf-8")

    #read 'text' file to create a lexicon that consists of words from the data only
    text = pd.read_csv(text_path,header=None)
    text.iloc[0][0] = text.iloc[0][0].split(' ',1)

    words_list = text.iloc[0][0][1]
    #create a lexicon specific for the utterance
    data_lexicon = list(dict.fromkeys(list(itertools.chain.from_iterable([words_list.split(' ')]))))

    unk_token=0
    for line in prons_list:
        line = line.strip()
        prons = line.split(" ")[:-2]
        # get the pronunciation
        if prons[0] != 'SIL':
            prons = " ".join(prons)
            word_candidates = lexicon.get(prons)
            for w_ind in range(len(word_candidates)):
                if word_candidates[w_ind] in data_lexicon:
                    word = word_candidates[w_ind]
                elif word_candidates[0] == '<UNK>':
                    word = words_list.split(' ')[unk_token]
            word = word.replace(' ','')
            start = line.split(" ")[-2]
            end = line.split(" ")[-1]
            word_ali.write(start + '\t' + end + '\t' + word + '\n')
                    
            unk_token = unk_token + 1


def format_alignments(rec_alignments, segments_dict, phns, save_dir):
    rec_ali_text = []
    
    for i in range(len(rec_alignments)):
        seg_id = rec_alignments.iloc[i]['name']
        phn_start = rec_alignments.iloc[i]['start']
        rec_id = segments_dict[seg_id][1]
        seg_start = segments_dict[seg_id][2]
        
        phn_start = float("{0:.3f}".format(seg_start + phn_start))
        phn_end = float("{0:.3f}".format(phn_start +  rec_alignments.iloc[i]['dur']))
        for j in range(len(phns)):
            if phns[j]['ind'] == str(rec_alignments.iloc[i]['phn']):
                phoneme = phns[j]['phn']

        txt = [rec_id,phn_start,phn_end,phoneme]
        rec_ali_text.append(txt)
        
    rec_id = rec_ali_text[0][0]
    rec_ali_text = pd.DataFrame(rec_ali_text)

            
    return rec_ali_text           


def split_alignments_per_recording(merged_alignments, segments, lexicon, phns, save_dir, text_path):
    colnames=['name', 'segment', 'start', 'dur','phn']
    rec_id = ""
    rec_alignments = []
    segments_dict = segments_to_dict(segments)

    for i in range(len(merged_alignments)):
        
        rec_id_next = merged_alignments.iloc[i,0]

        rec_alignments.append(merged_alignments.iloc[i])      
        
        if i == len(merged_alignments) - 1:
            rec_alignments = pd.DataFrame(rec_alignments,columns = colnames)

            rec_alignments = sort_segments(rec_alignments)
            rec_ali_phn = format_alignments(rec_alignments, segments_dict, phns, save_dir)  
            #print('Alignments sorted and formatted! :')
            pron2word_file, prons_list = phon2pron(rec_ali_phn)
            #print('Phonemes are grouped into pronunciations of words!')
            pron2word(pron2word_file, prons_list, lexicon, save_dir, text_path)
            print('Pronunciations are converted to words! TASK FINISHED! Open files ending with ".final.txt"')
            

def main(args):
    
    ali_dir = args.ali_dir
    save_dir = args.save_dir
    segments_path = args.segments_path
    lexicon_path = args.lexicon_path
    text_path = segments_path.split('/segments')[0] + '/text'
    segments = pd.read_csv(segments_path, header = None, delimiter = ' ')
    lexicon_path = "data/local/dict/lexicon.txt"

    merged_alignments = merge_alignments_ctm(ali_dir)     
    phns = read_phnsfile(ali_dir)
    lexicon = load_lexicon(lexicon_path)

    split_alignments_per_recording(merged_alignments,segments,lexicon, phns, save_dir,text_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("ali_dir", type=str, help="name of the dataset", default ='/home/emir/QMUL/gitRepos/MIREX/exp/tri3b_fmllr_ali_jamendo/')
    parser.add_argument("save_dir", type=str, help='alignments/jamendo', default ='alignments/jamendo')
    parser.add_argument("segments_path", type=str, help="data/jamendo/segments")
    parser.add_argument("lexicon_path", type=str, help="lyrics", default="data/local/dict/lexicon.txt")

    args = parser.parse_args()
    main(args)

