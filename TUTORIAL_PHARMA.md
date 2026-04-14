# Pharmaceutical Industry (Pharma) Tutorial

This tutorial walks you through building a complete Pharma data pipeline using the **Databricks workspace UI** and **Genie Code**.

> **Before you begin:** Make sure you've completed all steps in the [Prerequisites](README.md#1-prerequisites) section of the main README and have the Pharma CSV files downloaded to your local machine.

> **Important:** Throughout the exercises, replace `<your_username>` with your actual username (e.g., `user01`). Replace `<your_catalog>` with the catalog name assigned to you in the workspace.

---

## Exercise 1: Create Your Schema

*Tool: Workspace UI*

In this exercise, you'll create a schema to hold all the tables for your Pharma pipeline.

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

Upload the Pharma sample data to your landing volume by dragging and dropping the folders directly.

### Steps

1. On your local machine, open the `data/pharma/` directory from the downloaded repository. You should see these 9 folders:
   - `manufacturing_batches/`
   - `manufacturing_quality/`
   - `distribution_cold_chains/`
   - `distribution_warehouses/`
   - `retail_outlets/`
   - `retail_inventory/`
   - `retail_sales/`
   - `supply_materials/`
   - `supply_suppliers/`
2. In the Databricks workspace, navigate to the catalog explorer: `<your_catalog>` > `<your_username>_demo` > **Volumes** > `landing`
3. Click on the `landing` volume to open it
4. Select **all 9 folders** from your local `data/pharma/` directory and **drag & drop them** into the landing volume browser

That's it — the workspace will upload all folders with their CSV files in one go.

<!-- Screenshot: Drag and drop folders into the landing volume -->

### Validate

- Browse the `landing` volume in the catalog explorer
- Confirm all 9 subdirectories exist, each containing its CSV file
- Click on any CSV file to preview the data

---

## Exercise 4: Create the Pipeline and Bronze Layer

*Tool: Workspace UI + Genie Code in Pipeline IDE*

Now we'll create a **Spark Declarative Pipeline** using the workspace UI, then use Genie Code inside the pipeline IDE to write the bronze layer — raw ingestion from the landing volume into streaming tables.

### Step 1: Create the Pipeline

1. In the left sidebar, click **New** > **ETL pipeline**
2. Configure the pipeline:
   - **Pipeline name:** `<your_username>_ingestion`
   - **Default catalog:** `<your_catalog>`
   - **Default schema:** `<your_username>_demo`
   - **Language:** SQL
   - **Start with:** an empty file
3. Click **Create**

<!-- Screenshot: ETL pipeline creation dialog -->

The **pipeline IDE** will open with an empty SQL source file ready for your first transformation.

### Step 2: Write the Bronze Layer with Genie Code

1. In the pipeline IDE, you should see an empty source file (e.g., `pipeline_file_1.sql`). Rename it to `01_bronze.sql`
2. Open **Genie Code** (click the sparkle icon in the toolbar or press `Cmd+I` / `Ctrl+I`)
3. Paste the following prompt:

> **Genie Code Prompt:**
>
> ```
> Create DLT (Delta Live Tables) SQL statements to ingest raw CSV data from
> /Volumes/<your_catalog>/<your_username>_demo/landing/ into bronze streaming tables.
>
> Create one streaming table per CSV source with these table names:
> - 01_manufacturing_batches (from landing/manufacturing_batches/)
> - 01_manufacturing_quality (from landing/manufacturing_quality/)
> - 01_distribution_cold_chains (from landing/distribution_cold_chains/)
> - 01_distribution_warehouses (from landing/distribution_warehouses/)
> - 01_retail_outlets (from landing/retail_outlets/)
> - 01_retail_inventory (from landing/retail_inventory/)
> - 01_retail_sales (from landing/retail_sales/)
> - 01_supply_materials (from landing/supply_materials/)
> - 01_supply_suppliers (from landing/supply_suppliers/)
>
> Use Auto Loader (cloud_files) to read CSV files from the volumes.
> Set header to true and infer the schema.
> Each table should be a CREATE OR REFRESH STREAMING TABLE statement.
> ```

4. Review the generated SQL code
5. Accept the code into your source file

<!-- Screenshot: Genie Code generating bronze SQL in the pipeline IDE -->

### Validate

- Review the source file — you should see 9 streaming table definitions
- Each one should use `cloud_files` with the correct volume path
- Confirm the table names all start with `01_`
- The pipeline DAG sidebar should show the 9 bronze tables

---

## Exercise 5: Add the Silver Layer

*Tool: Genie Code in Pipeline IDE*

Add a new source file to the pipeline for the silver layer — cleaned and validated data with quality constraints.

### Steps

1. In the pipeline IDE, click **Add source file** (or the **+** button) to create a new SQL file
2. Name the file `02_silver.sql`
3. Open **Genie Code** and paste this prompt:

> **Genie Code Prompt:**
>
> ```
> Create DLT SQL statements to clean and transform bronze tables into silver
> streaming tables. Read from the bronze tables created in the 01_bronze file.
>
> Create these silver streaming tables:
> - 02_manufacturing_batches (from 01_manufacturing_batches)
> - 02_manufacturing_quality (from 01_manufacturing_quality)
> - 02_distribution_cold_chains (from 01_distribution_cold_chains)
> - 02_distribution_warehouses (from 01_distribution_warehouses)
> - 02_retail_outlets (from 01_retail_outlets)
> - 02_retail_inventory (from 01_retail_inventory)
> - 02_retail_sales (from 01_retail_sales)
> - 02_supply_materials (from 01_supply_materials)
> - 02_supply_suppliers (from 01_supply_suppliers)
>
> For each table:
> - Use CREATE OR REFRESH STREAMING TABLE with a SELECT from STREAM(LIVE.01_xxx)
> - Add CONSTRAINT clauses for data quality:
>   - NOT NULL on primary key columns
>   - Valid ranges (e.g., positive quantities, valid dates)
>   - Temperature bounds for cold chain data (e.g., between -80 and 25 Celsius)
>   - Quality test results should be valid enum values
> - TRIM string columns and standardize data types
> - Handle nulls with COALESCE where appropriate
> - Add a COMMENT describing the table purpose
> ```

4. Review the generated SQL — check that constraints make sense for the data
5. Accept the code into your source file

<!-- Screenshot: Silver layer source file with quality constraints -->

### Validate

- Review `02_silver.sql` — you should see 9 silver streaming table definitions
- Each should reference `STREAM(LIVE.01_xxx)` as the source
- Verify that CONSTRAINT clauses are present, especially temperature bounds for cold chain data
- The pipeline DAG sidebar should now show both bronze and silver tables

---

## Exercise 6: Add the Gold Layer

*Tool: Genie Code in Pipeline IDE*

Add a new source file for the business-level aggregations as gold materialized views. We'll build **one table at a time** so you can review each one.

### Steps

1. In the pipeline IDE, click **Add source file** (or the **+** button) to create a new SQL file
2. Name the file `03_gold.sql`

Now use Genie Code for each gold table, one at a time:

---

**Gold Table 1 — Batch Quality Summary**

Open Genie Code and paste:

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_batch_quality_summary.
> This view should aggregate quality test pass/fail rates by product and
> facility from LIVE.02_manufacturing_quality and LIVE.02_manufacturing_batches.
> Include total tests, pass count, fail count, and pass rate percentage.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept the code.

---

**Gold Table 2 — Cold Chain Compliance**

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_cold_chain_compliance.
> This view should calculate temperature compliance rates by route and carrier,
> flagging shipments that exceeded temperature thresholds from
> LIVE.02_distribution_cold_chains. Include total shipments, compliant count,
> non-compliant count, and compliance rate percentage.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept.

---

**Gold Table 3 — Inventory Status**

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_inventory_status.
> This view should show current inventory levels with expiry risk by outlet
> and product, joining LIVE.02_retail_inventory with LIVE.02_retail_outlets.
> Flag items nearing expiry (within 30 days) and include quantity on hand.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept.

---

**Gold Table 4 — Sales by Outlet**

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_sales_by_outlet.
> This view should aggregate sales by outlet, product, and month from
> LIVE.02_retail_sales joined with LIVE.02_retail_outlets.
> Include total quantity sold, total revenue, and average price per unit.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept.

---

**Gold Table 5 — Supply Chain Overview**

> **Genie Code Prompt:**
>
> ```
> Create a DLT materialized view called 03_supply_chain_overview.
> This view should provide end-to-end supply chain metrics from supplier to
> retail, joining LIVE.02_supply_suppliers, LIVE.02_supply_materials,
> LIVE.02_manufacturing_batches, LIVE.02_distribution_cold_chains, and
> LIVE.02_retail_inventory. Show supplier reliability, material lead times,
> and inventory coverage.
> Use CREATE OR REFRESH MATERIALIZED VIEW syntax.
> ```

Review and accept.

<!-- Screenshot: Gold source file with all 5 materialized views -->

### Validate

- Review `03_gold.sql` — confirm all 5 materialized views look correct
- Each should use `CREATE OR REFRESH MATERIALIZED VIEW`
- Verify the join logic and aggregations make business sense
- The pipeline DAG sidebar should now show the full lineage: bronze > silver > gold

---

## Exercise 7: Run the Pipeline

*Tool: Workspace UI*

Your pipeline already has all three source files. Now it's time to run it.

### Steps

1. In the pipeline IDE, click **Start** to run the pipeline
2. If you've navigated away, go to **Pipelines** in the left sidebar (under **Data Engineering**), find `<your_username>_ingestion`, and click **Start**

<!-- Screenshot: Pipeline running with DAG visualization -->

### Monitor

- Watch the DAG visualization as data flows through bronze > silver > gold
- The pipeline will show each streaming table and materialized view as a node
- Green nodes = successful, red = failed

**If the pipeline fails**, click on the failed node to see the error details. Common fixes:
- Volume path typos — double-check the paths in `01_bronze.sql`
- Column name mismatches — verify column names match between bronze/silver/gold
- Temperature constraint issues in cold chain data — adjust bounds if needed
- Use Genie Code in the pipeline IDE to help troubleshoot: paste the error message and ask for a fix

### Validate

1. Go to **Catalog** > `<your_catalog>` > `<your_username>_demo`
2. Verify that tables exist with the `01_`, `02_`, and `03_` prefixes
3. Click on a few tables and preview the data to confirm it loaded correctly

---

## Exercise 8: Create Genie Spaces

*Tool: Workspace UI*

Make the gold-layer data accessible to business users through **Genie Spaces** — natural language query interfaces.

### Genie Space 1 — Pharma Quality Analytics

1. In the left sidebar, click **Genie**
2. Click **New Genie space**
3. Configure the space:
   - **Name:** `<your_username> - Pharma Quality Analytics`
   - **Description:**
     > This space answers business questions about pharmaceutical quality and
     > compliance, including manufacturing batch quality pass/fail rates,
     > cold chain temperature compliance by route and carrier, and quality trends.
   - **Warehouse:** Select the SQL warehouse available in your workspace
   - **Tables:** Add the following gold tables from `<your_catalog>.<your_username>_demo`:
     - `03_batch_quality_summary`
     - `03_cold_chain_compliance`
4. Click **Save**

### Genie Space 2 — Pharma Operations Analytics

1. Click **New Genie space** again
2. Configure the space:
   - **Name:** `<your_username> - Pharma Operations Analytics`
   - **Description:**
     > This space answers business questions about pharmaceutical operations,
     > including inventory levels and expiry risk, sales performance by outlet
     > and product, and end-to-end supply chain metrics.
   - **Warehouse:** Select the same SQL warehouse
   - **Tables:** Add:
     - `03_inventory_status`
     - `03_sales_by_outlet`
     - `03_supply_chain_overview`
3. Click **Save**

<!-- Screenshot: Genie space creation with tables selected -->

### Test Your Genie Spaces

Try asking natural language questions in each space:

**Quality Analytics:**
- "Which products have the highest quality failure rate?"
- "What is the cold chain compliance rate by carrier?"
- "Show me facilities with pass rates below 95%"

**Operations Analytics:**
- "Which outlets have the most inventory nearing expiry?"
- "What are the top-selling products by revenue this month?"
- "Show me the supply chain lead times by supplier"

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
3. Name it: `<your_username> - Pharma Insights Dashboard`

### Step 2: Add Datasets (Using Genie Prompt)

In the dashboard editor, you'll add 3 datasets. Use the **Genie prompt** (the AI assistant within the dashboard canvas) to help generate each query.

**Dataset 1 — Quality Overview:**

Click **Add a dataset** (or use the data panel), then use the Genie prompt:

> **Genie Prompt:**
>
> ```
> Write a SQL query against <your_catalog>.<your_username>_demo.03_batch_quality_summary
> that summarizes quality pass/fail rates by product. Include product name,
> total tests, pass count, fail count, and pass rate percentage. Order by
> pass rate ascending to show worst performers first.
> ```

Review the generated SQL, adjust if needed, and save the dataset.

**Dataset 2 — Cold Chain Compliance:**

Add another dataset, use the Genie prompt:

> **Genie Prompt:**
>
> ```
> Write a SQL query against <your_catalog>.<your_username>_demo.03_cold_chain_compliance
> that shows compliance rates by carrier. Include carrier name, total shipments,
> compliant count, non-compliant count, and compliance rate percentage.
> Order by compliance rate ascending.
> ```

Review and save.

**Dataset 3 — Sales Performance:**

Add a third dataset, use the Genie prompt:

> **Genie Prompt:**
>
> ```
> Write a SQL query against <your_catalog>.<your_username>_demo.03_sales_by_outlet
> that shows monthly sales trends. Include month, total quantity sold,
> total revenue, and number of active outlets. Order by month.
> ```

Review and save.

### Step 3: Build Visualizations (Using Genie Prompt)

Now use the Genie prompt on the dashboard canvas to create visualizations from your datasets.

> **Genie Prompt:**
>
> ```
> Using the datasets I've added, create the following visualizations:
> 1. A counter/stat showing overall quality pass rate from the Quality Overview dataset
> 2. A bar chart showing pass/fail rates by product from the Quality Overview dataset
> 3. A bar chart showing compliance rates by carrier from the Cold Chain Compliance dataset
> 4. A line chart showing monthly revenue trends from the Sales Performance dataset
> ```

Arrange the visualizations on the canvas by dragging and resizing them.

### Step 4: Publish

1. Click **Publish** in the top-right corner of the dashboard editor
2. The dashboard is now accessible to other users in the workspace

<!-- Screenshot: Completed dashboard with visualizations -->

### Validate

1. In **Dashboards**, find your published dashboard
2. Open it and confirm:
   - The counter shows an overall pass rate
   - The bar charts render with data
   - The line chart shows monthly trends
3. Try interacting with filters or clicking on chart elements

---

## Wrap-Up

Congratulations! You've completed the Pharma tutorial! Here's what you accomplished:

| Step | What You Built | Tool Used |
|------|---------------|-----------|
| Exercise 1 | A Unity Catalog schema for your demo | Workspace UI |
| Exercise 2 | A managed volume for landing raw data | Workspace UI |
| Exercise 3 | Uploaded Pharma sample data via drag & drop | Workspace UI |
| Exercise 4 | Created pipeline + bronze layer with Auto Loader | Workspace UI + Genie Code |
| Exercise 5 | Silver layer — data quality constraints | Genie Code in Pipeline IDE |
| Exercise 6 | Gold layer — business aggregation views | Genie Code in Pipeline IDE |
| Exercise 7 | Ran the end-to-end DLT pipeline | Workspace UI |
| Exercise 8 | Genie spaces for natural language analytics | Workspace UI |
| Exercise 9 | Dashboard with 3 datasets and visualizations | UI + Genie Code |

**What's Next?**
- Try modifying the gold-layer transformations or adding new aggregations using the Genie Code
- Ask questions in your Genie spaces and see how the AI interprets them
- Try the [FSI tutorial](TUTORIAL_FSI.md) to build a second pipeline
