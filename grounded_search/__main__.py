import argparse
import os

import psycopg

from .index import read_evidence, replace_evidence

DEFAULT_DATABASE_URL = "postgresql://grounded:grounded@127.0.0.1:55432/grounded"


def main() -> None:
    parser = argparse.ArgumentParser(description="Grounded Document Search")
    commands = parser.add_subparsers(dest="command", required=True)
    index = commands.add_parser("index", help="Index the English evidence for a corpus.")
    index.add_argument("--corpus", required=True)
    args = parser.parse_args()

    try:
        evidence = read_evidence(args.corpus)
        database_url = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
        with psycopg.connect(database_url, connect_timeout=5) as connection:
            replace_evidence(connection, args.corpus, evidence)
        print(f"Indexed {len(evidence)} evidence sections for {args.corpus}.")
    except (ValueError, OSError, psycopg.Error) as error:
        parser.exit(1, f"Indexing failed: {error}\n")


if __name__ == "__main__":
    main()
