import random
import torch
from transformers import BertTokenizer,BertForSequenceClassification,AdamW
from transformers import get_linear_schedule_with_warmup

device=torch.device('cuda')

tokenizer=BertTokenizer.from_pretrained('bert-base-chinese')

print('这是一句话。')
print(tokenizer.tokenize('[CLS]'))
print(tokenizer.convert_tokens_to_ids(tokenizer.tokenize('[SEP]')))
print(tokenizer.convert_tokens_to_ids(tokenizer.tokenize('[PAD]')))
print(tokenizer.encode('这是一句话。',add_special_tokens=False))