# Project Assessment
## For classifying product names to categories:
* What precision (P@1) were you able to achieve?
    ```
    N	8473
    P@1	0.963
    R@1	0.963
    ```
* What fastText parameters did you use?
    ```
    EPOCHS=25
    NGRAMS=1
    LEARNING_RATE=1.0
    ```
* How did you transform the product names?
    * Remove all non-alphanumeric characters other than underscore.
    * Convert all letters to lowercase.
    * Trim excess space characters so that tokens are separated by a single space.

* How did you prune infrequent category labels, and how did that affect your precision?
    * Caclulated the total count of all leaf-level labels.
    * Calculated the total count of all depth=2-level labels.
    * I kept labels leaf-level labels OR depth=2-level labels:
        * leaf-level label count > 500
        * depth=2-level label count was > 500 -- if this was met then the label
          for the corresponding leaf-level label was rolled up to its depth=2-level parent label

    Precision increased substantiall from ~0.21 to ~0.96.
* How did you prune the category tree, and how did that affect your precision?
    * See response above.

## For deriving synonyms from content:
* What were the results for your best model in the tokens used for evaluation?
    ```
    # headphones
    earbud 0.871863
    ear 0.804368
    bud 0.739856
    noise 0.729004

    # nintendo
    wii 0.770601
    ds 0.760249
    game 0.645096
    playstation 0.642175
    ps2 0.64045

    # ps2
    psp 0.83028
    ps3 0.823938
    gba 0.772662
    gamecube 0.727795
    xbox 0.698361

    # plasma
    58 0.771785
    600hz 0.738228
    42 0.694399
    63 0.693472
    hdtv 0.677367
    ```
* What fastText parameters did you use?
    ```
    EPOCHS=25
    MODEL_TYPE="skipgram"
    MIN_COUNT=20
    ```
* How did you transform the product names?
    ```
    cat /workspace/datasets/fasttext/titles.txt | sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_titles.txt
    ```

## For integrating synonyms with search:
* How did you transform the product names (if different than previously)?
I used the same as above.
* What threshold score did you use?
0.8 because I favored precision over recall. Probably should have gone even higher :)
* Were you able to find the additional results by matching synonyms?
Yes, I was able to see the result set increase in number when using the `--synonyms` flag that I added to `query.py`