# Running forecasts 

## Data

Data needs to be in the format given in `sample_data.json`.

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

