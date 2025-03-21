# Running forecasts 

## Packages

Please install the required packages and make the required environments per the README.md file.

In addition, install the `openai` package in the retriever environment and ensure `tenacity` is installed in the retriever environment.

Be sure to have a Perplexity key and WandB key ready.

## Data

Data needs to be in the format given in `sample_data.json`. 

The `train` and `test` are keys of one map, each of which is a list of maps. Each list entry is a map representing a sample.

```
{
    'train': [
        {
            'id': 'train_0',
            'question': 'Will the South Korean president step down in 2025?',
            'golden_answers': ['Yes'],
            'metadata': {'0': 0}
        },
        ...
    ],
    'test': [
        {
            'id': 'test_0',
            'question': 'Will the war in Ukraine end in 2025?',
            'golden_answers': ['Yes'],
            'metadata': {'0': 0}
        },
        ...
    ]
}
```

Then run `python scripts/data_process/nq_search_forecast.py` to process the data. This will produce `train_forecast.parquet` and `test_forecast.parquet` in the `data/nq_search` directory. The `metadata` does not matter in this case. (the data directory is git ignored. You will need to run it yourself.)


## Running the perplexity server

In one shell (background or tmux), run the perplexity server.

This launches the perplexity server, which takes your query and runs async inference to perplexity. Changing this to Exa should be straightforward + query optimizations and rewritings.

```bash
bash retrieval_launch.sh
```

This should be quick and should show:

```
INFO:     Started server process [356924]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Running the PPO training

In another shell, run the PPO training.

```bash
bash train_ppo.sh
```

Be sure the batch sizes are set correctly. This is a fork of the original codebase which does not handle batch size edge cases well. Your batch size must be less than the number of data, or it will crash the whole process. 

Also be sure to set your train and eval data correctly.

```
data.train_files=$DATA_DIR/train_forecast.parquet \
data.val_files=$DATA_DIR/test_forecast.parquet \
```

# Settings, Base LLMs, data location

In `train_ppo.sh`, you can set the following:
```
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export DATA_DIR='data/nq_search'

WAND_PROJECT='Search-R1'

export BASE_MODEL='meta-llama/Llama-3.2-3B'
export EXPERIMENT_NAME=nq-search-r1-ppo-llama3.2-3b-em
```

This says we need 8 GPUs to train, the data lives in `data/nq_search` (`nq_search_forecast.py` puts the data there as well), and we are using the Llama-3.2-3B model (huggingface notation).

Since models are gated, you will need a valid key.

Logging is done to wandb. You will need a wandb key as well.