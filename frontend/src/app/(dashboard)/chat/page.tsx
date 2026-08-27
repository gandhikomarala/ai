"use client";

import React, { useState } from "react";
import { sendCopilotQuery, CopilotResponse } from "@/lib/api";
import { Send, Bot, User, Sparkles, BookOpen, Layers, CheckCircle2 } from "lucide-react";

export default function ChatPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<CopilotResponse | null>(null);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    setLoading(true);
    try {
      const data = await sendCopilotQuery(query);
      setResponse(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <header className="border-b border-surfaceBorder pb-4">
        <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Sparkles className="w-6 h-6 text-primary" />
          <span>AI Engineering Copilot</span>
        </h2>
        <p className="text-sm text-gray-400">Ask questions about architecture, code, incidents, or database queries.</p>
      </header>

      {/* Suggested prompts */}
      <div className="grid grid-cols-3 gap-3">
        {[
          "What is our authentication architecture?",
          "Why did INC-2841 happen in payment service?",
          "Show failed payments in database"
        ].map((prompt, i) => (
          <button
            key={i}
            onClick={() => setQuery(prompt)}
            className="text-left text-xs bg-surface border border-surfaceBorder/80 p-3 rounded-lg hover:border-primary/50 text-gray-300 hover:text-white transition"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Display */}
      {response && (
        <div className="space-y-4">
          {/* User query */}
          <div className="flex items-start space-x-3 bg-surface/50 border border-surfaceBorder/50 p-4 rounded-xl">
            <div className="bg-primary/20 p-2 rounded-lg text-primary"><User className="w-4 h-4" /></div>
            <div>
              <p className="text-xs text-gray-400 mb-1">User Query</p>
              <p className="text-sm font-medium text-white">{response.query}</p>
            </div>
          </div>

          {/* Agent reasoning steps */}
          {response.steps.length > 0 && (
            <div className="bg-surface/80 border border-surfaceBorder p-4 rounded-xl space-y-2">
              <div className="flex items-center space-x-2 text-xs font-semibold text-primary uppercase tracking-wide">
                <Layers className="w-4 h-4" />
                <span>Multi-Agent Reasoning Chain ({response.intent})</span>
              </div>
              <div className="space-y-2 pt-2">
                {response.steps.map((step, idx) => (
                  <div key={idx} className="text-xs flex items-start space-x-2 text-gray-300 bg-background/50 p-2 rounded border border-surfaceBorder/40">
                    <CheckCircle2 className="w-3.5 h-3.5 text-accent mt-0.5" />
                    <div>
                      <span className="font-semibold text-white">{step.agent_name}: </span>
                      <span>{step.thought}</span>
                      <p className="text-gray-400 text-[11px] mt-0.5">Observed: {step.observation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Copilot Final Answer */}
          <div className="flex items-start space-x-3 bg-surface border border-primary/30 p-5 rounded-xl">
            <div className="bg-primary p-2 rounded-lg text-white"><Bot className="w-5 h-5" /></div>
            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-primary">AegisAI Grounded Response</span>
                <span className="text-[11px] text-gray-400">{response.execution_time_ms.toFixed(0)}ms | Confidence: {(response.confidence*100).toFixed(0)}%</span>
              </div>
              <div className="text-sm text-gray-200 whitespace-pre-wrap leading-relaxed">
                {response.final_answer}
              </div>

              {/* Citations */}
              {response.citations.length > 0 && (
                <div className="mt-4 pt-3 border-t border-surfaceBorder/60">
                  <div className="flex items-center space-x-1.5 text-xs text-gray-400 font-semibold mb-2">
                    <BookOpen className="w-3.5 h-3.5 text-accent" />
                    <span>Verified Citations ({response.citations.length})</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    {response.citations.map((c, idx) => (
                      <div key={idx} className="bg-background/80 border border-surfaceBorder p-2.5 rounded text-xs">
                        <p className="font-semibold text-white truncate">[{c.index}] {c.title}</p>
                        <p className="text-gray-400 text-[11px] truncate">{c.file_path || c.section_title}</p>
                        <p className="text-gray-300 text-[11px] mt-1 line-clamp-2 italic">"{c.snippet}"</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Input bar */}
      <form onSubmit={handleSend} className="sticky bottom-0 bg-background/95 backdrop-blur pt-2">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask AegisAI anything about NovaStack architecture, code, or incidents..."
            className="w-full bg-surface border border-surfaceBorder rounded-xl pl-4 pr-12 py-3.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary transition"
          />
          <button
            type="submit"
            disabled={loading}
            className="absolute right-2.5 top-2.5 p-2 bg-primary hover:bg-primaryHover text-white rounded-lg transition disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
}
