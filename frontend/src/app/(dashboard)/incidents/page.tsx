"use client";

import React, { useEffect, useState } from "react";
import { fetchIncidents, fetchIncidentRCA } from "@/lib/api";
import { AlertTriangle, Clock, Activity, ShieldAlert, CheckCircle2 } from "lucide-react";

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [rca, setRca] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchIncidents().then(setIncidents);
  }, []);

  const handleInvestigate = async (key: string) => {
    setLoading(true);
    try {
      const data = await fetchIncidentRCA(key);
      setRca(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <header className="border-b border-surfaceBorder pb-4">
        <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
          <AlertTriangle className="w-6 h-6 text-danger" />
          <span>Incident Investigation & RCA Room</span>
        </h2>
        <p className="text-sm text-gray-400">Automated multi-source timeline reconstruction and root-cause synthesis.</p>
      </header>

      {/* Incident List */}
      <div className="grid grid-cols-1 gap-4">
        {incidents.map((inc) => (
          <div key={inc.id} className="bg-surface border border-surfaceBorder p-5 rounded-xl flex items-center justify-between">
            <div className="space-y-1">
              <div className="flex items-center space-x-2">
                <span className="bg-danger/20 text-danger border border-danger/30 text-xs px-2 py-0.5 rounded font-bold">{inc.incident_key}</span>
                <span className="text-xs bg-red-950/40 text-red-400 px-2 py-0.5 rounded font-medium">{inc.severity}</span>
                <span className="text-xs text-gray-400">{inc.service}</span>
              </div>
              <h3 className="text-base font-semibold text-white">{inc.title}</h3>
              <p className="text-xs text-gray-400 flex items-center space-x-1">
                <Clock className="w-3.5 h-3.5" />
                <span>Detected: {inc.started_at}</span>
              </p>
            </div>
            <button
              onClick={() => handleInvestigate(inc.incident_key)}
              disabled={loading}
              className="bg-danger hover:bg-red-600 text-white text-xs font-semibold px-4 py-2 rounded-lg transition disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Trigger AI RCA"}
            </button>
          </div>
        ))}
      </div>

      {/* RCA Report */}
      {rca && (
        <div className="bg-surface border border-danger/40 p-6 rounded-xl space-y-6">
          <div className="flex items-center justify-between border-b border-surfaceBorder pb-3">
            <div className="flex items-center space-x-2">
              <ShieldAlert className="w-5 h-5 text-danger" />
              <h3 className="font-bold text-white text-lg">Automated RCA: {rca.incident_key}</h3>
            </div>
            <span className="text-xs font-bold text-accent bg-accent/20 px-3 py-1 rounded-full border border-accent/30">
              Confidence: {(rca.confidence * 100).toFixed(0)}%
            </span>
          </div>

          <div className="space-y-2">
            <h4 className="text-xs font-bold text-gray-400 uppercase">Probable Root Cause</h4>
            <p className="text-sm text-gray-200 bg-background/60 p-3 rounded-lg border border-surfaceBorder leading-relaxed">
              {rca.probable_root_cause}
            </p>
          </div>

          {/* Timeline */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-gray-400 uppercase">Event Timeline</h4>
            <div className="space-y-2 border-l-2 border-primary/40 pl-4 ml-2">
              {rca.timeline.map((item: any, i: number) => (
                <div key={i} className="text-xs space-y-0.5 relative">
                  <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-primary" />
                  <span className="font-mono text-primary font-bold">{item.time}</span>
                  <p className="text-gray-200">{item.event}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Remediation */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-accent uppercase flex items-center space-x-1">
              <CheckCircle2 className="w-4 h-4 text-accent" />
              <span>Recommended Remediation Runbook</span>
            </h4>
            <ul className="space-y-1.5 text-xs text-gray-300">
              {rca.recommended_remediation.map((step: string, idx: number) => (
                <li key={idx} className="flex items-start space-x-2 bg-background/40 p-2 rounded">
                  <span className="font-bold text-accent">{idx + 1}.</span>
                  <span>{step}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
