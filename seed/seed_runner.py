import asyncio
from app.retrieval.hybrid_retriever import hybrid_retriever, RetrievedChunk

async def seed_database():
    print("Seeding NovaStack Technologies knowledge and telemetry into AegisAI...")
    
    # 1. Seed Core Documentation Chunks
    docs = [
        ("doc_01", "NovaStack Auth Architecture", "NovaStack uses stateless JWT access tokens with 60-minute expiration, Argon2id password hashing, and Redis-backed session invalidation. Row-Level Security enforces tenant boundaries."),
        ("doc_02", "Payment Service Architecture", "The payment-service connects directly to payments_db (PostgreSQL 16) and interfaces with Stripe API. It handles authorizations, captures, refunds, and webhooks."),
        ("doc_03", "Incident INC-2841 Post-Mortem", "Incident INC-2841 occurred on 2026-08-27. Deployment v2.8 for payment-service expected column stripe_customer_id on payments table, but migration 042_add_stripe_id.sql was omitted. Remediated by running alembic upgrade 042."),
        ("doc_04", "Service Dependency Map", "api-gateway routes to auth-service and order-service. order-service synchronously calls payment-service and asynchronously emits events to notification-service."),
        ("doc_05", "Database Schemas", "users_db stores users and memberships. orders_db stores customer orders. payments_db stores transactions and stripe_customer_id. analytics_db aggregates business KPIs.")
    ]
    
    for doc_id, title, content in docs:
        hybrid_retriever.index_chunk(RetrievedChunk(
            chunk_id=f"chk_{doc_id}",
            document_id=doc_id,
            title=title,
            content=content,
            score=1.0,
            retrieval_source="seed",
            metadata={"type": "documentation", "org": "NovaStack"}
        ))
    
    print(f"Successfully seeded {len(docs)} foundational knowledge chunks.")

if __name__ == "__main__":
    asyncio.run(seed_database())
