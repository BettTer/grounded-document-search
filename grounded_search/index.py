import re
from pathlib import Path

from psycopg import Connection

SECTION = re.compile(r"^## (.+)$", re.MULTILINE)
EVIDENCE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
BILINGUAL_BODY = re.compile(
    r"### English\n\s*(?P<english>.+?)\n### 简体中文\n\s*"
    r"(?P<chinese>.+?)\n\s*\[[^\]\n]+\]\((?P<url>https://[^\s)]+)\)\s*",
    re.DOTALL,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS evidence (
    corpus_id text NOT NULL,
    evidence_id text NOT NULL,
    document_path text NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    source_url text NOT NULL,
    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', title), 'A') ||
        setweight(to_tsvector('english', body), 'D')
    ) STORED,
    PRIMARY KEY (corpus_id, evidence_id)
);
CREATE INDEX IF NOT EXISTS evidence_search_idx ON evidence USING gin (search_vector);
"""

INSERT = """
INSERT INTO evidence (corpus_id, evidence_id, document_path, title, body, source_url)
VALUES (%s, %s, %s, %s, %s, %s)
"""


def read_evidence(corpus_id: str) -> list[tuple[str, str, str, str, str, str]]:
    if not EVIDENCE_ID.fullmatch(corpus_id):
        raise ValueError("Corpus ID must use lowercase letters, numbers and hyphens.")

    folder = Path("corpora") / corpus_id
    evidence = []
    seen_ids = set()
    for path in sorted(folder.glob("*.md")):
        intro, *sections = SECTION.split(path.read_text(encoding="utf-8"))
        title_line = intro.strip()
        title = title_line.removeprefix("# ").partition(" / ")[0]
        if not title_line.startswith("# ") or "\n" in title_line or not title.strip():
            raise ValueError(f"{path}: expected a document title.")
        if not sections:
            raise ValueError(f"{path}: expected at least one evidence section.")

        for evidence_id, content in zip(sections[::2], sections[1::2]):
            if not EVIDENCE_ID.fullmatch(evidence_id) or evidence_id in seen_ids:
                raise ValueError(f"{path}: invalid or duplicate evidence ID: {evidence_id}")
            match = BILINGUAL_BODY.fullmatch(content.strip())
            if not match or not match["english"].strip() or not match["chinese"].strip():
                raise ValueError(f"{path}#{evidence_id}: expected English, Chinese and a source link.")
            seen_ids.add(evidence_id)
            evidence.append(
                (corpus_id, evidence_id, path.as_posix(), title.strip(), match["english"].strip(), match["url"])
            )

    if not evidence:
        raise ValueError(f"No evidence documents found in {folder}.")
    return evidence


def replace_evidence(connection: Connection, corpus_id: str, evidence: list[tuple]) -> None:
    with connection.transaction(), connection.cursor() as cursor:
        cursor.execute(SCHEMA)
        cursor.execute("LOCK TABLE evidence IN SHARE ROW EXCLUSIVE MODE")
        cursor.execute("DELETE FROM evidence WHERE corpus_id = %s", (corpus_id,))
        cursor.executemany(INSERT, evidence)
