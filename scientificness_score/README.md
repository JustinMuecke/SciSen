# scientificness_score

This Directory holds all files to train models for the scientificness score task as well as code for evaluation and visualization.


## [nonSciSciClassifier](/nonSciSciClassifier.ipynb)

Jupyter Notebook containing the Code to train the BERT and SciBERT Huggingface transformers.
Logging of these trainings was done using the [weights and biases](https://wandb.ai/) tool.

## [inv_model](\inv_model.ipnyb)

Jupyter notebook containing the code to evaluate the transformer models

## [inv_token](/inv_token.ipnyb)

Jupyter notebook containing the code to  the influence of \<equation\> and \<reference\> tokens on the transformer models



##  [wide](/wide.ipynb)

Jupyter Notebook containing the Code to train the bag-of-words WideMLP model.
Logging of these trainings was done using the [weights and biases](https://wandb.ai/) tool.

Additionally, the Evaluation of a disjunct set of sentences as well as the investigation of the influence of \<equation\> and \<reference\> tokens is contained in this notebook


## [Models](/Models)

Contains all the trained models necessary to rerun the experiments.

## [Pickeled Opjects](//Pickled_Object)
Contains all serialized Analysis results using the Pickle Library


## [Sentence Evals](/SentenceEvals)
Contains all Analysis Results in txt format