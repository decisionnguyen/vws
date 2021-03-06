__author__ = 'HyNguyen'

import os
import sys
import codecs
import argparse
import time

def prepare_data(sentence = "", tagset = "YN"):
    sentence_result = ""
    tag_result = ""
    sentence = sentence.replace('__','_')
    sentence = sentence.replace('\t',' ')
    words = sentence.split()
    for words in words:
        syllables = words.split('_')
        if len(syllables) == 0:
            print("exception: ", syllables)
        elif len(syllables) == 1:
            sentence_result = sentence_result + " " + syllables[0]
            if tagset == "YN":
                tag_result = tag_result + " " + "0"
            elif tagset == "BIO":
                tag_result = tag_result + " " + "O"
            elif tagset == "BEMS":
                tag_result = tag_result + " " + "S"
            else:
                print("Invalid tagset")
                sys.exit(2)
        else:
            if tagset == "YN":
                for syllable_idx in range(len(syllables)):
                    sentence_result = sentence_result + " " + syllables[syllable_idx]
                    if syllable_idx == len(syllables) -1:
                        tag_result = tag_result + " " + "0"
                    else:
                        tag_result = tag_result + " " + "1"
            elif tagset == "BIO":
                for syllable_idx in range(len(syllables)):
                    sentence_result = sentence_result + " " + syllables[syllable_idx]
                    if syllable_idx == 0:
                        tag_result = tag_result + " " + "B"
                    else:
                        tag_result = tag_result + " " + "I"
            elif tagset == "BEMS":
                for syllable_idx in range(len(syllables)):
                    sentence_result = sentence_result + " " + syllables[syllable_idx]
                    if syllable_idx == 0:
                        tag_result = tag_result + " " + "B"
                    elif syllable_idx == len(syllables) -1:
                        tag_result = tag_result + " " + "E"
                    else:
                        tag_result = tag_result + " " + "M"
    return sentence_result, tag_result

if __name__ == '__main__':

    """
    Usage: lstmpreparedata.py [-h] -fi FI -fo FO -tagset TAGSET
    """

    parser = argparse.ArgumentParser(description='Parse process ')
    parser.add_argument('-fi', required=True, type = str)
    parser.add_argument('-fo', required=True, type = str)
    parser.add_argument('-tagset', required=True, type = str)
    args = parser.parse_args()

    dir_input = args.fi
    dir_ouput = args.fo
    tagset = args.tagset

    start = time.clock()

    sys.stdout.write("Preparing data : ")

    if os.path.isfile(dir_input) == False:
        sys.stdout.write("Input file does not exist ! \n")
        sys.exit(2)

    fi = codecs.open(dir_input, encoding='utf-8',mode='r')
    lines = fi.readlines()
    fo_word = codecs.open(dir_ouput+".words", encoding='utf-8',mode='w')
    fo_label = codecs.open(dir_ouput+".labels", encoding='utf-8',mode='w')

    count = 0
    for line in lines:
        words, label = prepare_data(sentence=line,tagset=tagset)
        fo_word.write(words+"\n")
        fo_label.write(label+"\n")
        if count % 100000 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
        count+=1

    sys.stdout.write("\n")
    fo_word.close()
    fo_label.close()
    fi.close()

    end = time.clock()
    sys.stdout.write("Time for preparing data: " + str(end - start) + "second \n")

