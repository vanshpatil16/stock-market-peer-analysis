# 📊 Indian Stock Peer Group Analysis Dashboard

A comprehensive Streamlit web application that allows you to compare Indian stock (NSE/BSE) performance against their peer groups. Analyze how different Indian stocks perform relative to each other over various time horizons with interactive visualizations.

## 🎯 What This Project Does

This application provides a **peer analysis dashboard** for stock market data. It enables users to:

- **Compare multiple stocks** side-by-side on normalized price charts
- **Analyze individual stock performance** against their peer group average
- **Visualize performance metrics** over different time periods (1 month to 20 years)
- **Share analysis views** via URL parameters
- **Explore stock relationships** through interactive charts and metrics

## 🏗️ Project Structure

```
demo-stockpeers/
├── streamlit_app.py    # Main application file (all logic and UI)
├── pyproject.toml      # Project configuration and dependencies
├── uv.lock            # Locked dependency versions for reproducibility
├── README.md          # This file
├── LICENSE            # Apache 2.0 License
└── .venv/             # Virtual environment (created after setup)
```

## 🛠️ Technology Stack

### What, Why, and Where They're Used

| Technology | What It Is | Why It's Used | Where It's Used |
|------------|------------|---------------|-----------------|
| **Streamlit** | Python web framework | Rapidly build interactive web apps without HTML/CSS/JS | Entire UI, widgets, caching, session state |
| **yfinance** | Yahoo Finance API wrapper | Fetch real-time and historical stock data (supports Indian stocks with .NS/.BO suffix) | Data fetching in `load_data()` function |
| **pandas** | Data manipulation library | Process and transform stock price data | Data normalization, DataFrame operations |
| **Altair** | Declarative visualization library | Create interactive charts with minimal code | All chart visualizations (line, area charts) |
| **uv** | Fast Python package manager | Quick dependency management and virtual environments | Project setup and dependency installation |

## 📋 Prerequisites

- **Python 3.10+** (required by `pyproject.toml`)
- **uv** package manager ([Installation guide](https://github.com/astral-sh/uv))

## 🚀 Installation & Setup

### Step 1: Create Virtual Environment

```bash
# Windows PowerShell
uv venv

# Linux/Mac
uv venv
```

This creates a `.venv` directory with an isolated Python environment.

### Step 2: Activate Virtual Environment

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
uv sync
```

This installs all required packages:
- `streamlit>=1.44.2` - Web framework
- `yfinance>=0.2.55` - Stock data API
- `pandas>=2.2.3` - Data processing
- `altair>=5.5.0` - Charting library

### Step 4: Run the Application

**Option A: Using uv (Recommended)**
```bash
uv run streamlit run streamlit_app.py
```

**Option B: With Activated Virtual Environment**
```bash
streamlit run streamlit_app.py
```

The app will start and display:
- **Local URL**: `http://localhost:8501` (or next available port)
- **Network URL**: Accessible from other devices on your network

## 📖 How to Use the App

### 1. **Select Stocks**

- Use the **"Stock tickers"** multiselect dropdown in the left panel
- Choose from 70+ predefined Indian stocks (RELIANCE.NS, TCS.NS, HDFCBANK.NS, etc.)
- Or type custom ticker symbols (e.g., "RELIANCE.NS", "TCS.NS", "INFY.NS")
- **Note**: Use `.NS` suffix for NSE (National Stock Exchange) stocks or `.BO` for BSE (Bombay Stock Exchange) stocks
- Default selection: `["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "ITC.NS"]`

### 2. **Choose Time Horizon**

- Select a time period using the **"Time horizon"** pills selector
- Options: 1 Month, 3 Months, 6 Months, 1 Year, 5 Years, 10 Years, 20 Years
- Default: **6 Months**

### 3. **View Visualizations**

The app displays several sections:

#### **Main Comparison Chart** (Right Panel)
- Normalized price chart showing all selected stocks
- All stocks start at 1.0 for easy comparison
- Interactive tooltips on hover

#### **Performance Metrics** (Left Panel Bottom)
- **Best Stock**: Highest performing stock with percentage gain
- **Worst Stock**: Lowest performing stock with percentage change

#### **Individual vs Peer Average** (Main Section)
- For each selected stock:
  - **Line Chart**: Stock price vs peer average (excluding itself)
  - **Area Chart**: Difference between stock and peer average
- Helps identify stocks outperforming or underperforming their peers

#### **Raw Data Table** (Bottom)
- Complete historical price data for all selected stocks
- Sortable and searchable DataFrame

### 4. **Share Your Analysis**

- The URL automatically updates with selected stocks
- Copy and share the URL to let others see the same view
- Example: `http://localhost:8501/?stocks=RELIANCE.NS,TCS.NS,HDFCBANK.NS`

## 🔄 Complete Workflow

### Application Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Opens Browser                        │
│                  (http://localhost:8501)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Streamlit App Initialization                    │
│  • Loads default stocks from query params or session state  │
│  • Sets up page layout (wide mode, 2 columns)              │
│  • Initializes UI components                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              User Interaction Layer                         │
│  ┌──────────────────┐      ┌──────────────────┐           │
│  │ Stock Selector   │      │ Time Horizon     │           │
│  │ (Multiselect)    │      │ (Pills)          │           │
│  └────────┬─────────┘      └────────┬─────────┘           │
│           │                          │                      │
│           └──────────┬───────────────┘                      │
│                      ▼                                      │
│           Updates Query Parameters                          │
│           Updates Session State                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Loading (Cached)                          │
│                                                             │
│  @st.cache_resource(ttl="6h")                              │
│  ┌─────────────────────────────────────┐                   │
│  │ 1. Check Cache                      │                   │
│  │    • Cache Hit? → Use cached data   │                   │
│  │    • Cache Miss? → Continue         │                   │
│  └─────────────────────────────────────┘                   │
│                      │                                      │
│                      ▼                                      │
│  ┌─────────────────────────────────────┐                   │
│  │ 2. Fetch from yfinance API          │                   │
│  │    yf.Tickers(tickers)              │                   │
│  │    .history(period=period)          │                   │
│  └─────────────────────────────────────┘                   │
│                      │                                      │
│                      ▼                                      │
│  ┌─────────────────────────────────────┐                   │
│  │ 3. Extract Closing Prices           │                   │
│  │    data["Close"]                    │                   │
│  └─────────────────────────────────────┘                   │
│                      │                                      │
│                      ▼                                      │
│  ┌─────────────────────────────────────┐                   │
│  │ 4. Store in Cache (6 hours)         │                   │
│  └─────────────────────────────────────┘                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Processing                                │
│                                                             │
│  1. Normalize Prices:                                       │
│     normalized = data.div(data.iloc[0])                     │
│     (All stocks start at 1.0)                              │
│                                                             │
│  2. Calculate Metrics:                                      │
│     • Latest normalized values                             │
│     • Best/Worst performers                                │
│                                                             │
│  3. Compute Peer Averages:                                  │
│     For each stock:                                         │
│       peers = normalized.drop(columns=[ticker])            │
│       peer_avg = peers.mean(axis=1)                       │
│       delta = stock - peer_avg                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Visualization Layer                            │
│                                                             │
│  ┌─────────────────────────────────────┐                   │
│  │ 1. Main Normalized Price Chart      │                   │
│  │    (Altair line chart)              │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
│  ┌─────────────────────────────────────┐                   │
│  │ 2. Performance Metrics              │                   │
│  │    (Best/Worst stock cards)         │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
│  ┌─────────────────────────────────────┐                   │
│  │ 3. Individual vs Peer Charts        │                   │
│  │    (Line + Area charts per stock)   │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
│  ┌─────────────────────────────────────┐                   │
│  │ 4. Raw Data Table                    │                   │
│  │    (Interactive DataFrame)           │                   │
│  └─────────────────────────────────────┘                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              User Sees Updated Visualizations                │
│              (Real-time updates on interaction)             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
yfinance API
    │
    ├─→ Historical OHLCV Data (Open, High, Low, Close, Volume)
    │
    ├─→ Extract Close Prices → pandas DataFrame
    │
    ├─→ Normalize: price[t] / price[0] → All start at 1.0
    │
    ├─→ Calculate Peer Averages (excluding self for each stock)
    │
    ├─→ Compute Deltas (stock - peer_avg)
    │
    └─→ Transform to Altair Chart Format
         │
         └─→ Display in Streamlit UI
```

## 🔍 Code Architecture

### Key Components

#### 1. **Imports & Configuration** (Lines 16-25)
```python
import streamlit as st      # UI framework
import yfinance as yf       # Stock data API
import pandas as pd         # Data manipulation
import altair as alt        # Charting library

st.set_page_config(...)     # Page setup (wide layout)
```

**Why**: Sets up the foundation - imports necessary libraries and configures the page layout.

#### 2. **Stock Data Constants** (Lines 38-134)
```python
STOCKS = ["AAPL", "MSFT", ...]  # 100+ predefined tickers
DEFAULT_STOCKS = [...]          # Default selection
```

**Why**: Provides a curated list of major stocks and sensible defaults for first-time users.

#### 3. **Session State & URL Parameters** (Lines 143-197)
```python
st.session_state.tickers_input  # Stores user selection
st.query_params["stocks"]        # URL-based state for sharing
```

**Why**: 
- **Session state**: Maintains user selections during app interaction
- **Query params**: Enables shareable URLs and bookmarking

#### 4. **Cached Data Loading** (Lines 209-215)
```python
@st.cache_resource(show_spinner=False, ttl="6h")
def load_data(tickers, period):
    tickers_obj = yf.Tickers(tickers)
    data = tickers_obj.history(period=period)
    return data["Close"]
```

**Why**:
- **Caching**: Avoids redundant API calls (saves time and respects rate limits)
- **6-hour TTL**: Balances freshness with performance
- **Returns Close prices**: Only what's needed for analysis

**Where**: Called whenever stocks or time period changes.

#### 5. **Data Normalization** (Line 233)
```python
normalized = data.div(data.iloc[0])
```

**Why**: Normalizes all stocks to start at 1.0, making percentage comparisons meaningful regardless of absolute price differences.

**Where**: Applied before all visualizations.

#### 6. **Peer Average Calculation** (Lines 295-297)
```python
peers = normalized.drop(columns=[ticker])
peer_avg = peers.mean(axis=1)
```

**Why**: Excludes the stock being analyzed from its peer group to show true relative performance.

**Where**: Used in individual stock comparison charts.

#### 7. **Visualization Components**

**Main Chart** (Lines 260-274): Altair line chart showing all stocks
**Metrics** (Lines 244-256): Best/worst stock cards
**Individual Charts** (Lines 308-348): Per-stock comparison charts

**Why**: Multiple views provide different insights:
- Overview: See all stocks together
- Metrics: Quick performance summary
- Individual: Deep dive into each stock's relative performance

## ✨ Key Features

### 1. **Intelligent Caching**
- Reduces API calls by caching data for 6 hours
- Improves performance and respects rate limits
- Automatically invalidates after TTL expires

### 2. **URL State Management**
- Selected stocks stored in URL query parameters
- Shareable links preserve analysis views
- Browser back/forward navigation works

### 3. **Error Handling**
- Rate limit detection and user-friendly warnings
- Missing data validation
- Empty ticker prevention

### 4. **Interactive Visualizations**
- Hover tooltips on charts
- Responsive layout adapts to screen size
- Real-time updates on user input

### 5. **Peer Analysis Logic**
- Excludes self from peer average calculation
- Provides fair comparison baseline
- Highlights outperformance/underperformance

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'yfinance'`

**Solution**: Make sure you're using the virtual environment:
```bash
# Option 1: Use uv run (recommended)
uv run streamlit run streamlit_app.py

# Option 2: Activate virtual environment first
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac
streamlit run streamlit_app.py
```

### Issue: Rate Limiting Warnings

**Why**: yfinance API has rate limits. The app handles this gracefully.

**Solution**: 
- Wait a few minutes and try again
- The cache will help reduce API calls on subsequent uses

### Issue: No Data for Some Tickers

**Why**: Invalid ticker symbols or delisted stocks.

**Solution**: 
- Verify ticker symbols are correct
- Check if stocks are still actively traded
- The app will show an error message for problematic tickers

### Issue: Port Already in Use

**Solution**: Streamlit will automatically use the next available port, or specify one:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📊 Example Use Cases

1. **Portfolio Analysis**: Compare your Indian stock holdings against each other
2. **Sector Comparison**: Analyze stocks within the same industry (e.g., Banking: HDFCBANK.NS, ICICIBANK.NS, KOTAKBANK.NS)
3. **Performance Tracking**: Monitor how Indian stocks perform over time
4. **Investment Research**: Identify outperforming stocks in a peer group
5. **Educational**: Learn about Indian stock market trends and relationships

## 🇮🇳 Indian Stock Ticker Format

- **NSE (National Stock Exchange)**: Append `.NS` to the ticker (e.g., `RELIANCE.NS`, `TCS.NS`)
- **BSE (Bombay Stock Exchange)**: Append `.BO` to the ticker (e.g., `RELIANCE.BO`, `TCS.BO`)
- Most popular stocks are listed on NSE, so `.NS` is commonly used
- You can mix NSE and BSE stocks in the same analysis

## 🚀 Deploying to Streamlit Cloud

Streamlit Cloud offers free hosting for Streamlit apps. Follow these steps to deploy your app:

### Prerequisites

1. **GitHub Account**: You need a GitHub account (free)
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Git Repository**: Your code should be in a GitHub repository

### Step-by-Step Deployment

#### Step 1: Prepare Your Repository

1. **Create a GitHub Repository** (if you haven't already):
   ```bash
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit: Indian Stock Peer Analysis Dashboard"
   
   # Create repository on GitHub, then push
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

2. **Ensure Required Files Are Present**:
   - ✅ `streamlit_app.py` - Your main app file
   - ✅ `requirements.txt` - Dependencies (already created)
   - ✅ `README.md` - Documentation
   - ✅ `.gitignore` - To exclude unnecessary files (optional but recommended)

#### Step 2: Create `.gitignore` (Recommended)

Create a `.gitignore` file to exclude unnecessary files:

```gitignore
# Virtual environment
.venv/
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Lock files (optional - you can include uv.lock if you want)
uv.lock
```

#### Step 3: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

2. **Sign In**: Use your GitHub account to sign in

3. **New App**:
   - Click "New app" button
   - Select your GitHub repository
   - Choose the branch (usually `main` or `master`)
   - Set the **Main file path**: `streamlit_app.py`
   - Set the **App URL**: Choose a custom subdomain (e.g., `indian-stock-analysis`)

4. **Advanced Settings** (Optional):
   - **Python version**: 3.10 or higher (default is usually fine)
   - **Dependencies file**: `requirements.txt` (auto-detected)

5. **Deploy**: Click "Deploy"

#### Step 4: Wait for Deployment

- Streamlit Cloud will:
  - Install dependencies from `requirements.txt`
  - Run your app
  - Provide a public URL (e.g., `https://indian-stock-analysis.streamlit.app`)

### Deployment Configuration

#### Using `requirements.txt` (Current Setup)

Your `requirements.txt` file is already created with:
```
altair>=5.5.0
pandas>=2.2.3
streamlit>=1.44.2
yfinance>=0.2.55
```

Streamlit Cloud will automatically detect and use this file.

#### Alternative: Using `pyproject.toml`

If you prefer using `pyproject.toml` (which you already have), Streamlit Cloud also supports it. However, `requirements.txt` is more widely supported and recommended.

### Post-Deployment

1. **Share Your App**: Your app will be publicly accessible at the provided URL
2. **Update Code**: Push changes to GitHub, and Streamlit Cloud will automatically redeploy
3. **Monitor**: Check the "Manage app" section for logs and settings

### Troubleshooting Deployment

#### Issue: App Fails to Deploy

**Check**:
- ✅ All dependencies are in `requirements.txt`
- ✅ `streamlit_app.py` is in the root directory
- ✅ Python version is 3.10+ (check in Streamlit Cloud settings)
- ✅ No syntax errors in your code

#### Issue: Module Not Found Errors

**Solution**: Ensure all imports are listed in `requirements.txt`

#### Issue: App Deploys But Shows Errors

**Check Logs**:
- Go to "Manage app" → "Logs" in Streamlit Cloud
- Look for error messages
- Common issues: missing dependencies, API rate limits, data fetching errors

### Environment Variables (If Needed)

If you need to add API keys or secrets later:

1. Go to "Manage app" → "Settings" → "Secrets"
2. Add secrets in TOML format:
   ```toml
   [secrets]
   API_KEY = "your-api-key"
   ```
3. Access in code: `st.secrets["API_KEY"]`

**Note**: This app doesn't require any API keys (yfinance is free), but this is useful for future enhancements.

### Custom Domain (Optional)

Streamlit Cloud free tier provides:
- `your-app-name.streamlit.app` subdomain
- Custom domains available on paid plans

### Automatic Updates

- **Auto-deploy**: Enabled by default
- Every push to your main branch triggers a redeploy
- Manual redeploy available in "Manage app" → "Reboot app"

## 🔗 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Altair Chart Gallery](https://altair-viz.github.io/gallery/)

---

**Happy Analyzing! 📈**

#   s t o c k - m a r k e t - p e e r - a n a l y s i s  
 