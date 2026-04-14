# Vibe Data Engineering with Genie Code

Welcome to the **Vibe Data Engineering Workshop**! In this hands-on tutorial, you'll use the **Genie Code** — the AI coding assistant built right into your Databricks workspace — to build a complete data pipeline from raw CSV ingestion to curated gold-layer tables, Genie spaces, and dashboards.

> **What is Vibe Data Engineering?** It's the practice of using AI assistants to build and manage data pipelines through conversational prompts instead of writing every line of code manually. You describe *what* you want, and the AI helps you build it.

> **Why Genie Code?** Everything happens in your browser — no CLI installs, no API keys, no local tooling. You use the workspace UI for setup tasks (creating schemas, volumes, uploading data) and the Genie Code in notebooks to generate pipeline code. It's the fastest way to go from zero to a working pipeline.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Repository Overview](#2-repository-overview)
3. [Getting the Data](#3-getting-the-data)
4. [Enabling Genie Code](#4-enabling-databricks-assistant)
5. [Choose Your Tutorial](#5-choose-your-tutorial)

---

## 1. Prerequisites

Before you begin, make sure you have:
- Access to a **Databricks workspace** ([sign up for a free trial](https://www.databricks.com/try-databricks) if you don't have one)
- **Genie Code** enabled in your workspace (enabled by default on most workspaces)
- A modern web browser (Chrome, Firefox, Edge, or Safari)

That's it — no local installations required.

> If you don't have workspace access yet, contact your workshop facilitator before proceeding.

### Checklist

Before moving on, confirm:

- [ ] You can log in to your Databricks workspace
- [ ] You can see the **Catalog** section in the left sidebar
- [ ] You can create a new **Notebook** (click **+ New** in the sidebar)

---

## 2. Repository Overview

This workshop repository contains sample data for two industries:

```
data/
├── fsi/                          # Financial Services Industry
│   ├── banking_accounts/
│   │   └── banking_accounts.csv
│   ├── banking_branches/
│   │   └── banking_branches.csv
│   ├── banking_customers/
│   │   └── banking_customers.csv
│   ├── banking_transactions/
│   │   └── banking_transactions.csv
│   ├── insurance_claims/
│   │   └── insurance_claims.csv
│   ├── insurance_customers/
│   │   └── insurance_customers.csv
│   └── insurance_policies/
│       └── insurance_policies.csv
│
└── pharma/                       # Pharmaceutical Industry
    ├── distribution_cold_chains/
    │   └── distribution_cold_chains.csv
    ├── distribution_warehouses/
    │   └── distribution_warehouses.csv
    ├── manufacturing_batches/
    │   └── manufacturing_batches.csv
    ├── manufacturing_quality/
    │   └── manufacturing_quality.csv
    ├── retail_inventory/
    │   └── retail_inventory.csv
    ├── retail_outlets/
    │   └── retail_outlets.csv
    ├── retail_sales/
    │   └── retail_sales.csv
    ├── supply_materials/
    │   └── supply_materials.csv
    └── supply_suppliers/
        └── supply_suppliers.csv
```

Each CSV file contains between 150 and 10,000 realistic sample records. Pick an industry to work with for the rest of the workshop — **FSI** or **Pharma**.

---

## 3. Getting the Data

You'll need to download the CSV files to your local machine so you can upload them to Databricks via the workspace UI.

**Option A — Download the ZIP:**

Download the full repository as a ZIP from GitHub, then extract the `data/` folder to a location you can easily find.

**Option B — Clone the repo (if you have Git):**

```bash
git clone https://github.com/muharandy-db/dbxf_genie_de.git
```

Then navigate to the `data/fsi/` or `data/pharma/` folder depending on which tutorial you choose.

---

## 4. Enabling Genie Code

Genie Code is the AI coding assistant built into notebooks, the SQL editor, and other workspace surfaces. It should be enabled by default.

To verify:

1. Open your Databricks workspace
2. Click **+ New** > **Notebook** to create a new notebook
3. Look for the **Assistant** icon (sparkle/star icon) in the notebook toolbar or sidebar
4. If you see it, you're ready to go

> **Not seeing the Assistant?** Ask your workspace admin to enable it under **Settings** > **Workspace settings** > **Genie Code**.

---

## 5. Choose Your Tutorial

Pick an industry and follow the step-by-step tutorial. Each tutorial contains 9 exercises that guide you through building a complete data pipeline using the workspace UI and Genie Code.

| Tutorial | Description | Exercises |
|----------|-------------|-----------|
| [**FSI (Financial Services)**](TUTORIAL_FSI.md) | Banking customers, accounts, transactions, insurance policies, and claims | 9 exercises |
| [**Pharma (Pharmaceutical)**](TUTORIAL_PHARMA.md) | Manufacturing batches, quality control, cold chain distribution, retail sales, and supply chain | 9 exercises |

Both tutorials follow the same structure:

| Phase | Exercises | Tool |
|-------|-----------|------|
| **Setup** | 1. Create schema, 2. Create volume, 3. Upload data | Workspace UI |
| **Pipeline** | 4. Bronze layer, 5. Silver layer, 6. Gold layer | Genie Code |
| **Execution** | 7. Create & run the pipeline | Workspace UI |
| **Analytics** | 8. Create Genie spaces, 9. Create dashboards | Workspace UI + Genie Code |

---

> **Vibe Data Engineering with Genie Code** — everything in your browser, nothing to install.
>
> For questions or feedback, reach out to your workshop facilitator.
