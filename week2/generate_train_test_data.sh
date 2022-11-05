#! /usr/bin/env bash
labeled_products="${1:-/workspace/datasets/fasttext/labeled_products.txt}"
normalize="${2:-N}"

LABELED_PRODUCTS_SHUFFLED="/workspace/datasets/fasttext/shuffled_labeled_products.txt"
TRAIN_DATA="/workspace/datasets/fasttext/training_data.txt"
TEST_DATA="/workspace/datasets/fasttext/test_data.txt"

printf "Shuffling ${labeled_products} file\\n"
shuf ${labeled_products} --random-source=<(seq 99999) > ${LABELED_PRODUCTS_SHUFFLED}
FIRST_LINE=$(head -1 ${LABELED_PRODUCTS_SHUFFLED})
FIRST_LINE_VALID="__label__abcat0401002 Canon - PowerShot 10.0-Megapixel Digital Camera - Black"
LAST_LINE=$(tail -1 ${LABELED_PRODUCTS_SHUFFLED})
LAST_LINE_VALID="__label__abcat0401004 Canon A1100 IS Blue 12.1MP Digital Camera with Tripod, Bag and Memory Card"
printf "\\tActual first line:${FIRST_LINE}\\n\\tValid first line: ${FIRST_LINE_VALID}\\n"
printf "\\tActual last line:${LAST_LINE}\\n\\tValid last line: ${LAST_LINE_VALID}\\n"

if [ ${normalize,,} = "y" ]
then
    LABELED_PRODUCTS_SHUFFLED_NORMALIZED="/workspace/datasets/fasttext/normalized_labeled_products.txt"
    printf "Normalizing ${LABELED_PRODUCTS_SHUFFLED}\\n"
    cat ${LABELED_PRODUCTS_SHUFFLED} |sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]_]/ /g" | tr -s ' ' > ${LABELED_PRODUCTS_SHUFFLED_NORMALIZED}
    printf "Creating train and test data files from normalized data\\n"
    head -10000 ${LABELED_PRODUCTS_SHUFFLED_NORMALIZED} > ${TRAIN_DATA}
    tail -10000 ${LABELED_PRODUCTS_SHUFFLED_NORMALIZED} > ${TEST_DATA}
else
    printf "Creating train and test data files from raw data\\n"
    head -10000 ${LABELED_PRODUCTS_SHUFFLED} > ${TRAIN_DATA}
    tail -10000 ${LABELED_PRODUCTS_SHUFFLED} > ${TEST_DATA}
fi