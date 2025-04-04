import re
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

RUN_HEADER = ["query_id", "q0", "doc_id", "rank", "score", "system"]


def main(args=None):
    parser = ArgumentParser()

    parser.add_argument("--rank_gpt_file", type=Path, required=True)
    parser.add_argument("--first_stage_file", type=Path, required=True)
    parser.add_argument("--sub_sample_sizes", type=int, required=True, nargs="+")

    args = parser.parse_args(args)

    rank_gpt_run = (
        pd.read_csv(args.rank_gpt_file, sep=r"\s+", names=RUN_HEADER).set_index(["query_id", "doc_id"]).sort_index()
    )
    first_stage_run = (
        pd.read_csv(args.first_stage_file, sep=r"\s+", names=RUN_HEADER).set_index(["query_id", "doc_id"])
    ).drop(columns=["q0", "system", "score"])
    rank_gpt_run = rank_gpt_run.merge(first_stage_run, on=["query_id", "doc_id"], suffixes=["", "_first_stage"])

    for sub_sample_size in args.sub_sample_sizes:
        sub_sample_run = (
            rank_gpt_run.loc[rank_gpt_run["rank_first_stage"] <= sub_sample_size]
            .reset_index()
            .drop(columns=["rank_first_stage"])
        )
        sub_sample_run["rank"] = (
            sub_sample_run.groupby("query_id")["score"].rank(ascending=False, method="first").astype(int)
        )
        sub_sample_run = sub_sample_run.sort_values(["query_id", "rank"], ascending=[True, True])
        sub_sample_run = sub_sample_run.loc[:, RUN_HEADER]
        file_name = args.rank_gpt_file.name
        file_name = re.sub(r"sampled-\d+", f"sampled-{sub_sample_size}", file_name)
        sub_sample_run.to_csv(
            args.rank_gpt_file.with_name(file_name),
            sep="\t",
            index=False,
            header=False,
        )


if __name__ == "__main__":
    main()
