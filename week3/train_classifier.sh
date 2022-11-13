#! /usr/bin/env bash
label_queries_shuffled="${1:-/workspace/datasets/fasttext/labeled_queries_shuffled.txt}"

TRAIN_DATA="/workspace/datasets/fasttext/train.csv"
TEST_DATA="/workspace/datasets/fasttext/test.csv"

printf "Creating train and test data files from raw data\\n"
head -100000 ${label_queries_shuffled} > ${TRAIN_DATA}
tail -10000 ${label_queries_shuffled} > ${TEST_DATA}

MODEL_FILE="query_classifier"
EPOCHS=50
NGRAMS=2
LEARNING_RATE=0.25
fasttext supervised -input ${TRAIN_DATA} -output ${MODEL_FILE} -lr ${LEARNING_RATE} -epoch ${EPOCHS} -wordNgrams ${NGRAMS}

for n in 1 3 5
do
    fasttext test "${MODEL_FILE}.bin" ${TEST_DATA} ${n}
done