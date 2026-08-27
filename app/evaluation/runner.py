import asyncio
from typing import List, Dict, Any
from app.evaluation.metrics import eval_metrics
from app.agents.runtime import agent_runtime

DEFAULT_BENCHMARK = [
    {
        "question": "What is our authentication architecture?",
        "ground_truth": "JWT access tokens with Argon2 password hashing and Redis session store.",
        "category": "knowledge"
    },
    {
        "question": "Why did INC-2841 happen in payment service?",
        "ground_truth": "Deployment v2.8 was rolled out without executing migration 042_add_stripe_id.sql.",
        "category": "incident"
    },
    {
        "question": "Show failed payments in database",
        "ground_truth": "SELECT id, order_id, amount, status FROM payments WHERE status = 'FAILED'",
        "category": "sql"
    }
]

class EvaluationRunner:
    async def run_benchmark(self, dataset: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = dataset or DEFAULT_BENCHMARK
        results = []
        faith_scores = []
        recall_scores = []
        relevance_scores = []

        for item in data:
            q = item["question"]
            gt = item["ground_truth"]
            state = await agent_runtime.execute(q)
            
            context_texts = [str(e) for e in state.evidence] if state.evidence else [state.final_answer]
            faith = eval_metrics.calculate_faithfulness(state.final_answer, context_texts)
            recall = eval_metrics.calculate_context_recall(gt, [state.final_answer] + context_texts)
            relevance = eval_metrics.calculate_answer_relevancy(q, state.final_answer)

            faith_scores.append(faith)
            recall_scores.append(recall)
            relevance_scores.append(relevance)

            results.append({
                "question": q,
                "answer": state.final_answer[:150] + "...",
                "faithfulness": faith,
                "context_recall": recall,
                "answer_relevancy": relevance,
                "execution_ms": state.execution_time_ms
            })

        avg_faith = round(sum(faith_scores) / len(faith_scores), 4)
        avg_recall = round(sum(recall_scores) / len(recall_scores), 4)
        avg_relevancy = round(sum(relevance_scores) / len(relevance_scores), 4)
        passed_gate = avg_faith >= 0.80 and avg_recall >= 0.70

        return {
            "total_questions": len(data),
            "overall_faithfulness": avg_faith,
            "overall_context_recall": avg_recall,
            "overall_answer_relevancy": avg_relevancy,
            "passed_regression_gate": passed_gate,
            "results": results
        }
