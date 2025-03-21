
file_path=/home/ubuntu/cold-blossom-29/~/log
index_file=$file_path/e5_Flat.index
corpus_file=$file_path/wiki-18.jsonl
retriever=intfloat/e5-base-v2
pplx_key=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

# python search_r1/search/retrieval_server.py --index_path $index_file \
#                                             --corpus_path $corpus_file \
#                                             --topk 3 \
#                                             --retriever_model $retriever

python search_r1/search/perplexity_server.py --pplx_key $pplx_key
