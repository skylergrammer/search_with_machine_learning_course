#! /usr/bin/env bash
set -x
TRAIN_DATA="${1:-/workspace/datasets/fasttext/training_data.txt}"
MODEL_FILE="product_classifier"
EPOCHS=25
NGRAMS=1
LEARNING_RATE=1.0
MODEL_TYPE="skipgram"
fasttext supervised -input ${TRAIN_DATA} -output ${MODEL_FILE} -lr ${LEARNING_RATE} -epoch ${EPOCHS} -wordNgrams ${NGRAMS}