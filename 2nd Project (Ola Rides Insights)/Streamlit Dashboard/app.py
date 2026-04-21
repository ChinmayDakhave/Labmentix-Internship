# =====================================================
# UBER-STYLE RIDE ANALYTICS DASHBOARD
# Modern, Dark-Themed Streamlit Application
# =====================================================
# Instructions:
# 1. Install required libraries:
#    pip install streamlit pandas plotly
# 2. Place this script and your 'queries.sql' file in the same folder
# 3. Update the DB_PATH variable below with your SQLite database file path
# 4. Run: streamlit run dashboard.py
# =====================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import re

# =====================================================
# CONFIGURATION - UPDATE THIS WITH YOUR DATABASE PATH
# =====================================================
DB_PATH = "2nd Project (Ola Rides Insights)/Streamlit Dashboard/ola_rides.db"  # <-- CHANGE THIS to your SQLite file path
QUERIES_FILE = "queries.sql"   # Path to your SQL queries file

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Ride Analytics Dashboard",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS FOR MODERN DARK THEME WITH GRADIENTS
# =====================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0c1222 50%, #0a0f1e 100%);
    }
    
    /* Glassmorphism card effect */
    .glass-card {
        background: rgba(18, 25, 45, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 40, 60, 0.8) 0%, rgba(20, 30, 50, 0.8) 100%);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        border-bottom: 3px solid;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #b0c4ff 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #8e9aaf;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    /* Headers */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        background: linear-gradient(120deg, #ffffff 30%, #7c8db0 80%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-weight: 700;
    }
    
    h1 {
        font-size: 2.5rem !important;
        letter-spacing: -0.02em;
    }
    
    /* Dataframe styling */
    .dataframe-container {
        background: rgba(18, 25, 45, 0.5);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1f2e;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: #3a4a6e;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #5a6e9a;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2a3a5e 0%, #1a2a4a 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3a4a6e 0%, #2a3a5e 100%);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-1px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 40, 60, 0.5);
        border-radius: 12px;
        font-weight: 500;
        color: #cbd5ff;
    }
    .streamlit-expanderContent {
        background: rgba(18, 25, 45, 0.4);
        border-radius: 0 0 12px 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(18, 25, 45, 0.5);
        border-radius: 16px;
        padding: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 8px 20px;
        font-weight: 500;
        color: #8e9aaf;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2a3a5e 0%, #1e2e4e 100%);
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(10, 15, 30, 0.8);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Status messages */
    .stAlert {
        background: rgba(30, 40, 60, 0.8);
        border-radius: 12px;
        border-left: 4px solid;
    }
    
    /* Divider */
    hr {
        margin: 1rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

@st.cache_data
def load_queries_from_file(filepath):
    """Parse SQL queries file and extract queries with their descriptions."""
    if not Path(filepath).exists():
        st.error(f"❌ Queries file not found: {filepath}")
        return []
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split by semicolon followed by newline (end of statement)
    raw_statements = re.split(r';\s*\n', content)
    
    queries = []
    for stmt in raw_statements:
        stmt = stmt.strip()
        if not stmt:
            continue
        
        # Extract comment as description (first line starting with '--')
        lines = stmt.split('\n')
        description = ""
        sql_lines = []
        for line in lines:
            if line.strip().startswith('--'):
                description = line.strip().lstrip('--').strip()
            else:
                sql_lines.append(line)
        
        sql = ' '.join(sql_lines).strip()
        if sql:
            # If no description found, use first few words of SQL
            if not description:
                description = sql[:50] + "..."
            queries.append({
                'description': description,
                'sql': sql
            })
    
    return queries

@st.cache_data
def execute_query(db_path, sql_query):
    """Execute SQL query and return DataFrame, handle errors gracefully."""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

def test_db_connection(db_path):
    """Test if database connection is successful."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return True, [t[0] for t in tables]
    except Exception as e:
        return False, str(e)

def create_metric_card(value, label, color="#4a6a9a"):
    """Display a metric in a styled card using HTML/CSS."""
    return f"""
    <div class="metric-card" style="border-bottom-color: {color};">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

# =====================================================
# SIDEBAR - CONNECTION SETUP
# =====================================================
with st.sidebar:
    st.markdown("## 🚖 Ride Analytics")
    st.markdown("---")
    
    # Database connection configuration
    st.markdown("### 🔌 Database Connection")
    
    # Allow user to override DB_PATH at runtime
    db_path_input = st.text_input(
        "SQLite Database Path",
        value=DB_PATH,
        help="Enter the full path to your SQLite .db file"
    )
    
    if db_path_input:
        DB_PATH = db_path_input
    
    # Test connection button
    if st.button("🔗 Test Connection", use_container_width=True):
        with st.spinner("Testing connection..."):
            success, result = test_db_connection(DB_PATH)
            if success:
                st.success(f"✅ Connected successfully!")
                st.caption(f"📊 Tables found: {', '.join(result[:5])}" + ("..." if len(result) > 5 else ""))
                st.session_state['db_connected'] = True
            else:
                st.error(f"❌ Connection failed: {result}")
                st.session_state['db_connected'] = False
    
    # Check initial connection state
    if 'db_connected' not in st.session_state:
        st.session_state['db_connected'] = False
    
    st.markdown("---")
    st.caption("💡 **Tip:** Make sure your database contains a 'rides' table matching the queries.")
    st.caption("📁 **Queries file:** `queries.sql` should be in the same directory.")

# =====================================================
# MAIN CONTENT
# =====================================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("🚀 Ride Operations Analytics")
st.caption("Real-time insights | Driver & Customer Metrics | Revenue Analysis")
st.markdown('</div>', unsafe_allow_html=True)

# Check database connection before proceeding
if not st.session_state['db_connected']:
    st.warning("⚠️ **Database not connected** | Please configure your database path in the sidebar and click 'Test Connection'.")
    st.stop()

# Load queries from file
queries = load_queries_from_file(QUERIES_FILE)
if not queries:
    st.error(f"❌ No queries found in {QUERIES_FILE}. Please ensure the file exists and contains valid SQL statements.")
    st.stop()

st.success(f"✅ Loaded {len(queries)} queries from `{QUERIES_FILE}`")

# =====================================================
# EXECUTE ALL QUERIES AND STORE RESULTS
# =====================================================
@st.cache_data
def fetch_all_query_results(db_path, queries_list):
    """Execute all queries and return results dictionary."""
    results = {}
    for idx, q in enumerate(queries_list):
        df, error = execute_query(db_path, q['sql'])
        results[idx] = {
            'description': q['description'],
            'sql': q['sql'],
            'df': df,
            'error': error
        }
    return results

with st.spinner("📊 Executing queries and loading data..."):
    query_results = fetch_all_query_results(DB_PATH, queries)

# =====================================================
# KPI DASHBOARD - Extract metrics from relevant queries
# =====================================================
st.markdown("## 📈 Key Performance Indicators")
st.markdown("---")

# Extract values from specific queries
kpi_data = {}

# Q1: Successful bookings count
if 0 in query_results and query_results[0]['df'] is not None:
    kpi_data['successful_rides'] = len(query_results[0]['df'])

# Q3: Customer cancellations
if 2 in query_results and query_results[2]['df'] is not None and not query_results[2]['df'].empty:
    kpi_data['customer_cancellations'] = query_results[2]['df'].iloc[0, 0]

# Q5: Driver cancellations
if 4 in query_results and query_results[4]['df'] is not None and not query_results[4]['df'].empty:
    kpi_data['driver_cancellations'] = query_results[4]['df'].iloc[0, 0]

# Q9: Total revenue
if 8 in query_results and query_results[8]['df'] is not None and not query_results[8]['df'].empty:
    revenue_val = query_results[8]['df'].iloc[0, 0]
    kpi_data['total_revenue'] = f"${revenue_val:,.2f}" if revenue_val else "$0"

# Q4: Total customers (distinct from top 5 query? Better to get count from Q4 dataframe)
if 3 in query_results and query_results[3]['df'] is not None:
    kpi_data['total_customers_booked'] = len(query_results[3]['df'])

# Display KPI row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(create_metric_card(
        kpi_data.get('successful_rides', 'N/A'), 
        "Successful Rides", 
        "#2ecc71"
    ), unsafe_allow_html=True)
with col2:
    st.markdown(create_metric_card(
        kpi_data.get('total_revenue', 'N/A'), 
        "Total Revenue", 
        "#f1c40f"
    ), unsafe_allow_html=True)
with col3:
    st.markdown(create_metric_card(
        kpi_data.get('customer_cancellations', 'N/A'), 
        "Customer Cancellations", 
        "#e74c3c"
    ), unsafe_allow_html=True)
with col4:
    st.markdown(create_metric_card(
        kpi_data.get('driver_cancellations', 'N/A'), 
        "Driver Cancellations", 
        "#e67e22"
    ), unsafe_allow_html=True)
with col5:
    st.markdown(create_metric_card(
        kpi_data.get('total_customers_booked', 'N/A'), 
        "Active Customers", 
        "#9b59b6"
    ), unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# VISUALIZATION SECTION (Enhanced insights)
# =====================================================
st.markdown("## 📊 Visual Analytics")

# Create two columns for charts
chart_col1, chart_col2 = st.columns(2)

# Chart 1: Average ride distance per vehicle type (Q2)
with chart_col1:
    if 1 in query_results and query_results[1]['df'] is not None:
        df_q2 = query_results[1]['df']
        if not df_q2.empty:
            fig = px.bar(
                df_q2, x='Vehicle_Type', y='avg_distance',
                title="Average Ride Distance by Vehicle Type",
                labels={'avg_distance': 'Avg Distance (km)', 'Vehicle_Type': 'Vehicle Type'},
                color='avg_distance',
                color_continuous_scale='tealrose',
                text_auto='.2f'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#cbd5ff',
                title_font_color='white',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

# Chart 2: Top 5 customers by rides (Q4)
with chart_col2:
    if 3 in query_results and query_results[3]['df'] is not None:
        df_q4 = query_results[3]['df']
        if not df_q4.empty:
            fig = px.bar(
                df_q4, x='Customer_ID', y='total_rides',
                title="Top 5 Customers by Ride Count",
                labels={'total_rides': 'Number of Rides', 'Customer_ID': 'Customer ID'},
                color='total_rides',
                color_continuous_scale='blues',
                text_auto=True
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#cbd5ff',
                title_font_color='white',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

# Second row of charts
chart_col3, chart_col4 = st.columns(2)

# Chart 3: Average customer rating per vehicle type (Q8)
with chart_col3:
    if 7 in query_results and query_results[7]['df'] is not None:
        df_q8 = query_results[7]['df']
        if not df_q8.empty:
            fig = px.bar(
                df_q8, x='Vehicle_Type', y='avg_customer_rating',
                title="Average Customer Rating by Vehicle Type",
                labels={'avg_customer_rating': 'Avg Rating (1-5)', 'Vehicle_Type': 'Vehicle Type'},
                color='avg_customer_rating',
                color_continuous_scale='viridis',
                range_y=[0, 5],
                text_auto='.2f'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#cbd5ff',
                title_font_color='white',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

# Chart 4: Driver Ratings Range for Prime Sedan (Q6) - show as gauge or indicator
with chart_col4:
    if 5 in query_results and query_results[5]['df'] is not None:
        df_q6 = query_results[5]['df']
        if not df_q6.empty:
            max_rating = df_q6['max_rating'].iloc[0]
            min_rating = df_q6['min_rating'].iloc[0]
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = (max_rating + min_rating) / 2,
                delta = {'reference': 4.0, 'valueformat': '.1f'},
                title = {'text': "Prime Sedan Driver Ratings", 'font': {'color': 'white'}},
                gauge = {
                    'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#4a6a9a"},
                    'steps': [
                        {'range': [0, min_rating], 'color': "rgba(200, 100, 100, 0.3)"},
                        {'range': [min_rating, max_rating], 'color': "rgba(100, 200, 100, 0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_rating
                    }
                }
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=300
            )
            fig.add_annotation(
                x=0.5, y=0.2, xref="paper", yref="paper",
                text=f"Range: {min_rating:.1f} - {max_rating:.1f}",
                showarrow=False,
                font=dict(color="#cbd5ff", size=12)
            )
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================================
# DETAILED QUERY RESULTS
# =====================================================
st.markdown("## 📋 Detailed Query Results")
st.markdown("Explore each query's raw data below.")

# Create tabs for different categories of queries
tab1, tab2, tab3 = st.tabs(["💰 Revenue & Bookings", "🚗 Vehicle Analytics", "⚠️ Cancellations & Issues"])

# Organize queries into tabs
with tab1:
    # Q1: Successful bookings
    if 0 in query_results:
        with st.expander("✅ Q1: All Successful Bookings", expanded=False):
            if query_results[0]['error']:
                st.error(f"Error: {query_results[0]['error']}")
            else:
                st.dataframe(query_results[0]['df'], use_container_width=True, height=400)
                st.caption(f"📊 {len(query_results[0]['df'])} rows returned")
    
    # Q7: UPI payments
    if 6 in query_results:
        with st.expander("💳 Q7: Rides Paid by UPI", expanded=False):
            if query_results[6]['error']:
                st.error(f"Error: {query_results[6]['error']}")
            else:
                st.dataframe(query_results[6]['df'], use_container_width=True, height=400)
                st.caption(f"📊 {len(query_results[6]['df'])} rows returned")
    
    # Q9: Total booking value
    if 8 in query_results:
        with st.expander("💰 Q9: Total Revenue from Successful Rides", expanded=False):
            if query_results[8]['error']:
                st.error(f"Error: {query_results[8]['error']}")
            else:
                val = query_results[8]['df'].iloc[0, 0]
                st.metric("Total Revenue", f"${val:,.2f}" if val else "$0")
                st.dataframe(query_results[8]['df'], use_container_width=True)

with tab2:
    # Q2: Avg distance per vehicle
    if 1 in query_results:
        with st.expander("📏 Q2: Average Ride Distance per Vehicle Type", expanded=False):
            if query_results[1]['error']:
                st.error(f"Error: {query_results[1]['error']}")
            else:
                st.dataframe(query_results[1]['df'], use_container_width=True)
    
    # Q6: Max/Min driver ratings for Prime Sedan
    if 5 in query_results:
        with st.expander("⭐ Q6: Driver Ratings Range (Prime Sedan)", expanded=False):
            if query_results[5]['error']:
                st.error(f"Error: {query_results[5]['error']}")
            else:
                st.dataframe(query_results[5]['df'], use_container_width=True)
    
    # Q8: Avg customer rating per vehicle
    if 7 in query_results:
        with st.expander("📝 Q8: Average Customer Rating per Vehicle Type", expanded=False):
            if query_results[7]['error']:
                st.error(f"Error: {query_results[7]['error']}")
            else:
                st.dataframe(query_results[7]['df'], use_container_width=True)

with tab3:
    # Q3: Customer cancellations
    if 2 in query_results:
        with st.expander("❌ Q3: Total Cancelled Rides by Customers", expanded=False):
            if query_results[2]['error']:
                st.error(f"Error: {query_results[2]['error']}")
            else:
                st.dataframe(query_results[2]['df'], use_container_width=True)
    
    # Q5: Driver cancellations (personal/car issues)
    if 4 in query_results:
        with st.expander("🔧 Q5: Driver Cancellations (Personal/Car Issues)", expanded=False):
            if query_results[4]['error']:
                st.error(f"Error: {query_results[4]['error']}")
            else:
                st.dataframe(query_results[4]['df'], use_container_width=True)
    
    # Q10: Incomplete rides with reasons
    if 9 in query_results:
        with st.expander("⚠️ Q10: All Incomplete Rides with Reasons", expanded=False):
            if query_results[9]['error']:
                st.error(f"Error: {query_results[9]['error']}")
            else:
                st.dataframe(query_results[9]['df'], use_container_width=True, height=400)
                st.caption(f"📊 {len(query_results[9]['df'])} incomplete rides found")

# =====================================================
# ADDITIONAL: Top Customers Section (Q4)
# =====================================================
st.markdown("---")
st.markdown("## 🏆 Customer Leadership Board")

if 3 in query_results and query_results[3]['df'] is not None:
    df_top = query_results[3]['df']
    if not df_top.empty:
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.dataframe(df_top, use_container_width=True, hide_index=True)
        with col_b:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Insights")
            st.markdown(f"- **Top Customer:** {df_top.iloc[0]['Customer_ID']} with **{df_top.iloc[0]['total_rides']}** rides")
            if len(df_top) > 1:
                st.markdown(f"- **2nd Place:** {df_top.iloc[1]['Customer_ID']} ({df_top.iloc[1]['total_rides']} rides)")
            st.markdown(f"- **Total rides from top 5:** {df_top['total_rides'].sum()}")
            st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #5a6e8a; padding: 2rem 0 1rem 0;'>"
    "🚀 Dashboard built with Streamlit • Data from SQLite • Modern Analytics"
    "</div>",
    unsafe_allow_html=True
)
