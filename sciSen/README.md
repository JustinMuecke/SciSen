# Extraction of Scientific Sentences from the LaTeX files

This folder contains the files for extracting sentences from scientific papers' LaTeX files, i.e. creation of our scientific sentences datasets.

## How To:
1. TexToParagraphs.py
    * place LaTeX files of ranked papers in subdirectories matching their rank and adjust InputPath_tex to match
    * adjust OutputhPath_selected_paragraphs (selected sentences for section classification) and OutputPath_all_paragraphs (all sentences) to desired paths
    * run TexToParagraphs.py
2. ParagraphsToSentences.py
    * to obtain full dataset of sentences:
        * set SaveAsParagraphs = False
        * set dataPath to match TexToParagraphs.py's OutputPath_all_paragraphs / place the respective .jsonl file on desired path
        * set statisticsPath to your preferred path for saving information about the sentence extraction process
        * set outputPathTxt to your preferred path
        * run ParagraphsToSentences.py
    * to obtain dataset for section classification:
        * set SaveAsParagraphs = True
        * set dataPath to match TexToParagraphs.py's OutputPath_selected_paragraphs / place the respective .jsonl file on desired path
        * set statisticsPath to your preferred path for saving information about the sentence extraction process
        * set outputPathJson and outputPathTxt to your preferred paths
        * run ParagraphsToSentences.py

## References & Acknowledgements
Random names list taken from Kaggle:
https://www.kaggle.com/datasets/jojo1000/facebook-last-names-with-count?resource=download

Permissible Titles and synonym mappings for the section classification task are based on
CiteWorth's https://github.com/copenlu/cite-worth/blob/main/dataset_creation/data/permissible_section_titles.txt
and Danial Podjavorsek's dictionary mapping of section headings to categories


## [arXiv-crawler-master](sciSen/arXiv-crawler-master)
The arXiv crawler by Simon Birkholz was used to investigate if crawling makes sense in our context. 
We decided to use the data provided by [arXiv](https://info.arxiv.org/help/bulk_data_s3.html) on Amazon S3. Therefore, this folder contains the procedure to extract the selected papers (e.g. containing conference). The project was then mainly used to extract the provided data into a single Latex .tex-file.
This can be seen in  [InvestigatePapersToCrawl.ipynb](sciSen/arXiv-crawler-master/InvestigatePapersToCrawl.ipynb)
