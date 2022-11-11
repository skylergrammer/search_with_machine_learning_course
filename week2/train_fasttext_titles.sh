#! /usr/bin/env bash
set -x
TRAIN_DATA="${1:-/workspace/datasets/fasttext/normalized_titles.txt}"
MODEL_FILE="title_model"
EPOCHS=25
MODEL_TYPE="skipgram"
MIN_COUNT=20
fasttext skipgram -input ${TRAIN_DATA} -output ${MODEL_FILE} -epoch ${EPOCHS} -minCount ${MIN_COUNT}