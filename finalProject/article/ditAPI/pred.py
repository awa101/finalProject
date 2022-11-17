# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import random
import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm, tqdm_notebook
tqdm.pandas()
from transformers import AutoTokenizer
import easydict
from pathlib import Path


# 전역변수
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'current device : {device}')

args = easydict.EasyDict({
        "seed":42,
        "seq_max_len":128,
        "batch_size": 32,
        "n_splits" : 2,
        "num_workers":0,
        "dp": 0.0,
        "model": "kobert" 
    })

method = 'soft'

def seed_everything(seed: int = 42, contain_cuda: bool = False):
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    print(f"Seed set as {seed}")


def tokenized_dataset(args, dataset, tokenizer):
    lst_premise = dataset['premise'].tolist()
    lst_hypothesis = dataset['hypothesis'].tolist()

    tokenized_sentences = tokenizer(
        lst_premise,
        lst_hypothesis,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=args.seq_max_len,
        add_special_tokens=True
    )

    return tokenized_sentences

class NLI_Dataset(Dataset):
    def __init__(self, tokenized_dataset, label):
        self.tokenized_dataset = tokenized_dataset
        self.label = label

    def __getitem__(self, idx):
        item = {key: val[idx].clone().detach() for key, val in self.tokenized_dataset.items()}
        item['label'] = torch.tensor(self.label[idx])
        return item

    def __len__(self):
        return len(self.label)

def get_tokenizer(args):
    if args.model == 'kobert':
        # tokenizer = KoBertTokenizer.from_pretrained('monologg/kobert')
        tokenizer = AutoTokenizer.from_pretrained("kykim/bert-kor-base")

    return tokenizer


"""## Prediction"""


class kobert_Classifier(nn.Module):

    def __init__(self, bert, hidden_size=768, num_classes=2, dr_rate=0.0):
        super(kobert_Classifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.pooler = nn.Linear(hidden_size, hidden_size)
        self.classifier = nn.Linear(hidden_size, num_classes)
        torch.nn.init.xavier_uniform_(self.classifier.weight)
        self.dropout = nn.Dropout(p=dr_rate)

    def forward(self, token_ids, attention_mask, segment_ids):
        # TypeError: dropout(): argument 'input' (position 1) must be Tensor, not tuple
        out = self.bert(input_ids=token_ids, attention_mask=attention_mask, token_type_ids=segment_ids)[0]
        out = out[:, 0, :]
        out = self.pooler(out)
        out = torch.nn.functional.tanh(out)  # although BERT uses tanh here, it seems Electra authors used gelu here

        if self.dr_rate:
            out = self.dropout(out)
        
        return self.classifier(out)

def load_test_dataset(args, title, content, tokenizer):
    premise = title
    hypothesis = content
    test_dataset = pd.DataFrame({'premise' : [premise], 'hypothesis' : [hypothesis], 'label' : [0]})
    test_label = test_dataset['label'].values

    tokenized_test = tokenized_dataset(args, test_dataset, tokenizer)
    return tokenized_test, test_label

def test_ensemble_main(args, title, content, ensemble='soft'):   # 'soft', 'hard'
    BASE_DIR = Path(__file__).resolve().parent
    dirTmp = os.path.join(BASE_DIR, "model.pt")
    print('BASE_DIR : ', BASE_DIR)
    print('dirTmp1111 : ', dirTmp)
    model = torch.load(dirTmp, map_location=device)
    tokenizer = get_tokenizer(args)
    # load test datset
    test_dataset, test_label = load_test_dataset(args, title, content, tokenizer)
    test_dataset = NLI_Dataset(test_dataset, test_label)
    testloader = DataLoader(test_dataset,
                    shuffle=False,
                    batch_size=args.batch_size,
                    num_workers=args.num_workers,
                    )
    
    if ensemble == 'soft':
        all_fold_logits = np.zeros((1, 2))  # rows of df, target labels
        for idx in tqdm(range(1, args.n_splits+1)):
            BASE_DIR = Path(__file__).resolve().parent
            load_path = f'models/{idx}-fold/best.pt'
            dirTmp = os.path.join(BASE_DIR, load_path)
            print('dirTmp2222 : ', dirTmp)
            model.load_state_dict(torch.load(dirTmp,map_location=torch.device('cpu')))
            model.to(device)
            model.eval()

            progress_bar = tqdm(enumerate(testloader), total=len(testloader), leave=True, position=0,)
            for i, data in progress_bar:
                with torch.no_grad():
                    logits = model(
                        data['input_ids'].to(device),
                        data['attention_mask'].to(device),
                        data['token_type_ids'].to(device)
                    )
                if i==0:
                    one_fold_logits = logits
                else:
                    one_fold_logits = torch.cat([one_fold_logits,logits],dim=0)
            
            one_fold_logits = one_fold_logits.squeeze(0).detach().cpu().numpy()

            all_fold_logits += one_fold_logits
        soft_output = list(np.argmax(all_fold_logits, axis=1))
        return soft_output, all_fold_logits




def modelPredictFunc(title, content) :

    print('----------> title test : ', title)

    seed_everything(args.seed)
    print('seed_everything')
    
    soft_output, all_fold_logits = test_ensemble_main(args, title, content, ensemble=method)
    print('test_ensemble_main')

    score = (all_fold_logits[0][0] / 2)*100
    score = round(score)

    print(score)
    return score
