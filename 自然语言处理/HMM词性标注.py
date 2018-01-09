import nltk
from nltk.corpus import brown

#加载语料库
brown_tags_words=[]
for sent in brown.tagged_sents():
    #添加开头
    brown_tags_words.append(('START','START'))
    #添加词性和单词，这里词性用前两个字母表示
    brown_tags_words.extend([(tag[:2],word) for word,tag in sent])
    #添加尾部
    brown_tags_words.append(('END','END'))

#计算P(wi | ti) = count(wi, ti) / count(ti)
cfd_tagwords=nltk.ConditionalFreqDist(brown_tags_words)
cpd_tagwords=nltk.ConditionalProbDist(cfd_tagwords,nltk.MLEProbDist)

#计算P(ti | t{i-1}) = count(t{i-1}, ti) / count(t{i-1})
brown_tags=[tag for (tag,word) in brown_tags_words]
cfd_tags=nltk.ConditionalFreqDist(nltk.bigrams(brown_tags))
cpd_tags=nltk.ConditionalProbDist(cfd_tags,nltk.MLEProbDist)

#输入句子
sentence=["I", "like", "apple"]

#Viterbi算法进行词性标注
distinct_tags=set(brown_tags)
viterbi=[]
backpointer=[]
##计算第一个viterbi和回溯点
first_viterbi={}
first_backpointer={}
for tag in distinct_tags:
    if tag=='START':continue
    first_viterbi[tag]=cpd_tags['START'].prob(tag)*cpd_tagwords[tag].prob(sentence[0])
    first_backpointer[tag]='START'
viterbi.append(first_viterbi)
backpointer.append(first_backpointer)
##计算中间的viterbi和回溯点
for wordindex in range(1,len(sentence)):
    this_viterbi={}
    this_backpointer={}
    prev_viterbi=viterbi[-1]
    for tag in distinct_tags:
        if tag=='START':continue
        best_previous=max(prev_viterbi.keys(),key=lambda prevtag:prev_viterbi[prevtag]*cpd_tags[prevtag].prob(tag)*cpd_tagwords[tag].prob(sentence[wordindex]))
        this_viterbi[tag]=prev_viterbi[best_previous]*cpd_tags[best_previous].prob(tag)*cpd_tagwords[tag].prob(sentence[wordindex])
        this_backpointer[tag]=best_previous
    viterbi.append(this_viterbi)
    backpointer.append(this_backpointer)
##计算所有以END结尾的viterbi和回溯点
prev_viterbi=viterbi[-1]
best_previous=max(prev_viterbi.keys(),key=lambda prevtag:prev_viterbi[prevtag]*cpd_tags[prevtag].prob('END'))
prob_tagsequence = prev_viterbi[ best_previous ] * cpd_tags[ best_previous].prob("END")

#保存最佳tag标注
backpointer.reverse()
best_tagsequence = ["END", best_previous]
current_best_tag = best_previous
for bp in backpointer:
    best_tagsequence.append(bp[current_best_tag])
    current_best_tag=bp[current_best_tag]
best_tagsequence.reverse()
best_tagsequence=best_tagsequence[1:-1]

#显示结果
for i in range(len(sentence)):
    print(sentence[i]+'|'+best_tagsequence[i])
