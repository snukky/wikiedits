#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from difflib import SequenceMatcher

import string, argparse



def diff(err_toks, cor_toks, garbage):
    result = []
    matcher = SequenceMatcher(None, err_toks, cor_toks)
    ispunct = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        err = ' '.join(err_toks[i1:i2])
        cor = ' '.join(cor_toks[j1:j2])
        if ( tag=='insert' and garbage.issuperset(cor)) or  (tag=='delete' and garbage.issuperset(err)) or (tag=='replace' and garbage.issuperset(err) and garbage.issuperset(cor)):
            ispunct.append(cor)
        else:
            ispunct.append(False)
        if tag == 'replace':
            result.append("[-{}-] {{+{}+}}".format(err, cor))
        elif tag == 'insert':
            result.append("{{+{}+}}".format(cor))
        elif tag == 'delete':
            result.append("[-{}-]".format(err))
        else:
            ispunct[-1]=True
            result.append(err)
    
    if not all(ispunct):
        new_result=[]
        for i,j in zip(ispunct,result):
            if type(i)==str:
                new_result.append(i)
            else:
                new_result.append(j)
        result=new_result

    return ' '.join(result),all(ispunct)


def comment_skip(file):
    for line in file:
        if not line.startswith('###'):
            yield line

def pairwise_sent(file):
    prev = None
    for line in file:
        line=line.strip()
        if line == '' or line =='\n':
            continue
        if prev is None:
            prev = line
        else:
            yield prev,line
            prev = None
        

def print_edits(err,cor,text,file):
    print(err,cor,sep='\n',end='\n\n',file=file)

def print_wdiff(err,cor,text,file):
    print(text,file=file)
    
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Cleanup Edits File')
    parser.add_argument('input_file', help='input filename')
    parser.add_argument('discard_file', default = None, nargs='?', help='discarded filename')
    parser.add_argument('output_file', default = None, nargs='?', help='outputs filename')
    parser.add_argument('output_format', default = 'wdiff', nargs='?',choices = ('edits','wdiff'), help=' output format')
    parser.add_argument('min_char', default = 6,nargs='?', help='minimum characters')
    parser.add_argument('garbage', nargs='?',default = string.punctuation+'।॰' + string.digits+'’।०१२३४५६७८९', help='garbage characters')

    args = parser.parse_args()

    args.discard_file = args.discard_file or args.input_file.rstrip('edits')+'discard.' + args.output_format
    args.output_file = args.output_file or args.input_file.rstrip('edits')+'clean.' + args.output_format
    args.garbage = set(args.garbage)
    print_formatted = globals()['print_'+args.output_format]

    with open(args.input_file,'r') as input_file,open(args.discard_file,'w') as discard_file,open(args.output_file,'w') as output_file:
        for err,cor in pairwise_sent(comment_skip(input_file)):
            text, is_discard = diff(err.split(), cor.split(),args.garbage)
            if len(err.split())<args.min_char and len(cor.split()) < args.min_char or is_discard:
                select_file = discard_file
            else:
                select_file = output_file
            print_formatted(err,cor,text,select_file)
        
                
