# MS MARCO LLM Distillation

This repository contains the code and data for the paper [`Rank-DistiLLM: Closing the Effectiveness Gap Between Cross-Encoders and LLMs for Passage Re-ranking`](https://webis.de/publications.html#schlatt_2025c) accepted at ECIR'25.

## Usage

We use the [`lightning-ir`](https://github.com/webis-de/lightning-ir) library for fine-tuning and running experiments. Follow the installation instructions from the repository to install the library.

## Model Zoo

| Model Name                                                          | TREC DL 19/20 nDCG@10 (BM25) | TIREx nDCG@10 |
| ------------------------------------------------------------------- | ---------------------------- | ------------- |
| [monoelectra-base](https://huggingface.co/webis/monoelectra-base)   | 0.715                        | 0.416         |
| [monoelectra-large](https://huggingface.co/webis/monoelectra-large) | 0.730                        | 0.434         |

### Data

The run files for MS MARCO training queries for different first-stage retrieval models and LLM re-rankers can be downloaded from [Zenodo](https://zenodo.org/records/11147862).

### Fine-tuning

To fine-tune a model using ColBERTv2 hard negatives, update the `train_dataset` argument in `configs/monoelectra-fine-tune-colbert.yaml` to point to the downloaded ColBERTv2 run file.

Then run the following command to fine-tune the model:

```bash
lightning-ir fit --config configs/monoelectra-fine-tune-colbert.yaml
```

To fine-tune a model using our proposed distillation method, update the `train_dataset` argument in `configs/monoelectra-fine-tune-distillation.yaml` to point to the downloaded distillation run file.

Then run the following command to fine-tune the model:

```bash
lightning-ir fit --config configs/monoelectra-fine-tune-distillation.yaml
```

### Inference

We provide an example configuration file for running inference on TREC Deep Learning 2019 and 2020 using our fine-tuned models in `configs/predict-trec-dl.yaml`.

To re-rank passages, run the following command (this will download the fine-tuned from HuggingFace and the MS MARCO passage corpus using [`ir_datasets`](https://ir-datasets.com/)):

```bash
lightning-ir re_rank --config configs/predict-trec-dl.yaml
```

## Citation

```bibtex
@InProceedings{schlatt:2025,
  address =                  {Berlin Heidelberg New York},
  author =                   {Ferdinand Schlatt and Maik Fr{\"o}be and Harrisen Scells and Shengyao Zhuang and Bevan Koopman and Guido Zuccon and Benno Stein and Martin Potthast and Matthias Hagen},
  booktitle =                {Advances in Information Retrieval. 47th European Conference on IR Research (ECIR 2025)},
  doi =                      {10.1007/978-3-031-88714-7_31},
  month =                    apr,
  publisher =                {Springer},
  series =                   {Lecture Notes in Computer Science},
  site =                     {Lucca, Italy},
  title =                    {{Rank-DistiLLM: Closing the Effectiveness Gap Between Cross-Encoders and LLMs for Passage Re-ranking}},
  year =                     2025
}
```
