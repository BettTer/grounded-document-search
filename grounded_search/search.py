from psycopg import Connection
from psycopg.rows import dict_row

SEARCH_SQL = """
WITH input(question, match_mode) AS (VALUES (%s::text, %s::text)),
query AS (
    SELECT CASE WHEN match_mode = 'and'
        THEN plainto_tsquery('english', question)
        ELSE (
            SELECT string_agg(quote_literal(term), ' | ' ORDER BY term)::tsquery
            FROM unnest(tsvector_to_array(to_tsvector('english', question))) AS lexemes(term)
        )
    END AS terms
    FROM input
)
SELECT evidence_id, document_path, title, body, source_url,
       ts_rank_cd(search_vector, terms) AS score
FROM evidence CROSS JOIN query
WHERE corpus_id = %s AND search_vector @@ terms
ORDER BY score DESC, evidence_id COLLATE "C"
LIMIT %s
"""


def search(connection: Connection, corpus_id: str, question: str, limit: int, match_mode: str) -> list[dict]:
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute(SEARCH_SQL, (question, match_mode, corpus_id, limit))
        return cursor.fetchall()
