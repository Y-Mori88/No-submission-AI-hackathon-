"use client";
import { useState } from "react";
import { postEligibility } from "@/lib/api";

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    setErr(null);
    try {
      const data = await postEligibility({
        age: 25,
        income_yen: 3200000,
        household: 2,
        occupation: "student",
      });
      setResult(data);
    } catch (e: any) {
      setErr(e?.message ?? "unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: 24 }}>
      <h1>補助金 判定デモ</h1>
      <button onClick={run} disabled={loading}>
        {loading ? "判定中..." : "判定する"}
      </button>
      {err && <p style={{ color: "tomato" }}>{err}</p>}
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </main>
  );
}
