import argparse
import json
import os
from pathlib import Path

import psycopg

from .evaluation import evaluate
from .index import read_evidence, replace_evidence
from .search import search

DEFAULT_DATABASE_URL = "postgresql://grounded:grounded@127.0.0.1:55432/grounded"


def positive_limit(value: str) -> int:
    limit = int(value)
    if limit < 1:
        raise argparse.ArgumentTypeError("K must be a positive integer.")
    return limit


def main() -> None:
    parser = argparse.ArgumentParser(description="Grounded Document Search")
    commands = parser.add_subparsers(dest="command", required=True)
    index = commands.add_parser("index", help="Index the English evidence for a corpus.")
    index.add_argument("--corpus", required=True)
    query = commands.add_parser("search", help="Find and rank evidence using keyword search.")
    query.add_argument("question")
    query.add_argument("--k", type=positive_limit, default=5)
    report = commands.add_parser("eval", help="Evaluate keyword evidence retrieval.")
    report.add_argument("--dataset", type=Path, required=True)
    for command in (query, report):
        command.add_argument("--corpus", required=True)
        command.add_argument("--match", choices=("or", "and"), default="or")
    args = parser.parse_args()

    try:
        database_url = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
        if args.command == "index":
            evidence = read_evidence(args.corpus)
            with psycopg.connect(database_url, connect_timeout=5) as connection:
                replace_evidence(connection, args.corpus, evidence)
            print(f"Indexed {len(evidence)} evidence sections for {args.corpus}.")
            return

        with psycopg.connect(database_url, connect_timeout=5) as connection:
            if args.command == "search":
                hits = search(connection, args.corpus, args.question, args.k, args.match)
                result = [{"rank": rank, **hit} for rank, hit in enumerate(hits, start=1)]
            else:
                result = evaluate(connection, args.corpus, args.dataset, args.match)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, psycopg.Error) as error:
        parser.exit(1, f"{args.command} failed: {error}\n")


if __name__ == "__main__":
    main()
