# SciSen: Fine-Tuning Language Models for Scientific Writing Support

## About

We support scientific writers in determining whether a written sentence is scientific, to which section it belongs, and what paraphrasing could be done to improve a sentence. Firstly, we propose a regression model trained on a corpus of scientific sentences extracted from peer-reviewed scientific papers and non-scientific sentences collected from Reddit, Twitter, and science fiction books. The goal is to assign a score to a written sentence to indicate if it is on a similar scientific level as published papers. Secondly, we classify a sentence in the section in which it belongs. We create a mapping of section titles of published papers onto a standard paper layout. Given a sentence and different amounts of context, the goal is to classify to which section the sentence most likely belongs. Finally, we propose a paraphraser, which aims to improve the scientific style of a sentence by suggesting an alternative sentence that may include word substitutions, additions to the sentence, and structural changes. Our Models are trained and evaluated on a dataset based on the Papers with Code database, containing 307,318 papers from differently ranked conferences. All three components achieve good levels of performance. The scientificness score reliably evaluates whether a sentence matches the linguistic level of published papers. Here, the baseline WideMLP outperforms transformer models. For the section classification, transformer models outperform the WideMLP baseline, with BERT achieving better results than SciBERT in most cases. While the paraphrasing transformers make comparatively few alterations, they succeed in producing output sentences close to the gold standard. Large fine-tuned models such as T5 Large perform best in experiments considering various measures of difference between input sentence and gold standard.


## Contact
 * [JustinMücke](mailto:justin.muecke@uni-ulm.de)
 * [LuiseMetzger](mailto:luise.metzger@uni-ulm.de)
 * [PhilippSchauz](mailto:philipp.schauz@uni-ulm.de)
 * [DariaWaldow](mailto:dario.waldow@uni-ulm.de)

## Prerequisites
We run our experiments on a server with CUDA 11.7 and A-100 GPUs and the packages provided in the requirements.txt. 

## [scientificness_score](/scientificness_score)

Given sentences from scientific or non-scientific background, we fine-tune two transformer models, SciBERT and BERT, as
well as an WideMLP model to create a score which indicates how
scientific a sentence is written.

##  [section-classification](/section-classification)

Considering the paragraph structure, we ine-tune models using sentences from scientific papers labelled with their structural context, i.e. the type of section within the typical scientific paper structure (introduction, related work, method, experiment, result, discussion, conclusion) they originate from. 

## [paraphraser](/paraphraser)
We aim to paraphrase sentences into a more scientific style. In order to achieve this, we employ a Paraphraser based on the Pegasus model as well as a Insert Delete and Modify method used with BERT to distort and reconstruct sentences to create a training dataset.
This dataset is then used to finetune T5 and BART models.


## [nonSciSen](/nonSciSen)

This Folder contains any preprocessing done to none scientifc sentences from different origins

## [sciSen](/sciSen)

Here, the acquisition of raw LaTeX files as well as the subsequent extraction and preprocessing of the scientific sentences can be found 


