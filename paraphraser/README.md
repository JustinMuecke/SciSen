# Paraphrasing
This folder contains the data preparation/creation of the parallel dataset, the training procedure and our evaluation for the scientific paraphrasing.

## Prepare Paraphrasing
This notebook contains the dataset for the Pegasus-DS with respective WER scores and the IDM-DS with an implementation of the IDM method. 

## Training Paraphraser
This notebook contains a config in the beginning which allows to adjust the parameters relevant for our experiments including hyperparameter tuning. The notebook saves the model_checkpoints accoding to the specified hyperparameters and dataset. 
The batch size provides a reference  size on our GPUs.

The notebook can be converted to a python file with jupyter nbconvert TrainingParaphraser.ipynb 
For this to work the line in the beginning `%env PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` needs to be removed.
Afterwards the Hyperparameters can be adjusted on the top of the python file.

To reproduce our results we provide a python list with our experimental setup which allows to select the required parameters.
* path: provides the general location to save: 
    * the models: /models/style
    * the tokenized dataset: datasets/style/tokenized/
    
## Evaluation Paraphraser
This notebook contains a config to load respective fine-tuned models. Then it allows to evaluate the performance of the models on the datasets Pegasus-DS, IDM-DS and GYAFC. Furthermore, it is possible to calculate the results of the reference models by loading their respective model outputs. 

The notebook can be converted to a python file with jupyter nbconvert EvaluationParaphraser.ipynb 
For this to work the line in the beginning `%env PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` needs to be removed.
Afterwards the Hyperparameters can be adjusted on the top of the python file.

To reproduce our results we provide a python list with our experimental setup which allows to select the required parameters.
* model_path: should contain the finetuned models with the defined naming structure containing the dataset and parameters
* dataset_path: the path for the gyafc dataset and the datasets generated during the Preparation
* output_path: location for the model outputs in case of the test split of Pegasus-DS and IDM-DS
