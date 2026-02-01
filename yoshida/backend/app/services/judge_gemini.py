import json
from typing import Dict, Any, List

from vertexai import init
from vertexai.generative_models import GenerativeModel

from ..core.config import settings

FORCED_FORMAT = {
  "program_id": "xxx_001",
  "level": "high | medium | low | unknown",
  "confidence": 0.0,
  "reasons": [{"text": "理由の説明文", "evidence_ref": 0}],
  "deadline": {"date": "YYYY-MM-DD | null", "evidence_ref": 1},
  "todo": [{"text": "ユーザーが最初にやるべき行動", "evidence_ref": 2}],
  "evidence": [{"page": 0, "source_url": "", "snippet": ""}]
}

SYSTEM_PROMPT = """あなたは自治体の補助金制度について、与えられた根拠（EVIDENCE）だけを用いて
対象可能性を High/Medium/Low/Unknown のいずれかで判定するアシスタントです。

制約:
- EVIDENCE に書かれていない情報を推測・補完・捏造してはいけません。
- 理由(reasons)、やること(todo)、期限(deadline)に書く主張は、必ず根拠を1つ以上参照してください。
- 根拠が不足する場合は level="unknown" とし、deadline.date は null にしてください。
- 出力は JSON のみ。JSON の外側に説明文、コードブロック、前置き、後置きを一切書かないでください。
- evidence_ref は evidence 配列の 0 始まりインデックスです。
"""

def _safe_json_parse(text: str) -> Dict[str, Any]:
    # 余計な文字が混ざる事故対策：最初の { から最後の } を抜く
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no json object found")
    return json.loads(text[start:end+1])

def judge_with_gemini(program_id: str, evidence: List[Dict[str, Any]], user_payload: Dict[str, Any]) -> Dict[str, Any]:
    if not settings.gcp_project:
        # ローカルで Vertex 未設定ならunknownで返す（開発体験優先）
        return {
            "program_id": program_id,
            "level": "unknown",
            "confidence": 0.0,
            "reasons": [{"text": "GCP設定が未入力のため判定できない", "evidence_ref": 0}],
            "deadline": {"date": None, "evidence_ref": None},
            "todo": [{"text": "GCP_PROJECT / 認証設定を行う", "evidence_ref": 0}],
            "evidence": evidence,
        }

    init(project=settings.gcp_project, location=settings.gcp_region)
    model = GenerativeModel(settings.gemini_model)

    prompt = {
        "user_input": user_payload,
        "program_id": program_id,
        "evidence": evidence,
        "output_format_example": FORCED_FORMAT
    }

    resp = model.generate_content(
        [SYSTEM_PROMPT, json.dumps(prompt, ensure_ascii=False)],
        generation_config={"temperature": 0.2, "max_output_tokens": 1200},
    )

    data = _safe_json_parse(resp.text)

    # 最低限の後処理（不足時はunknownに寄せる）
    data.setdefault("program_id", program_id)
    data.setdefault("evidence", evidence)
    if data.get("level") not in ["high", "medium", "low", "unknown"]:
        data["level"] = "unknown"
    if not isinstance(data.get("confidence", 0.0), (int, float)):
        data["confidence"] = 0.0
    return data
