from argparse import ArgumentParser
from collections import Counter
import xml.etree.ElementTree as ET

CATEGORIES_FN = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'


def generate_leaf_to_parent_categories(category_tree, parent_level=2, label_str="__label__"):
    leaf_to_parent_categories = dict()
    parent_counts = Counter()
    for child in tree.getroot():
        cat_path = child.find("path")
        cat_path_ids = [cat.find("id").text for cat in cat_path]
        if len(cat_path_ids) > parent_level:
            parent = label_str + cat_path_ids[parent_level]
            leaf = label_str + cat_path_ids[-1]
            if parent != leaf:
                leaf_to_parent_categories[leaf] = parent
                parent_counts[parent] += 1
    return leaf_to_parent_categories, parent_counts


def get_class_counts(data):
    class_counts = Counter()
    for (label, *_) in data:
        class_counts[label] += 1
    return class_counts


def filter_data_by_class_count(
        data,
        class_counts,
        leaf_to_parent_categories,
        min_class_count=500,
    ):
    new_data = []
    for (label, *text) in data:
        class_count = class_counts[label]
        if class_count > min_class_count:
            new_data.append((label, text))
        elif label in leaf_to_parent_categories and class_counts[leaf_to_parent_categories[label]] > min_class_count:
            parent_category_label = leaf_to_parent_categories[label]
            new_data.append((parent_category_label, text))
    return new_data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("labeled_products_fn")
    parser.add_argument("labeled_products_clean_fn")
    parser.add_argument("--min_class_count", "-m", type=int, default=500)
    args = parser.parse_args()

    tree = ET.parse(CATEGORIES_FN)
    leaf_to_parent_categories, parent_counts = generate_leaf_to_parent_categories(tree)
    with open(args.labeled_products_fn) as f:
        # each line formatted as space delimited list of strings with first being the label
        # E.g. "__label__abcat0515028 HP - Mini Laptop Sleeve"
        data = [x.split() for x in f]

    class_counts = get_class_counts(data)
    class_counts.update(parent_counts)
    data_pruned = filter_data_by_class_count(
        data,
        class_counts,
        leaf_to_parent_categories,
        min_class_count=args.min_class_count
    )

    with open(args.labeled_products_clean_fn, 'w') as f:
        for (label, text) in data_pruned:
            line = " ".join([label, " ".join(text)+"\n"])
            f.write(line)
