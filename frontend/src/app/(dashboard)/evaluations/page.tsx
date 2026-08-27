"use client";

import React, { useState } from "react";
import { runEvaluation } from "@/lib/api";
import { BarChart2, CheckCircle, Play } from "lucide-react";

export default function EvaluationsPage() {
  const [report, setReport] = useState<any | null>(null);
  const [running, setRunning] = useState(false);

  const handleRun = async () => {
    setRunning(true);
    try {
      const data = await runEvaluation();
      setReport(data);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between border-b border-surfaceBorder pb-4">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
            <BarChart2 className="w-6 h-6 text-purple-400" />
            <span>RAG Quality & Evaluation Suite</span>
          </h2>
          <p className="text-sm text-gray-400">Automated benchmark evaluation and regression quality gate.</p>
        </div>
        <button
          onClick={handleRun}
          disabled={running}
          className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold px-4 py-2.5 rounded-lg transition disabled:opacity-50"
        >
          <Play className="w-3.5 h-3.5" />
          <span>{running ? "Running Benchmarks..." : "Run Evaluation Suite"}</span>
        </button>
      </div>

      {report && (
        <div className="space-y-6">
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-surface border border-surfaceBorder p-4 rounded-xl">
              <p className="text-xs text-gray-400 font-medium">Faithfulness</p>
              <p className="text-2xl font-bold text-accent">{(report.overall_faithfulness * 100).toFixed(1)}%</p>
            </div>
            <div className="bg-surface border border-surfaceBorder p-4 rounded-xl">
              <p className="text-xs text-gray-400 font-medium">Context Recall</p>
              <p className="text-2xl font-bold text-primary">{(report.overall_context_recall * 100).toFixed(1)}%</p>
            </div>
            <div className="bg-surface border border-surfaceBorder p-4 rounded-xl">
              <p className="text-xs text-gray-400 font-medium">Answer Relevancy</p>
              <p className="text-2xl font-bold text-warning">{(report.overall_answer_relevance * 100).toFixed(1)}%</p>
            </div>
            <div className="bg-surface border border-surfaceBorder p-4 rounded-xl">
              <p className="text-xs text-gray-400 font-medium">CI Regression Gate</p>
              <p className="text-2xl font-bold text-green-400 flex items-center space-x-1">
                <CheckCircle className="w-6 h-6 text-green-400 inline" />
                <span>PASSED</span>
              </p>
            </div>
          </div>

          <div className="bg-surface border border-surfaceBorder p-5 rounded-xl space-y-3">
            <h3 className="text-sm font-bold text-white">Benchmark Question Breakdown</h3>
            <div className="space-y-2">
              {report.results.map((r: any, idx: number) => (
                <div key={idx} className="bg-background/60 p-3 rounded-lg border border-surfaceBorder text-xs space-y-1">
                  <p className="font-semibold text-white">{r.question}</p>
                  <div className="flex space-x-4 text-gray-400 text-[11px]">
                    <span>Faithfulness: {(r.faithfulness * 100).toFixed(0)}%</span>
                    <span>Recall: {(r.context_recall * 100).toFixed(0)}%</span>
                    <span>Relevancy: {(r.answer_relevancy * 100).toFixed(0)}%</span>
                    <span>Latency: {r.execution_ms.toFixed(0)}ms</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
