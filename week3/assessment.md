# Assessment

## For query classification:
- How many unique categories did you see in your rolled up training data when you set the minimum number of queries per category to 1000? To 10000?
    * min_queries=1000: 380
    * min_queries=10000: 68

- What were the best values you achieved for R@1, R@3, and R@5? You should have tried at least a few different models, varying the minimum number of queries per category, as well as trying different fastText parameters or query normalization. Report at least 2 of your runs.

  * Run 1
    * Params:
        * min_queries=1000
        * epochs=25
        * lr=0.25
        * wordNgrams=2
    * Recall:
        * R@1 = 0.462
        * R@3 = 0.616
        * R@5 = 0.673

  * Run 2
    * Params:
        * min_queries=1000
        * epochs=25
        * lr=0.25
        * wordNgrams=2
    * Recall:
        * R@1 = 0.569
        * R@3 = 0.737
        * R@5 = 0.821

## For integrating query classification with search: ###
- Give 2 or 3 examples of queries where you saw a dramatic positive change in the results because of filtering. Make sure to include the classifier output for those queries.

* "sony over the ear headphones"
  * Went from 7980 results to 641. Top results were the similar.

    ```
    pcmcat144700050004	0.602
    pcmcat143000050011	0.345
    pcmcat171900050028	0.022
    pcmcat248700050021	0.006
    pcmcat143000050007	0.005
    abcat0208011    	0.003
    abcat0303000    	0.002
    pcmcat246100050002	0.001
    cat02015        	0.001
    cat02010        	0.001
    ```

* "counter top dishwasher"
  * The top results went from gift cards (LOL) to at least counter top appliances.
    ```
    abcat0102008    	0.306
    abcat0912000    	0.219
    abcat0900000    	0.076
    abcat0905001    	0.055
    pcmcat167300050040	0.053
    cat02015        	0.039
    abcat0910001    	0.015
    abcat0903000    	0.011
    pcmcat219900050000	0.010
    pcmcat243000050004	0.007
    ```
* "ipod nano"
  * Top results stopped including accessories.
    ```
    abcat0201011    	0.638
    pcmcat144000050001	0.082
    abcat0208008    	0.061
    pcmcat191200050015	0.058
    abcat0200000    	0.030
    pcmcat165900050054	0.029
    abcat0208007    	0.009
    abcat0106001    	0.009
    pcmcat186400050010	0.008
    pcmcat209400050001	0.008
    ```
- Give 2 or 3 examples of queries where filtering hurt the results, either because the classifier was wrong or for some other reason. Again, include the classifier output for those queries.
* "sonic the hedgehog"
  * Results in a null query since it is classified as "Movies and TV shows" but sonic is a video game.
    ```
    cat02015        	0.595
    pcmcat232900050017	0.113
    abcat0703002    	0.084
    cat02010        	0.044
    abcat0706002    	0.026
    cat02661        	0.015
    cat02009        	0.015
    cat02685        	0.012
    abcat0707002    	0.008
    cat02673        	0.008
    ```