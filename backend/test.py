import string
from checklist.perturb import Perturb
from checklist.editor import Editor
import numpy as np

def random_string(n):
    return ''.join(np.random.choice([x for x in string.ascii_letters + string.digits],n))
def random_url(n=6):
    return 'https://t.co/%s' % random_string(n)
def random_handle(n=6):
    return '@%s' % random_string(n)

def add_irrelevant(sentence):
    urls_and_handles = [random_url(n=6) for _ in range(5)] + [random_handle() for _ in range(5)]
    irrelevant_before = ['@airline '] + urls_and_handles
    irrelevant_after = urls_and_handles
    rets = ['%s %s' % (x,sentence) for x in irrelevant_before]
    rets += ['%s %s' % (sentence,x) for x in irrelevant_after]
    return rets

sentences=['你好','yes!']

t=Perturb.perturb(sentences, add_irrelevant, nsamples=500)
print(t.data)