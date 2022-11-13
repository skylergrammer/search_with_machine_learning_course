import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv

# Useful if you want to perform stemming.
import nltk
stemmer = nltk.stem.PorterStemmer()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/fasttext/labeled_queries.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1, type=int, help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
queries_df = pd.read_csv(queries_file_name)[['category', 'query']]
queries_df = queries_df[queries_df['category'].isin(categories)]
queries_df["query"] = queries_df["query"]\
    .str.replace("[^a-zA-Z0-9]", " ")\
    .str.replace("\s+", " ")\
    .str.strip()\
    .str.lower().map(lambda x: ' '.join([stemmer.stem(y) for y in x.split()]))

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.
categories_with_parents = set(parents_df["category"])
query_counts_per_category = queries_df.groupby(["category"]).size().reset_index(name='count')
labels_with_counts_below_threshold = query_counts_per_category[query_counts_per_category["count"] < args.min_queries].sort_values("count")
iterations = 0
while labels_with_counts_below_threshold.size > 0:
    unique_labels_0 = len(set(queries_df["category"]))
    for _, row in labels_with_counts_below_threshold.iterrows():
        label = row["category"]
        label_counts = row["count"]
        if label in categories_with_parents:
            parent_of_label = parents_df[parents_df["category"] == label]["parent"].iloc[0]
            queries_df.loc[queries_df["category"] == label, "category"] = parent_of_label
        else:
            print(f"{label} already at highest level")
    iterations += 1
    query_counts_per_category = queries_df.groupby(["category"]).size().reset_index(name='count')
    new_label_counts = query_counts_per_category[query_counts_per_category["category"] == parent_of_label]["count"].iloc[0]
    labels_with_counts_below_threshold = query_counts_per_category[query_counts_per_category["count"] < args.min_queries].sort_values("count")
    unique_labels_1 = len(set(queries_df["category"]))
    print(f"Category rollup reduced unique labels from {unique_labels_0} to {unique_labels_1} in {iterations} iterations.")
# Create labels in fastText format.
queries_df['label'] = '__label__' + queries_df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
queries_df = queries_df[queries_df['category'].isin(categories)]
queries_df['output'] = queries_df['label'] + ' ' + queries_df['query']
queries_df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)
