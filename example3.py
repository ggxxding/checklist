import checklist
from checklist.perturb import Perturb
import spacy

#英文spacy例子
dataset=['John is a man','Mary is a woman']
nlp=spacy.load('en_core_web_sm')
pdataset=list(nlp.pipe(dataset))

ret=Perturb.perturb(pdataset, Perturb.change_names,n=2)
print("dataset:")
print(pdataset)
print("output:")
print(ret.data)