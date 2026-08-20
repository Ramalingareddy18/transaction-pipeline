# 📊 Dashboard User Guide

## Streamlit Analytics Dashboard

**Read Time**: 10 minutes  
**Audience**: Data Analysts, Business Users, Managers  
**Access URL**: `http://127.0.0.1:8501`

---

## 🎯 Dashboard Overview

The Transaction Pipeline Dashboard provides interactive analytics for transaction data, including:

- 📊 Summary statistics
- 📈 Time-series analysis
- 💰 Category spending breakdown
- 🔴 Anomaly detection visualization
- 🔍 Data exploration tools

---

## 🚀 Starting the Dashboard

### Ensure API is Running First

```bash
# Terminal 1: Start the API
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Wait for: "Application startup complete"
```

### Start the Dashboard

**Windows PowerShell** (Terminal 2)
```powershell
streamlit run dashboard.py

# Opens automatically or visit:
# http://127.0.0.1:8501
```

**macOS/Linux** (Terminal 2)
```bash
streamlit run dashboard.py

# Opens automatically or visit:
# http://127.0.0.1:8501
```

### Browser Access

Open your web browser:
```
http://127.0.0.1:8501
```

You should see:
- Dashboard title: "💰 Transaction Analytics Dashboard"
- Summary statistics at the top
- Charts and tables below

---

## 📊 Dashboard Sections

### 1. Header & Navigation

```
💰 Transaction Analytics Dashboard
[Sidebar]  [Main Content Area]
```

**Sidebar Menu** (Left side)
- Dashboard title
- Refresh controls
- Filter options
- Help section

---

### 2. Summary Metrics Section

The top section displays key statistics:

```
┌─────────────────┬─────────────────┬─────────────────┐
│ Total Txns      │ Net Amount      │ Average Amount  │
│                 │                 │                 │
│ 5,000           │ $125,000.50     │ $25.00          │
└─────────────────┴─────────────────┴─────────────────┘

┌─────────────────┬─────────────────┬─────────────────┐
│ Median Amount   │ Min Amount      │ Max Amount      │
│                 │                 │                 │
│ $15.00          │ -$5,000.00      │ $10,000.00      │
└─────────────────┴─────────────────┴─────────────────┘
```

**Metrics Explained**

| Metric | Description | Interpretation |
|--------|-------------|-----------------|
| **Total Txns** | Total number of transactions | Size of dataset |
| **Net Amount** | Sum of all transaction amounts | Overall balance change |
| **Average** | Mean transaction amount | Typical transaction size |
| **Median** | Middle value transaction | Central tendency |
| **Min Amount** | Smallest transaction | Highest debit |
| **Max Amount** | Largest transaction | Highest credit |

---

### 3. Spending by Category Chart

**Chart Type**: Interactive Bar Chart  
**X-Axis**: Categories (Food, Transport, etc.)  
**Y-Axis**: Total spending amount  

**What It Shows**
- Which categories have highest spending
- How many transactions per category
- Total spent in each category

**How to Use**
```
1. Hover over a bar to see exact values
2. Click legend items to show/hide categories
3. Use zoom tools in top-right of chart
4. Double-click to reset zoom
```

**Example Reading**
```
Food & Dining:    $1,500 spent across 500 transactions
Transportation:   $900 spent across 300 transactions
Income:          $60,000 earned from 12 transactions
```

---

### 4. Daily Total Transactions Chart

**Chart Type**: Interactive Line Chart  
**X-Axis**: Date  
**Y-Axis**: Transaction total per day  

**What It Shows**
- Daily transaction activity over time
- Spending patterns and trends
- Peak and low activity periods

**How to Use**
```
1. Hover over points to see daily totals
2. Pan left/right to navigate dates
3. Click and drag to zoom into date range
4. Double-click to reset zoom
```

---

### 5. Monthly Spending Trend

**Chart Type**: Line Chart with Area Fill  
**X-Axis**: Month (YYYY-MM)  
**Y-Axis**: Cumulative spending  

**What It Shows**
- Spending trends month-to-month
- Whether spending is increasing/decreasing
- Seasonal patterns

**Pattern Analysis**
```
Upward trend:  Spending increasing over months
Downward:      Spending decreasing
Flat:          Consistent spending
Volatility:    Up and down swings
```

---

### 6. Data Explorer Table

**Table Type**: Scrollable, sortable data table

**Features**
- Expandable rows (click to expand)
- Sortable columns (click header)
- Searchable content
- Adjustable view height

**Columns Displayed**
```
transaction_id    → Unique identifier
date              → Transaction date
description       → What was purchased
amount            → Dollar amount
currency          → Currency type (USD)
category          → Spending category
account           → Which account
transaction_type  → Credit or Debit
```

**How to Use**
```
1. Click column header to sort
2. Click row arrow to expand details
3. Scroll horizontally to see more columns
4. Use search box to filter rows
```

---

## 🎮 Interactive Features

### Refresh Data

```
[🔄 Refresh] button at top
- Reloads data from API
- Updates all charts
- Use when API data changed
```

### Filter Controls (Future Enhancement)

```
Sidebar Filters (when implemented):
- Date Range Picker
- Category Multi-Select
- Amount Range Slider
```

---

## 📊 Common Analysis Tasks

### Task 1: Find Highest Spending Category

**Steps**
```
1. Look at "Spending by Category" bar chart
2. Identify tallest bar
3. Hover to see exact amount
4. Click category in legend to isolate
```

**Example**
```
Food & Dining has the highest bar
= Most money spent on food
```

### Task 2: Check Recent Transactions

**Steps**
```
1. Scroll to Data Explorer Table
2. Click column header "date" to sort descending
3. Most recent transactions appear at top
4. Click row to expand full details
```

---

### Task 3: Analyze Spending Trends

**Steps**
```
1. Look at "Monthly Spending Trend" chart
2. Observe line direction (up/down)
3. Identify peak and low months
4. Hover over specific month for exact value
```

**Pattern Recognition**
```
Upward line = Spending increasing
Downward line = Spending decreasing
Sharp spike = Unusual month
```

---

### Task 4: Identify Anomalies

**Steps**
```
1. API returns anomalies automatically
2. Look for unusual amounts in charts
3. Check high-value transactions in table
4. Review anomaly details (see 10_ANOMALY_DETECTION.md)
```

---

## 🔍 Data Quality Indicators

The dashboard shows data health:

```
✓ All data loaded    = No issues
⚠ Partial load       = Some data missing
✗ Load failed        = Connection problem
```

**If data doesn't load**
```
1. Check API is running: http://127.0.0.1:8000/health
2. Check database connection
3. Refresh page (F5)
4. Restart dashboard: streamlit run dashboard.py
```

---

## 🖥️ Browser Compatibility

**Recommended**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Access Requirements**
- JavaScript enabled
- Cookies enabled
- Pop-ups allowed
- 1024x768 minimum resolution

---

## ⚙️ Dashboard Configuration

### Customize Display

**File**: `dashboard.py`

**Editable Settings**
```python
# Title
st.set_page_config(
    page_title="Transaction Analytics",
    page_icon="💰"
)

# API URL
API_URL = "http://127.0.0.1:8000"

# Chart colors
color_palette = "viridis"

# Default refresh interval
REFRESH_SECONDS = 300
```

---

## 🐛 Troubleshooting Dashboard

### Issue: "Unable to reach the API"

**Solution**
```bash
# Check API is running
curl http://127.0.0.1:8000/health

# If not running:
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Then refresh dashboard
```

### Issue: "No data displayed"

**Solution**
```bash
# Check database has data
python src/etl_pipeline.py

# Refresh dashboard
# Or restart dashboard:
streamlit run dashboard.py
```

### Issue: Charts are empty

**Solution**
```
1. Verify API endpoint returns data:
   curl http://127.0.0.1:8000/analytics/summary

2. Check data was loaded:
   python src/etl_pipeline.py

3. Refresh dashboard page (F5)
```

### Issue: Dashboard loads slowly

**Solutions**
```
1. Reduce data size:
   - Filter by date range
   - Query specific categories

2. Increase performance:
   - Restart dashboard
   - Check API performance
   - Monitor database

3. Check resources:
   - Available memory
   - CPU usage
   - Network speed
```

### Issue: Charts not updating

**Solution**
```
1. Click [🔄 Refresh] button
2. Or manually refresh page (F5)
3. If still no update:
   - Restart API
   - Restart dashboard
   - Check data pipeline
```

---

## 📱 Mobile Access

Dashboard works on mobile but optimized for desktop.

**Mobile Considerations**
```
✓ Works on tablets (landscape mode)
⚠ Limited on phones (vertical mode)
- Use horizontal orientation
- Zoom out to see full charts
```

---

## 🎨 Dashboard Customization

### Add New Chart

**File**: `dashboard.py`

```python
# Example: Add a new chart
import streamlit as st
import plotly.express as px

# Get data
data = fetch_summary()

# Create chart
fig = px.pie(
    data,
    values='amount',
    names='category',
    title='Category Distribution'
)

# Display
st.plotly_chart(fig, use_container_width=True)
```

### Modify Metrics

**File**: `dashboard.py`

```python
# Change which metrics display
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("New Metric", value)
```

---

## 📊 Data Export

### Export from Dashboard

**Currently Supported**
```
1. Copy data from table (select → copy)
2. Screenshot charts (browser tools)
3. Download full data via API
```

**Future Feature**
```
- Export to CSV
- Export to PDF reports
- Email report generation
```

---

## 🔐 Dashboard Security

**Current**
- No authentication required (local deployment)
- Access controlled by network

**Production Deployment**
- Add authentication layer
- Implement role-based access
- Use HTTPS
- Add rate limiting

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[1_QUICKSTART.md](1_QUICKSTART.md)** — Quick start guide
- **[4_API_DOCUMENTATION.md](4_API_DOCUMENTATION.md)** — API endpoints
- **[10_ANOMALY_DETECTION.md](10_ANOMALY_DETECTION.md)** — Anomaly details

---

## 🆘 Getting Help

**Dashboard Not Loading**
1. Check API: `curl http://127.0.0.1:8000/health`
2. Check database: `python src/database_connection.py`
3. Restart dashboard: `streamlit run dashboard.py`

**Charts Showing Wrong Data**
1. Run ETL: `python src/etl_pipeline.py`
2. Refresh dashboard: `[🔄 Refresh]` button
3. Clear browser cache: Ctrl+Shift+Delete

**Performance Issues**
1. Close other applications
2. Reduce dataset size
3. Restart dashboard service

---

**Dashboard is fully functional and ready for analysis!** 📊✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
