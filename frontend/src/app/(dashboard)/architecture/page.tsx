"use client";

import React from "react";
import { Network, Server, Database, ArrowRight } from "lucide-react";

export default function ArchitecturePage() {
  const services = [
    { name: "api-gateway", tier: "Gateway", language: "Go", callers: ["Client"], deps: ["auth-service", "order-service"] },
    { name: "auth-service", tier: "Security", language: "TypeScript", callers: ["api-gateway"], deps: ["users_db", "Redis"] },
    { name: "order-service", tier: "Commerce", language: "Python", callers: ["api-gateway"], deps: ["payment-service", "orders_db"] },
    { name: "payment-service", tier: "Billing", language: "Python", callers: ["order-service"], deps: ["payments_db", "Stripe API"] },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <header className="border-b border-surfaceBorder pb-4">
        <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Network className="w-6 h-6 text-warning" />
          <span>Microservice Architecture Topology</span>
        </h2>
        <p className="text-sm text-gray-400">GraphRAG entity-relationship dependency map for NovaStack.</p>
      </header>

      <div className="grid grid-cols-2 gap-4">
        {services.map((svc) => (
          <div key={svc.name} className="bg-surface border border-surfaceBorder p-5 rounded-xl space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Server className="w-4 h-4 text-primary" />
                <h3 className="font-bold text-white text-base">{svc.name}</h3>
              </div>
              <span className="text-[11px] font-mono bg-surfaceBorder px-2 py-0.5 rounded text-gray-300">{svc.language}</span>
            </div>
            <div className="text-xs space-y-1 text-gray-300">
              <p><span className="text-gray-400">Upstream: </span>{svc.callers.join(", ")}</p>
              <p><span className="text-gray-400">Dependencies: </span>{svc.deps.join(", ")}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
