from fastapi import APIRouter
from ....schemas.request import EligibilityRequest
from ....schemas.response import EligibilityResponse
from ....services.retriever_stub import get_evidence_chunks
from ....services.judge_gemini import judge_with_gemini

router = APIRouter()

@router.post("/eligibility", response_model=EligibilityResponse)
def eligibility(req: EligibilityRequest):
    municipality = req.municipality or "○○市"
    evidence = get_evidence_chunks(municipality)

    # MVP：とりあえず1制度だけ判定（後で複数制度resultsへ拡張）
    judged = judge_with_gemini(
        program_id="xxx_001",
        evidence=evidence,
        user_payload=req.model_dump()
    )

    return {
        "municipality": municipality,
        "results": [
            {
                "program_id": judged.get("program_id", "xxx_001"),
                "program_name": "○○市 若年単身者支援金",
                "level": judged["level"],
                "confidence": float(judged.get("confidence", 0.0)),
                "reasons": judged.get("reasons", []),
                "deadline": judged.get("deadline", {"date": None, "evidence_ref": None}),
                "todo": judged.get("todo", []),
                "evidence": judged.get("evidence", evidence),
            }
        ],
        "meta": {"model": "vertexai-gemini", "version": "mvp-0.1"},
    }
