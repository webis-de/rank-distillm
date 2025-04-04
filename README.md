# Rank-DistiLLM

This repository contains the code and data for the paper [`Rank-DistiLLM: Closing the Effectiveness Gap Between Cross-Encoders and LLMs for Passage Re-ranking`](https://webis.de/publications.html#schlatt_2025c) accepted at ECIR'25.

## Usage

We use the [`lightning-ir`](https://github.com/webis-de/lightning-ir) library for fine-tuning and running experiments. Follow the installation instructions from the repository to install the library.

## Model Zoo

| Model Name                                                                | TREC DL 19 (BM25) | TREC DL 20 (BM25) | TREC DL 19 (ColBERTv2) | TREC DL 20 (ColBERTv2) |
| ------------------------------------------------------------------------- | ----------------- | ----------------- | ---------------------- | ---------------------- |
| [webis/monoelectra-base](https://huggingface.co/webis/monoelectra-base)   | 0.721             | 0.711             |  0.770                 |  0.770                 |
| [webis/monoelectra-large](https://huggingface.co/webis/monoelectra-large) | 0.732             | 0.727             |  0.766                 |  0.796                 |

(nDCG@10 on TREC DL 19 and TREC DL 20)


To reproduce the results, run the following command:

```bash
lightning-ir re_rank --config ./configs/re-rank.yaml --model.model_name_or_path <MODEL_NAME>
```

### Data

The ColBERTv2 distillation data from Rank-DistiLLM is directly integrated into lightning-ir with the dataset id `msmarco-passage/train/rank-distillm-rankzephyr`. You can use this dataset id in the `data.train_dataset.run_path_or_id` argument of the configuration files.

The run files for MS MARCO training queries for different first-stage retrieval models and LLM re-rankers can be downloaded from [Zenodo](https://zenodo.org/records/15131907).

## Fine-Tuning

Pre-fine-tuning (first stage fine-tuning using positive samples from MS MARCO and hard-negatives sampled using ColBERTv2 with InfoNCE) can be done using the following command.

```bash
lightning-ir fit --config ./configs/pre-finetune.yaml
```

The model can be further fine-tuned (second stage fine-tuning using the RankDistiLLM dataset with RankNet or Approx Discounted Rank-MSE loss) using the following command. The model checkpoint from the pre-fine-tuning stage can be used as a starting point.

```bash
lightning-ir fit --config ./configs/fine-tune.yaml
```

## Reproduction

We have uploaded the run files to reproduce the results in [Zenodo](https://zenodo.org/records/15150456). Download and unpack the `experiments.tar.gz` file and then run the `notebooks/effectiveness.ipynb` notebook to reproduce the results.


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
