from typing import List, Dict

def get_evidence_chunks(municipality: str) -> List[Dict]:
    # TODO: Firestore / Vector Search に差し替え
    return [
        {"page": 2, "source_url": "https://example.go.jp/program.pdf", "snippet": "対象者：18歳以上39歳以下の単身者"},
        {"page": 5, "source_url": "https://example.go.jp/program.pdf", "snippet": "申請期限：2026年2月28日まで"},
        {"page": 6, "source_url": "https://example.go.jp/program.pdf", "snippet": "申請時に学生証の提出が必要"},
    ]
