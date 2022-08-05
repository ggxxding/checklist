import numpy as np
import pandas as pd
from senta import Senta
from senta.common.rule import InstanceName
from senta.data.util_helper import convert_texts_to_ids, structure_fields_dict
from senta.utils.util_helper import array2tensor, text_type


class SentimentChineseClassifier(Senta):
    def __init__(self):
        super(SentimentChineseClassifier, self).__init__()
        self.init_model(model_class="ernie_1.0_skep_large_ch", task="sentiment_classify", use_cuda=True)

    def predict(self, texts_, aspects=None):
        if isinstance(texts_, text_type):
            texts_ = [texts_]

        if isinstance(aspects, text_type):
            aspects = [aspects]

        return_list = convert_texts_to_ids(
            texts_, self.tokenizer, self.max_seq_len, self.truncation_type, self.padding_id)
        record_dict = structure_fields_dict(return_list, 0, need_emb=False)
        input_list = []
        for item in self.input_keys:
            kv = item.split("#")
            name = kv[0]
            key = kv[1]
            input_item = record_dict[InstanceName.RECORD_ID][key]
            input_list.append(input_item)
        inputs = [array2tensor(ndarray) for ndarray in input_list]
        result = self.inference.run(inputs)
        batch_result = self.model_class.parse_predict_result(result)
        results = []
        if self.inference_type == 'seq_lab':
            for text, probs in zip(texts_, batch_result):
                label = [self.label_map[l] for l in probs]
                results.append((text, label, probs.tolist()))
        else:
            for text, probs in zip(texts_, batch_result):
                label = self.label_map[np.argmax(probs)]
                results.append((text, label, probs.tolist()))
        return results


def main():

    classifier = SentimentChineseClassifier()
    df = pd.read_csv('test220531.txt', header=None)
    df = df.values
    texts = [x for [x] in df]
    result = classifier.predict(texts)
    print(result)
    preds=[]
    pred1=[]
    pred2=[]
    for i in result:
        if i[1]=='positive':
            preds.append(1)
        else:
            preds.append(0)
        pred1.append(i[2][0])
        pred2.append(i[2][1])
    preds=np.array(preds).reshape(-1,1)
    pred1=np.array(pred1).reshape(-1,1)
    pred2=np.array(pred2).reshape(-1,1)
    out = np.concatenate([preds,pred1,pred2],axis=1)
    out=pd.DataFrame(out)
    out=out.astype({0:int})
    out.to_csv('output_skep_220531.txt', sep=' ', header=None, index=False)

    df=pd.read_csv('test_10cats.csv')
    texts=df['review'].values
    labels = df['label'].values


if __name__ == '__main__':
    main()