# Multilabel Section Classification Models

This folder contains our implementation of fine-tuning pre-trained BERT and SciBERT transformer models (from Huggingface), as well as the WideMLP baseline, for scientific section classification.

## Transformers
relevant file: Transformers.ipynb
1. Check for the dependencies listed in the first cell
2. Configure the experimental setup:
    - Indicate the path to the dataset .jsonl file for section classification in the input_path variable
        - note: this file is obtained during sentence extraction in sciSen/ParagraphsToSentences.py > outputPathJson
    - adjust the output_path_model and output_path_results variables to match your folder structure
    - To replicate our experiments, set:
        - BERT or SciBERT in: model_name
        - number of sentences for inputs in: context_width
        - conference ranks in: test_splits

## WideMLP
relevant file: WideMLP.ipynb
1. Check for the dependencies listed in the first cells
2. Configure the experimental setup:
    - Indicate the path to the dataset .jsonl file for section classification in the INPUT_PATH variable
        - note: this file is obtained during sentence extraction in sciSen/ParagraphsToSentences.py > outputPathJson
    - adjust the MODEL_PATH and RESULTS_PATH variables to match your folder structure
    - To replicate our experiments, set:
        - number of sentences for inputs in: context_width
        - conference ranks in: test_splits

## References
    @article{DBLP:journals/corr/abs-1810-04805,
    author    = {Jacob Devlin and
                Ming{-}Wei Chang and
                Kenton Lee and
                Kristina Toutanova},
    title     = {{BERT:} Pre-training of Deep Bidirectional Transformers for Language
                Understanding},
    journal   = {CoRR},
    volume    = {abs/1810.04805},
    year      = {2018},
    url       = {http://arxiv.org/abs/1810.04805},
    archivePrefix = {arXiv},
    eprint    = {1810.04805},
    timestamp = {Tue, 30 Oct 2018 20:39:56 +0100},
    biburl    = {https://dblp.org/rec/journals/corr/abs-1810-04805.bib},
    bibsource = {dblp computer science bibliography, https://dblp.org}
    }

    @inproceedings{beltagy-etal-2019-scibert,
    title = {SciBERT: A Pretrained Language Model for Scientific Text},
    author = {Beltagy, Iz  and Lo, Kyle  and Cohan, Arman},
    booktitle = {EMNLP},
    year = {2019},
    publisher = {Association for Computational Linguistics},
    url = {https://www.aclweb.org/anthology/D19-1371}
    }

    @misc{ACL22MultiLabel,
    doi = {10.48550/ARXIV.2204.03954},
    url = {https://arxiv.org/abs/2204.03954},
    author = {Diera, Andor and Lin, Bao Xin and Khera, Bhakti and Meuser, Tim and Singhal, Tushar and Galke, Lukas and Scherp, Ansgar},
    keywords = {Computation and Language (cs.CL), FOS: Computer and information sciences, FOS: Computer and information sciences},
    title = {Bag-of-Words vs. Sequence vs. Graph vs. Hierarchy for Single- and Multi-Label Text Classification},
    publisher = {arXiv},
    year = {2022},
    copyright = {arXiv.org perpetual, non-exclusive license}
    }


