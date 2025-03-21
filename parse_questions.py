import pandas as pd
from datasets import Dataset
import os

def extract_questions(file_path):
    questions = []
    with open(file_path, 'r') as file:
        for line in file:
            question = line.strip()
            if question:
                questions.append(question)
    return questions

def make_prefix(dp, template_type):
    question = dp['question']

    # NOTE: also need to change reward_score/countdown.py
    if template_type == 'base':
        """This works for any base model"""
        prefix = f"""Answer the given question. \
You must conduct reasoning inside <think> and </think> first every time you get new information. \
After reasoning, if you find you lack some knowledge, you can call a search engine by <search> query </search> and it will return the top searched results between <information> and </information>. \
You can search as many times as your want. \
If you find no further external knowledge needed, you can directly provide the answer inside <answer> and </answer>, without detailed illustrations. For example, <answer> Beijing </answer>. Question: {question}\n"""
    else:
        raise NotImplementedError
    return prefix

def main():
    questions_list = extract_questions('questions.txt')
    
    # copied from original code. why are they making wrapper of process_fn? kinda odd...
    def make_map_fn(split):

        def process_fn(example, idx):
            example['question'] = example['question'].strip()
            if example['question'][-1] != '?':
                example['question'] += '?'
            question = make_prefix(example, template_type='base')
            solution = {
                "target": example['golden_answers'],
            }

            data = {
                "data_source": 'nq',
                "prompt": [{
                    "role": "user",
                    "content": question,
                }],
                "ability": "fact-reasoning",
                "reward_model": {
                    "style": "rule",
                    "ground_truth": solution
                },
                "extra_info": {
                    'split': split,
                    'index': idx,
                }
            }
            return data

        return process_fn
    
    out_dict = []
    for i, question in enumerate(questions_list):
        out_dict.append({
            'id': i,
            'question': question,
            'golden_answers': ['None'],
            'metadata': {
                'source': 'questions.txt'
            }
        })
        
    data = pd.DataFrame(out_dict)
    dataset = Dataset.from_pandas(data)
    
    dataset = dataset.map(function=make_map_fn('forward'), with_indices=True)
    
    dataset.to_parquet(os.path.join('/home/ubuntu/cold-blossom-29/', 'data/output/questions.parquet'))
    

if __name__ == '__main__':
    main()
