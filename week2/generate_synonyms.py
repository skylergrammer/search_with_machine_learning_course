from argparse import ArgumentParser
import fasttext


class SynonymGenerator:
    def __init__(self, model_fn):
        self.model = fasttext.load_model(model_fn)

    def _synonymize(self, keyword, threshold=0.75):
        synonyms = self.model.get_nearest_neighbors(keyword, k=20)
        for (score, synonym) in synonyms:
            if score > threshold:
                yield synonym

    def generate_synonyms_list(self, keywords, threshold=0.75):
        synonyms = dict()
        for keyword in keywords:
            valid_synonyms = list(self._synonymize(keyword))
            if valid_synonyms:
                synonyms[keyword] = valid_synonyms
        return synonyms

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("keywords_fn")
    parser.add_argument("model_fn")
    parser.add_argument("--synonyms_fn", "-o", default="/workspace/datasets/fasttext/synonyms.csv")
    parser.add_argument("--threshold", "-t", type=float, default=0.75)
    args = parser.parse_args()

    with open(args.keywords_fn) as f:
        keywords = f.read().splitlines()

    synonym_generator = SynonymGenerator(args.model_fn)
    synonyms = synonym_generator.generate_synonyms_list(keywords, threshold=args.threshold)

    with open(args.synonyms_fn, "w") as f:
        for keyword, synonyms in sorted(synonyms.items()):
            line = ",".join([keyword, ",".join(synonyms)])
            f.write(line+'\n')
