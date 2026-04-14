# Financial Services Industry (FSI) Tutorial

This tutorial walks you through building a complete FSI data pipeline using the **Databricks workspace UI** and **Genie Code**.

> **Before you begin:** Make sure you've completed all steps in the [Prerequisites](README.md#1-prerequisites) section of the main README and have the FSI CSV files downloaded to your local machine.

> **Important:** Throughout the exercises, replace `<your_username>` with your actual username (e.g., `user01`). Replace `<your_catalog>` with the catalog name assigned to you in the workspace.

---

## Exercise 1: Create Your Schema

*Tool: Workspace UI*

In this exercise, you'll create a schema to hold all the tables for your FSI pipeline.

### Steps

1. In the left sidebar, click **Catalog**
2. Browse the catalog explorer to find your catalog (`<your_catalog>`)
   - If you need to create your own catalog: click the **+** button at the top of the catalog explorer, select **Create catalog**, name it `<your_username>_catalog`, and click **Create**
3. Click on your catalog to expand it
4. Click the **+** button next to the catalog name (or the kebab menu **...** > **Create schema**)
5. Enter the schema name: `<your_username>_demo`
6. Click **Create**

<!-- Screenshot: Catalog explorer showing the new schema -->

### Validate

- In the catalog explorer, expand your catalog
- Confirm `<your_username>_demo` appears under the catalog

---

## Exercise 2: Create a Landing Volume

*Tool: Workspace UI*

Create a Unity Catalog Volume to store the raw CSV files that you'll upload.

### Steps

1. In the catalog explorer, navigate to `<your_catalog>` > `<your_username>_demo`
2. Click on the schema name to open it
3. Click the **Create** button, then select **Volume**
4. Set the volume name to `landing`
5. Leave the volume type as **Managed**
6. Click **Create**

<!-- Screenshot: Volume creation dialog -->

### Validate

- In the catalog explorer, navigate to `<your_catalog>` > `<your_username>_demo`
- Click on **Volumes** tab
- Confirm the `landing` volume appears

---

## Exercise 3: Upload Data to Volume

*Tool: Workspace UI (Drag & Drop)*

Upload the FSI sample data to your landing volume using the workspace file browser.

### Steps

1. In the catalog explorer, navigate to `<your_catalog>` > `<your_username>_demo` > **Volumes** > `landing`
2. Click on the `landing` volume to open it
3. For each data source, create a subdirectory and upload the corresponding CSV file:

   | Subdirectory | File to Upload |
   |-------------|---------------|
   | `banking_customers` | `banking_customers.csv` |
   | `banking_accounts` | `banking_accounts.csv` |
   | `banking_transactions` | `banking_transactions.csv` |
   | `banking_branches` | `banking_branches.csv` |
   | `insurance_customers` | `insurance_customers.csv` |
   | `insurance_policies` | `insurance_policies.csv` |
   | `insurance_claims` | `insurance_claims.csv` |

4. To create each subdirectory and upload:
   - Click **Create** > **Folder**, enter the folder name (e.g., `banking_customers`), click **Create**
   - Open the folder, then click **Upload** (or drag & drop the CSV file into the folder)
   - Repeat for each data source

<!-- Screenshot: Volume browser showing uploaded files -->

### Validate

- Browse the `landing` volume in the catalog explorer
- Confirm all 7 subdirectories exist, each containing its CSV file
- Click on any CSV file to preview the data

---

## Exercise 4: Create the Bronze Layer

*Tool: Genie Code in Notebook*

Now we switch to the Genie Code to generate the pipeline code. You'll create a notebook and use the Assistant to write the bronze layer — raw ingestion from the landing volume into streaming tables.

### Steps

1. Click **+ New** > **Notebook** in the sidebar
2. Name the notebook `01_bronze`
3. Set the default language to **SQL**
4. Open the **Genie Code** (click the sparkle icon in the toolbar or press `Cmd+I` / `Ctrl+I`)
5. Paste the following prompt into the Assistant:

> **Genie Code Prompt:**
>
> ```
> Create DLT (Delta Live Tables) SQL statements to ingest raw CSV data from
> /Volumes/<your_catalog>/<your_username>_demo/landing/ into bronze streaming tables.
>
> Create one streaming table per CSV source with these table names:
> - 01_banking_customers (from landing/banking_customers/)
> - 01_banking_accounts (from landing/banking_accounts/)
> - 01_banking_transactions (from landing/banking_transactions/)
> - 01_banking_branches (from landing/banking_branches/)
> - 01_insurance_customers (from landing/insurance_customers/)
> - 01_insurance_policies (from landing/insurance_policies/)
> - 01_insurance_claims (from landing/insurance_claims/)
>
> Use Auto Loader (cloud_files) to read CSV files from the volumes.
> Set header to true and infer the schema.
> Each table should be a CREATE OR REFRESH STREAMING TABLE statement.
> ```

6. Review the generated SQL code
7. Accept the code into your notebook cells (one `CREATE OR REFRESH STREAMING TABLE` per cell)

<!-- Screenshot: Genie Code generating bronze SQL -->

### Validate

- Review the notebook — you should see 7 streaming table definitions
- Each one should use `cloud_files` with the correct volume path
- Confirm the table names all start with `01_`

> **Don't run the notebook yet** — we'll create the pipeline and run everything together in Exercise 7.

---

## Exercise 5: Create the Silver Layer

*Tool: Genie Code in Notebook*

Create a second notebook for the silver layer — cleaned and validated data with quality constraints.

### Steps

1. Click **+ New** > **Notebook** in the sidebar
2. Name the notebook `02_silver`
3. Set the default language to **SQL**
4. Open the **Genie Code** and paste this prompt:

> **Genie Code Prompt:**
>
> ```
> Create DLT SQL statements to clean and transform bronze tables into silver
> streaming tables. Read from the bronze tables created in the 01_bronze notebook.
>
> Create these silver streaming tables:
> - 02_banking_customers (from 01_banking_customers)
> - 02_banking_accounts (from 01_banking_accounts)
> - 02_banking_transactions (from 01_banking_transactions)
> - 02_banking_branches (from 01_banking_branches)
> - 02_insurance_customers (from 01_insurance_customers)
> - 02_insurance_policies (from 01_insurance_policies)
> - 02_insurance_claims (from 01_insurance_claims)
>
> For each table:
> - Use CREATE OR REFRESH STREAMING TABLE with a SELECT from STREAM(LIVE.01_xxx)
> - Add CONSTRAINT clauses for data quality (NOT NULL on primary key columns,
>   valid ranges where applicable — e.g., positive amounts, valid dates)
> - TRIM string columns and standardize data types
> - Handle nulls with COALESCE where appropriate
> - Add a COMMENT describing the table purpose
> ```

5. Review the generated SQL — check that constraints make sense for the data
6. Accept the code into your notebook

<!-- Screenshot: Silver layer notebook with quality constraints -->

### Validate

- Review the notebook — you should see 7 silver streaming table definitions
- Each should reference `STREAM(LIVE.01_xxx)` as the source
- Verify that CONSTRAINT clauses are present for key columns

---

## Exercise 6: Create the Gold Layer

*Tool: Genie Code in Notebook*

Create the business-level aggregations as gold materialized views. We'll build **one table at a time** so you can review each one.

### Steps

1. Click **+ New** > **Notebook** in the sidebar
2. Name the notebook `03_gold`
3. Set the default language to **SQL**

Now use the Genie Code for each gold table, one at a time:

---

**Gold Table 1 — Customer 360**

Open the Assistant and paste:

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_customer_360.
> This view should create a unified customer profile by joining
> LIVE.02_banking_customers and LIVE.02_insurance_customers on customer
> identifiers, enriched with account counts from LIVE.02_banking_accounts
> and policy counts from LIVE.02_insurance_policies.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept the code.

---

**Gold Table 2 — Policy Claims Summary**

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_policy_claims_summary.
> This view should aggregate claims by policy type, showing total claims,
> approved vs denied counts, average claim amount, and total settlement
> amounts from LIVE.02_insurance_claims joined with LIVE.02_insurance_policies.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept.

---

**Gold Table 3 — Transaction Daily Summary**

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_transaction_daily_summary.
> This view should aggregate daily transaction volumes and amounts by
> transaction type and channel from LIVE.02_banking_transactions.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept.

---

**Gold Table 4 — Branch Performance**

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_branch_performance.
> This view should show branch-level metrics including total accounts,
> total balances, transaction counts, and active customer counts by joining
> LIVE.02_banking_branches, LIVE.02_banking_accounts, and
> LIVE.02_banking_transactions.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept.

---

**Gold Table 5 — Customer Risk Profile**

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_customer_risk_profile.
> This view should combine banking risk ratings with insurance claim history
> to create a unified risk score per customer, using LIVE.02_banking_customers,
> LIVE.02_banking_accounts, LIVE.02_insurance_customers, and
> LIVE.02_insurance_claims.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept.

<!-- Screenshot: Gold notebook with all 5 materialized views -->

### Validate

- Review the `03_gold` notebook — confirm all 5 materialized views look correct
- Each should use `CREATE OR REFRESH MATERIALIZED VIEW`
- Verify the join logic and aggregations make business sense

---

## Exercise 7: Create and Run the Pipeline

*Tool: Workspace UI*

Now bring it all together — create a DLT pipeline that references your three notebooks and run it.

### Steps

1. In the left sidebar, click **Pipelines** (under **Data Engineering**)
2. Click **Create pipeline**
3. Configure the pipeline:
   - **Pipeline name:** `<your_username>_ingestion`
   - **Pipeline mode:** Triggered
   - **Source code:** Add all three notebooks — `01_bronze`, `02_silver`, `03_gold`
     - Click **Add source code** and navigate to each notebook
   - **Destination:**
     - **Catalog:** `<your_catalog>`
     - **Target schema:** `<your_username>_demo`
4. Click **Create**
5. Click **Start** to run the pipeline

<!-- Screenshot: Pipeline creation dialog with all three notebooks -->

### Monitor

- Watch the DAG visualization as data flows through bronze > silver > gold
- The pipeline will show each streaming table and materialized view as a node
- Green nodes = successful, red = failed

**If the pipeline fails**, click on the failed node to see the error details. Common fixes:
- Volume path typos — double-check the paths in `01_bronze`
- Column name mismatches — verify column names match between bronze/silver/gold
- Use the Genie Code in the failed notebook to help troubleshoot: paste the error message and ask for a fix

### Validate

1. Go to **Catalog** > `<your_catalog>` > `<your_username>_demo`
2. Verify that tables exist with the `01_`, `02_`, and `03_` prefixes
3. Click on a few tables and preview the data to confirm it loaded correctly

---

## Exercise 8: Create Genie Spaces

*Tool: Workspace UI*

Make the gold-layer data accessible to business users through **Genie Spaces** — natural language query interfaces.

### Genie Space 1 — Customer Analytics

1. In the left sidebar, click **Genie**
2. Click **New Genie space**
3. Configure the space:
   - **Name:** `<your_username> - Customer Analytics`
   - **Description:**
     > This space answers business questions about FSI customers, including
     > unified customer profiles across banking and insurance, risk profiles,
     > and policy-claim relationships.
   - **Warehouse:** Select the SQL warehouse available in your workspace
   - **Tables:** Add the following gold tables from `<your_catalog>.<your_username>_demo`:
     - `03_customer_360`
     - `03_customer_risk_profile`
     - `03_policy_claims_summary`
4. Click **Save**

### Genie Space 2 — Operations Analytics

1. Click **New Genie space** again
2. Configure the space:
   - **Name:** `<your_username> - Operations Analytics`
   - **Description:**
     > This space answers business questions about FSI operations, including
     > daily transaction volumes, branch performance metrics, and operational trends.
   - **Warehouse:** Select the same SQL warehouse
   - **Tables:** Add:
     - `03_transaction_daily_summary`
     - `03_branch_performance`
3. Click **Save**

<!-- Screenshot: Genie space creation with tables selected -->

### Test Your Genie Spaces

Try asking natural language questions in each space:

**Customer Analytics:**
- "Who are the top 10 customers by total account balance?"
- "What is the claim approval rate by policy type?"
- "Which customers have the highest risk scores?"

**Operations Analytics:**
- "What is the total transaction volume by channel this month?"
- "Which branches have the most active customers?"
- "Show me daily transaction trends over the past week"

### Validate

- Both Genie spaces appear in the **Genie** section of the sidebar
- Each space can answer questions about its assigned tables
- The SQL warehouse processes queries successfully

---

## Exercise 9: Create a Dashboard

*Tool: Workspace UI + Genie Code*

Create a dashboard to visualize insights from the gold-layer data. You'll use the workspace UI to create the dashboard, the **Genie Code** (Genie prompt within the dashboard editor) to generate dataset queries, and then build visualizations.

### Step 1: Create the Dashboard

1. In the left sidebar, click **Dashboards**
2. Click **Create dashboard**
3. Name it: `<your_username> - FSI Insights Dashboard`

### Step 2: Add Datasets (Using Genie Prompt)

In the dashboard editor, you'll add 3 datasets. Use the **Genie prompt** (the AI assistant within the dashboard canvas) to help generate each query.

**Dataset 1 — Customer Overview:**

Click **Add a dataset** (or use the data panel), then use the Genie prompt:

> **Genie Prompt:**
>
> ```
> Write a SQL query against <your_catalog>.<your_username>_demo.03_customer_360
> that summarizes total customers, average account balance, and customer
> distribution by segment. Include counts and averages grouped by segment.
> ```

Review the generated SQL, adjust if needed, and save the dataset.

**Dataset 2 — Claims Analysis:**

Add another dataset, use the Genie prompt:

> **Genie Prompt:**
>
> ```
> Write a SQL query against <your_catalog>.<your_username>_demo.03_policy_claims_summary
> that shows total claims, approved vs denied counts, average claim amount,
> and total settlement amount grouped by policy type.
> ```

Review and save.

**Dataset 3 — Branch Performance:**

Add a third dataset, use the Genie prompt:

> **Genie Prompt:**
>
> ```
> Write a SQL query against <your_catalog>.<your_username>_demo.03_branch_performance
> that shows branch name, total accounts, total balances, transaction counts,
> and active customer counts, ordered by total balances descending.
> ```

Review and save.

### Step 3: Build Visualizations (Using Genie Prompt)

Now use the Genie prompt on the dashboard canvas to create visualizations from your datasets.

> **Genie Prompt:**
>
> ```
> Using the datasets I've added, create the following visualizations:
> 1. A counter/stat showing total number of customers from the Customer Overview dataset
> 2. A bar chart showing customer distribution by segment from the Customer Overview dataset
> 3. A bar chart showing approved vs denied claims by policy type from the Claims Analysis dataset
> 4. A table showing the top branches by total balance from the Branch Performance dataset
> ```

Arrange the visualizations on the canvas by dragging and resizing them.

### Step 4: Publish

1. Click **Publish** in the top-right corner of the dashboard editor
2. The dashboard is now accessible to other users in the workspace

<!-- Screenshot: Completed dashboard with visualizations -->

### Validate

1. In **Dashboards**, find your published dashboard
2. Open it and confirm:
   - The counter shows a customer total
   - The bar charts render with data
   - The table shows branch metrics
3. Try interacting with filters or clicking on chart elements

---

## Wrap-Up

Congratulations! You've completed the FSI tutorial! Here's what you accomplished:

| Step | What You Built | Tool Used |
|------|---------------|-----------|
| Exercise 1 | A Unity Catalog schema for your demo | Workspace UI |
| Exercise 2 | A managed volume for landing raw data | Workspace UI |
| Exercise 3 | Uploaded FSI sample data via drag & drop | Workspace UI |
| Exercise 4 | Bronze layer — raw ingestion with Auto Loader | Genie Code |
| Exercise 5 | Silver layer — data quality constraints | Genie Code |
| Exercise 6 | Gold layer — business aggregation views | Genie Code |
| Exercise 7 | Created and ran the end-to-end DLT pipeline | Workspace UI |
| Exercise 8 | Genie spaces for natural language analytics | Workspace UI |
| Exercise 9 | Dashboard with 3 datasets and visualizations | UI + Genie Code |

**What's Next?**
- Try modifying the gold-layer transformations or adding new aggregations using the Genie Code
- Ask questions in your Genie spaces and see how the AI interprets them
- Try the [Pharma tutorial](TUTORIAL_PHARMA.md) to build a second pipeline
