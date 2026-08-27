from fastapi import APIRouter
from app.evaluation.runner import EvaluationRunner
from app.core.responses import success_response

router = APIRouter()
eval_runner = EvaluationRunner()

@router.get("/run")
async def run_evaluation():
    report = await eval_runner.run_benchmark()
    return success_response(report)
