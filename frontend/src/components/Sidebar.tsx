import React from "react";
import Link from "next/link";
import { Shield, MessageSquare, AlertTriangle, Code2, Network, Activity, BarChart2 } from "lucide-react";

export function Sidebar() {
  return (
    <aside className="w-64 bg-surface border-r border-surfaceBorder h-screen flex flex-col p-4">
      <div className="flex items-center space-x-3 mb-8 px-2">
        <div className="bg-primary/20 p-2 rounded-lg text-primary border border-primary/30">
          <Shield className="w-6 h-6" />
        </div>
        <div>
          <h1 className="font-bold text-lg text-white">AegisAI</h1>
          <p className="text-xs text-gray-400">Enterprise AI Copilot</p>
        </div>
      </div>

      <nav className="flex-1 space-y-1">
        <Link href="/chat" className="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm text-gray-300 hover:bg-surfaceBorder/60 hover:text-white transition">
          <MessageSquare className="w-4 h-4 text-primary" />
          <span>AI Copilot Chat</span>
        </Link>
        <Link href="/incidents" className="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm text-gray-300 hover:bg-surfaceBorder/60 hover:text-white transition">
          <AlertTriangle className="w-4 h-4 text-danger" />
          <span>Incident RCA</span>
        </Link>
        <Link href="/code" className="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm text-gray-300 hover:bg-surfaceBorder/60 hover:text-white transition">
          <Code2 className="w-4 h-4 text-accent" />
          <span>Code Explorer</span>
        </Link>
        <Link href="/architecture" className="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm text-gray-300 hover:bg-surfaceBorder/60 hover:text-white transition">
          <Network className="w-4 h-4 text-warning" />
          <span>Architecture Graph</span>
        </Link>
        <Link href="/evaluations" className="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm text-gray-300 hover:bg-surfaceBorder/60 hover:text-white transition">
          <BarChart2 className="w-4 h-4 text-purple-400" />
          <span>RAG Quality & Eval</span>
        </Link>
      </nav>

      <div className="p-3 bg-surfaceBorder/30 rounded-lg border border-surfaceBorder/50 text-xs text-gray-400">
        <div className="flex items-center space-x-2 text-accent mb-1 font-medium">
          <Activity className="w-3.5 h-3.5" />
          <span>NovaStack Enterprise</span>
        </div>
        <p>Tenant: NovaStack Corp (100k+ LOC)</p>
      </div>
    </aside>
  );
}
