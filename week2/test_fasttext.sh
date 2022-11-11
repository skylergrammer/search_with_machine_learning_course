#! /usr/bin/env bash
set -x
N=${1:-1}
TEST_DATA="/workspace/datasets/fasttext/test_data.txt"
MODEL_FILE="/workspace/search_with_machine_learning_course/week2/product_classifier.bin"
fasttext test ${MODEL_FILE} ${TEST_DATA} ${N}