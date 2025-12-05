# Project Overview

**DocGuard AI** is an automated system for analyzing contracts and business documents.  
It combines PDF preprocessing, OCR, and multi-step LLM reasoning to identify risks, ambiguous clauses, hidden obligations, and potential legal or financial issues.

DocGuard is designed for individuals, freelancers, and small to medium businesses that need a fast and accessible way to understand documents without legal expertise.  
The system performs structural parsing, extracts relevant sections, evaluates potential risks, and produces structured JSON or Markdown reports.

The architecture follows an open-core model.  
The public repository includes the API layer, preprocessing utilities, and a basic example pipeline.  
The core analysis engine (multi-step LLM workflow, heuristics, risk scoring, prompt templates, and interpretation rules) remains private and is used only in production.

The initial scope focuses on contract analysis (service agreements, NDAs, employment contracts, lease agreements, etc.).  
Future versions may extend to financial, operational, and corporate documents.

The MVP target is to demonstrate the complete processing flow:  
document upload → preprocessing → OCR → basic analysis → structured output.

---

# Objectives

- Provide a reliable automated tool for analyzing legal documents  
- Detect ambiguous, high-risk, or hidden clauses  
- Deliver consistent, structured results regardless of document formatting  
- Offer a clear API suitable for integration with external applications  
- Establish a foundation for future commercial development  

---

# Blockchain Integration

Blockchain functionality is optional and designed for EVM-compatible networks.  
On-chain request accounting and pay-per-use billing can be implemented in any low-fee environment, including Polygon, Arbitrum, BNB Chain, and others.

The choice of an initial network for deployment will depend on technical compatibility and partner ecosystem preferences.  
The architecture is not tied to a single chain and allows future multi-network expansion.

---

# Roadmap

## Phase 1 - MVP (1–2 weeks)

- Define architecture and project structure  
- Implement basic PDF preprocessing  
- Integrate OCR for scanned documents  
- Add minimal single-step LLM analysis (demo logic)  
- Provide a public `/analyze` API endpoint  
- Include example inputs and outputs  
- Write initial documentation  

**Deliverable:** functional demo showing end-to-end document processing.

---

## Phase 2 - Core Analysis Engine (2–4 weeks)

- Implement document segmentation  
- Add multi-step LLM analysis  
- Introduce basic heuristics for risk detection  
- Add the first version of a risk scoring model  
- Create prompt templates and configuration logic  
- Implement a simple sequential orchestrator for step-by-step analysis  

**Deliverable:** the first internal version of the private risk analysis engine.

---

## Phase 3 - Deployment and Infrastructure

- Deploy public demo API  
- Set up CI/CD  
- Add GPU inference backend if needed  
- Provide a simple public demo page  

**Deliverable:** publicly accessible demonstration of the system.

---

## Phase 4 - Blockchain Module

- On-chain accounting of requests  
- Pay-per-use billing  
- Signature-based authentication  
- Deployment to an EVM-compatible network  

---

# Long-Term Development

- Improved robustness for documents with complex layouts  
- Extended heuristics and refined risk scoring  
- Support for multiple LLM providers  
- Document version comparison (redline)  
- Advanced reporting templates  
- **Prototype of a visual interface for uploading documents and viewing results**  
  (UI technology not predetermined)  
- Multi-language support  
- Domain-specific model fine-tuning  
- Commercial SaaS offering  
- Integrations with corporate document workflow systems  

