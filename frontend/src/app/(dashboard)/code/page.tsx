"use client";

import React, { useState } from "react";
import { Code2, FileCode, Folder, GitBranch, Search } from "lucide-react";

export default function CodeExplorerPage() {
  const [selectedFile, setSelectedFile] = useState("app/services/payment_processor.py");

  const mockCode = `import asyncio
import logging
from app.db.session import AsyncSession
from app.models.payment import Payment

logger = logging.getLogger("payment-service")

class PaymentProcessor:
    """Processes customer payment authorizations and Stripe webhooks."""
    
    def __init__(self, db: AsyncSession, stripe_client):
        self.db = db
        self.stripe = stripe_client

    async def execute_charge(self, order_id: str, amount_cents: int, customer_id: str) -> bool:
        logger.info(f"Initiating charge for order {order_id}")
        charge = await self.stripe.charges.create(
            amount=amount_cents,
            currency="usd",
            customer=customer_id
        )
        return charge.status == "succeeded"
`;

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <header className="border-b border-surfaceBorder pb-4">
        <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Code2 className="w-6 h-6 text-accent" />
          <span>Code Intelligence & AST Explorer</span>
        </h2>
        <p className="text-sm text-gray-400">Browse AST symbol trees, call graphs, and indexed repository files.</p>
      </header>

      <div className="grid grid-cols-3 gap-4 h-[600px]">
        {/* File tree */}
        <div className="bg-surface border border-surfaceBorder rounded-xl p-4 space-y-3">
          <div className="flex items-center space-x-2 text-xs font-bold text-gray-400 uppercase">
            <Folder className="w-4 h-4 text-primary" />
            <span>payment-service (Branch: main)</span>
          </div>
          <div className="space-y-1">
            {[
              "app/main.py",
              "app/services/payment_processor.py",
              "app/models/payment.py",
              "alembic/versions/042_add_stripe_id.sql",
              "tests/unit/test_payments.py"
            ].map((f) => (
              <button
                key={f}
                onClick={() => setSelectedFile(f)}
                className={`w-full text-left flex items-center space-x-2 px-3 py-2 rounded-lg text-xs transition ${
                  selectedFile === f ? "bg-primary text-white font-medium" : "text-gray-300 hover:bg-surfaceBorder/50"
                }`}
              >
                <FileCode className="w-3.5 h-3.5" />
                <span className="truncate">{f}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Code viewer */}
        <div className="col-span-2 bg-surface border border-surfaceBorder rounded-xl p-4 flex flex-col">
          <div className="flex items-center justify-between border-b border-surfaceBorder pb-2 mb-3">
            <span className="text-xs font-mono text-gray-300">{selectedFile}</span>
            <span className="text-xs text-accent font-medium">AST Parsed</span>
          </div>
          <pre className="flex-1 bg-background/80 p-4 rounded-lg font-mono text-xs text-gray-200 overflow-auto">
            {mockCode}
          </pre>
        </div>
      </div>
    </div>
  );
}
