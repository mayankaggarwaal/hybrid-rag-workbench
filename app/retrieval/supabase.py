import json
from contextlib import closing

import psycopg

from app.embeddings import hash_embedding
from app.models import Document, SearchHit
from app.retrieval.base import RetrievalProvider


class SupabasePostgresProvider(RetrievalProvider):
    """Hosted Supabase Postgres adapter using FTS + pgvector reciprocal-rank fusion."""
    def __init__(self, database_url: str, dimensions: int = 384) -> None:
        self.database_url, self.dimensions = database_url, dimensions

    def index(self, documents: list[Document]) -> None:
        sql = """INSERT INTO knowledge_documents
          (id, workspace_id, resource_type, event_time, title, content, metadata, embedding)
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s::vector)
          ON CONFLICT (id) DO UPDATE SET title=EXCLUDED.title, content=EXCLUDED.content,
          metadata=EXCLUDED.metadata, embedding=EXCLUDED.embedding"""
        with closing(psycopg.connect(self.database_url)) as conn, conn.cursor() as cur:
            for doc in documents:
                vector = doc.embedding or hash_embedding(doc.text, self.dimensions)
                cur.execute(sql, (doc.id, doc.workspace_id, doc.resource_type, doc.event_time,
                                  doc.title, doc.text, json.dumps(doc.metadata), str(vector)))
            conn.commit()

    def search(self, workspace_id: str, query: str, limit: int = 5) -> list[SearchHit]:
        vector = hash_embedding(query, self.dimensions)
        sql = """WITH lexical AS (
            SELECT id, row_number() OVER (ORDER BY ts_rank(search_vector, websearch_to_tsquery('english', %s)) DESC) rank
            FROM knowledge_documents WHERE workspace_id=%s AND search_vector @@ websearch_to_tsquery('english', %s) LIMIT 50
          ), semantic AS (
            SELECT id, row_number() OVER (ORDER BY embedding <=> %s::vector) rank
            FROM knowledge_documents WHERE workspace_id=%s LIMIT 50
          ) SELECT d.id,d.workspace_id,d.resource_type,d.event_time,d.title,d.content,d.metadata,
              30.0 * (COALESCE(1.0/(60+l.rank),0)+COALESCE(1.0/(60+s.rank),0)) score
            FROM lexical l FULL JOIN semantic s USING(id) JOIN knowledge_documents d ON d.id=COALESCE(l.id,s.id)
            ORDER BY score DESC LIMIT %s"""
        with closing(psycopg.connect(self.database_url)) as conn, conn.cursor() as cur:
            cur.execute(sql, (query, workspace_id, query, str(vector), workspace_id, limit))
            return [SearchHit(Document(str(r[0]), r[1], r[2], r[3].isoformat(), r[4], r[5], r[6]), float(r[7])) for r in cur.fetchall()]

    def timeline(self, workspace_id: str, limit: int = 50) -> list[Document]:
        with closing(psycopg.connect(self.database_url)) as conn, conn.cursor() as cur:
            cur.execute("SELECT id,workspace_id,resource_type,event_time,title,content,metadata FROM knowledge_documents WHERE workspace_id=%s ORDER BY event_time DESC LIMIT %s", (workspace_id, limit))
            return [Document(str(r[0]), r[1], r[2], r[3].isoformat(), r[4], r[5], r[6]) for r in cur.fetchall()]

