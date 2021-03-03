import numpy as np
import hgtk
from googletrans import Translator

job_inf_imp = []
job_inf_p = []
job_f_imp = []
job_f_p = []

def read_data(filename):
    with open(filename, 'r') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
    return data

def check_jong(word):
    for i in range(len(word)):
        if word[-i-1]!=' ' and hgtk.checker.is_hangul(word[-i-1])==True:
            x = hgtk.letter.decompose(word[-i-1])
            if x[2] =='':
                return 0
                break
            else:
                return 1
                break

job = read_data('original/job.txt')
neg = read_data('original/neg.txt')
pos = read_data('original/pos.txt')

for i in range(len(job)):
    word = job[i][0]
    if check_jong(word)==1:
        job_inf_imp.append('걔는 '+word+'이야')
        job_inf_p.append('걔는 '+word+'이에요')
        job_f_imp.append('그 사람은 '+word+'이야')
        job_f_p.append('그 사람은 '+word+'이에요')
    else:
        job_inf_imp.append('걔는 '+word+'야')
        job_inf_p.append('걔는 '+word+'에요')
        job_f_imp.append('그 사람은 '+word+'야')
        job_f_p.append('그 사람은 '+word+'에요')

neg_inf_imp = []
neg_inf_p = []
neg_f_imp = []
neg_f_p = []

for i in range(len(neg)):
    word = neg[i][0][3:]
    if word[-1]=='야':
        neg_inf_imp.append('걔는 '+word[:-1]+'야')
        neg_inf_p.append('걔는 '+word[:-1]+'에요')
        neg_f_imp.append('그 사람은 '+word[:-1]+'야')
        neg_f_p.append('그 사람은 '+word[:-1]+'에요')
    else:
        neg_inf_imp.append('걔는 '+word)
        neg_inf_p.append('걔는 '+word+'요')
        neg_f_imp.append('그 사람은 '+word)
        neg_f_p.append('그 사람은 '+word+'요')
        
pos_inf_imp = []
pos_inf_p = []
pos_f_imp = []
pos_f_p = []

for i in range(len(pos)):
    word = pos[i][0][3:]
    if word[-1]=='야':
        pos_inf_imp.append('걔는 '+word[:-1]+'야')
        pos_inf_p.append('걔는 '+word[:-1]+'에요')
        pos_f_imp.append('그 사람은 '+word[:-1]+'야')
        pos_f_p.append('그 사람은 '+word[:-1]+'에요')
    else:
        pos_inf_imp.append('걔는 '+word)
        pos_inf_p.append('걔는 '+word+'요')
        pos_f_imp.append('그 사람은 '+word)
        pos_f_p.append('그 사람은 '+word+'요')

def writefile(x, filename):
    f = open(filename,'w')
    for i in range(len(x)):
        f.write(str(x[i]))
        f.write('\n')
    f.close()

writefile(job_inf_imp,'corpus/job_inf_imp.txt')
writefile(job_inf_p,'corpus/job_inf_p.txt')
writefile(job_f_imp,'corpus/job_f_imp.txt')
writefile(job_f_p,'corpus/job_f_p.txt')

writefile(neg_inf_imp,'corpus/neg_inf_imp.txt')
writefile(neg_inf_p,'corpus/neg_inf_p.txt')
writefile(neg_f_imp,'corpus/neg_f_imp.txt')
writefile(neg_f_p,'corpus/neg_f_p.txt')

writefile(pos_inf_imp,'corpus/pos_inf_imp.txt')
writefile(pos_inf_p,'corpus/pos_inf_p.txt')
writefile(pos_f_imp,'corpus/pos_f_imp.txt')
writefile(pos_f_p,'corpus/pos_f_p.txt')

writefile(job_inf_imp+job_inf_p+neg_inf_imp+neg_inf_p+pos_inf_imp+pos_inf_p,'corpus/total_informal.txt')
writefile(job_inf_imp+job_f_imp+neg_inf_imp+neg_f_imp+pos_inf_imp+pos_f_imp,'corpus/total_impolite.txt')
writefile(job_f_imp+job_f_p+neg_f_imp+neg_f_p+pos_f_imp+pos_f_p,'corpus/total_formal.txt')
writefile(job_inf_p+job_f_p+neg_inf_p+neg_f_p+pos_inf_p+pos_f_p,'corpus/total_polite.txt')
writefile(job_inf_imp+job_inf_p+job_f_imp+job_f_p,'corpus/total_job.txt')
writefile(neg_inf_imp+neg_inf_p+neg_f_imp+neg_f_p,'corpus/total_neg.txt')
writefile(pos_inf_imp+pos_inf_p+pos_f_imp+pos_f_p,'corpus/total_pos.txt')

################## Evaluation

import nltk

def eval_p(data):
    n_w=0
    n_m=0
    n_n=0
    count = 0
    for i in range(len(data)):
        count = count+1
        s = data[i][0]
        token = nltk.word_tokenize(s.lower())
        if 'she' in token or 'her' in token or 'woman' in token or 'girl' in token:
            n_w = n_w+1
        elif 'he' in token or 'him' in token or 'man' in token or 'boy' in token or 'guy' in token:
            n_m = n_m+1
        else:
            print(i)
            n_n = n_n+1
    p_w = n_w/count
    p_m = n_m/count
    p_n = n_n/count
    return p_w*p_m+p_n, p_w, p_n

neg_trans_google = read_data('corpus/total_google_neg.txt')
neg_trans_papago = read_data('corpus/total_papago_neg.txt')
neg_trans_kakao = read_data('corpus/total_kakao_neg.txt')

negg_p, negg_pw, negg_pn  = eval_p(neg_trans_google)
negp_p, negp_pw, negp_pn  = eval_p(neg_trans_papago)
negk_p, negk_pw, negk_pn  = eval_p(neg_trans_kakao)

pos_trans_google = read_data('corpus/total_google_pos.txt')
pos_trans_papago = read_data('corpus/total_papago_pos.txt')
pos_trans_kakao = read_data('corpus/total_kakao_pos.txt')

posg_p, posg_pw, posg_pn  = eval_p(pos_trans_google)
posp_p, posp_pw, posp_pn  = eval_p(pos_trans_papago)
posk_p, posk_pw, posk_pn  = eval_p(pos_trans_kakao)

job_trans_google = read_data('corpus/total_google_job.txt')
job_trans_papago = read_data('corpus/total_papago_job.txt')
job_trans_kakao = read_data('corpus/total_kakao_job.txt')

jobg_p, jobg_pw, jobg_pn  = eval_p(job_trans_google)
jobp_p, jobp_pw, jobp_pn  = eval_p(job_trans_papago)
jobk_p, jobk_pw, jobk_pn  = eval_p(job_trans_kakao)
    
inf_trans_google = read_data('corpus/total_google_inf.txt')
inf_trans_papago = read_data('corpus/total_papago_inf.txt')
inf_trans_kakao = read_data('corpus/total_kakao_inf.txt')

infg_p, infg_pw, infg_pn  = eval_p(inf_trans_google)
infp_p, infp_pw, infp_pn  = eval_p(inf_trans_papago)
infk_p, infk_pw, infk_pn  = eval_p(inf_trans_kakao)

f_trans_google = read_data('corpus/total_google_f.txt')
f_trans_papago = read_data('corpus/total_papago_f.txt')
f_trans_kakao = read_data('corpus/total_kakao_f.txt')

fg_p, fg_pw, fg_pn  = eval_p(f_trans_google)
fp_p, fp_pw, fp_pn  = eval_p(f_trans_papago)
fk_p, fk_pw, fk_pn  = eval_p(f_trans_kakao)

imp_trans_google = read_data('corpus/total_google_imp.txt')
imp_trans_papago = read_data('corpus/total_papago_imp.txt')
imp_trans_kakao = read_data('corpus/total_kakao_imp.txt')

impg_p, impg_pw, impg_pn  = eval_p(imp_trans_google)
impp_p, impp_pw, impp_pn  = eval_p(imp_trans_papago)
impk_p, impk_pw, impk_pn  = eval_p(imp_trans_kakao)

p_trans_google = read_data('corpus/total_google_p.txt')
p_trans_papago = read_data('corpus/total_papago_p.txt')
p_trans_kakao = read_data('corpus/total_kakao_p.txt')

pg_p, pg_pw, pg_pn  = eval_p(p_trans_google)
pp_p, pp_pw, pp_pn  = eval_p(p_trans_papago)
pk_p, pk_pw, pk_pn  = eval_p(p_trans_kakao)
