# SciSen: Towards a Scientific Writing Feedback System

## About

Writing scientific papers poses several challenges. It is often not clear how to write text using scientific vocabulary as opposed to
colloquial language. Also, organising content into sections poses a challenge, as different information should be provided in different sections. We present SciSen, a system consisting of three components to support writers. Firstly, we propose a classifier trained on a corpus of scientific sentences extracted from peer reviewed scientific papers and non-scientific sentences collected from reddit, twitter, and science fiction books. The model gives researchers feedback if a written sentence is on the same scientific level as published papers. Secondly, we classify a sentence as to which section it belongs. We created a mapping of available section titles of published papers onto a standard paper layout. Given a sentence and its context, this model can classify to which section the sentence should belong. Finally, we propose a paraphraser that aims to enhance the scientific style of a sentence by providing suggestions for word replacements, additions to the sentence, and structural changes. Models are tested and evaluated on a dataset based on the Papers with Code database, containing 307.318 papers from differently ranked conferences. All three components achieve good levels of performance. We achieved a scientificness score to reliably evaluate if a sentence matches the linguistic level of published papers. Here, the baseline WideMLP outperformed the transformer. For the section classification, transformer models outperform the WideMLP baseline, with BERT achieving better results than SciBERT in most cases. While the paraphrasers’ make comparatively few alterations, they succeed in producing output sentences close to a gold standard. Large fine-tuned models perform best.


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


## Project-Intern Resources

### [MiroBoard](https://miro.com/app/board/uXjVPPtYGO8=/)
### [Minutes_Notepad](https://newpad.stuve.uni-ulm.de/yPRbaLXbS6CtXm5df7_j5w#)
### [Texfiles](https://cloudstore.uni-ulm.de/s/DJyRaGWpczwMq2k)
### [ScientificParagraphsAndSentencesDataCollection](https://cloudstore.uni-ulm.de/s/LHat94HqyEt856b)
### [NonScientificSentencesDataCollection](https://cloudstore.uni-ulm.de/s/YYqcpYqWQ5o8QYq)


