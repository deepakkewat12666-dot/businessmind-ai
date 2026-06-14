import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import io
import warnings
import streamlit.components.v1 as components

warnings.filterwarnings('ignore')

st.set_page_config(page_title="BusinessMind AI", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------------------------------------
# DESIGN SYSTEM & CSS MOCKUP INJECTION
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');
    
    :root {
        --font-sans: 'Inter', sans-serif;
    }
    
    /* Streamlit Overrides */
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .stApp { background: #08090f; font-family: var(--font-sans); color: #e0e4ff; }
    .block-container { padding-top: 1rem !important; padding-left: 60px !important; padding-right: 1rem !important; max-width: 100% !important;}
    
    /* Mockup CSS */
    .sidebar{position:fixed;top:0;left:0;height:100vh;background:#0d0f1a;width:52px;padding:12px 0;display:flex;flex-direction:column;align-items:center;gap:8px;border-right:0.5px solid #1e2235;z-index:99999}
    .sb-logo{width:32px;height:32px;background:#5b4fcf;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#fff;margin-bottom:8px}
    .sb-icon{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#3a3f5c;font-size:16px;cursor:pointer}
    .sb-icon.active{background:#1a1d2e;color:#7c6df0}
    .sb-icon:hover{background:#151824;color:#7c6df0}
    .sb-div{width:24px;height:0.5px;background:#1e2235;margin:4px 0}
    
    .topbar{position:fixed;top:0;left:52px;right:0;background:#0d0f1a;border-bottom:0.5px solid #1e2235;padding:0 20px;height:48px;display:flex;align-items:center;justify-content:space-between;z-index:99998}
    .topbar-title{font-size:13px;font-weight:500;color:#e0e4ff}
    .topbar-right{display:flex;align-items:center;gap:10px}
    .badge{font-size:10px;padding:3px 8px;border-radius:20px;font-weight:500;display:inline-flex;align-items:center;}
    .badge-purple{background:#1e1a3a;color:#9d8ff5;border:0.5px solid #3d3480}
    .badge-green{background:#0f1f16;color:#4ade80;border:0.5px solid #1a4a2a}
    .badge-amber{background:#1f1700;color:#fbbf24;border:0.5px solid #4a3a00}
    .badge-red{background:rgba(248, 113, 113, 0.1);color:#f87171;border:0.5px solid rgba(248, 113, 113, 0.3)}
    .avatar{width:28px;height:28px;border-radius:50%;background:#5b4fcf;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#fff}
    
    .upload-zone{border:1.5px dashed #1e2235;border-radius:12px;padding:20px;text-align:center;margin-bottom:16px;background:#0d0f1a;position:relative}
    .upload-icon{width:36px;height:36px;background:#1a1d2e;border-radius:10px;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;color:#7c6df0;font-size:18px}
    .upload-title{font-size:13px;font-weight:500;color:#c8cde8;margin-bottom:4px}
    .upload-sub{font-size:11px;color:#3a3f5c}
    
    /* Hide ALL native Streamlit file uploader visuals - keep only functional */
    [data-testid="stFileUploadDropzone"] { 
        position: absolute !important; 
        top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
        width: 100% !important; height: 100% !important;
        opacity: 0 !important; 
        cursor: pointer !important;
        z-index: 10 !important;
        background: transparent !important; 
        border: none !important; 
    }
    [data-testid="stFileUploaderDropzone"] {
        position: absolute !important;
        inset: 0 !important;
        opacity: 0 !important;
        cursor: pointer !important;
        z-index: 10 !important;
    }
    section[data-testid="stFileUploaderDropzone"] > div { display: none !important; }
    [data-testid="stFileUploaderDropzoneInput"] { 
        position: absolute !important; 
        inset: 0 !important; 
        width: 100% !important; 
        height: 100% !important; 
        opacity: 0 !important; 
        cursor: pointer !important;
    }
    /* Hide file uploader label and instructions text */
    .stFileUploader label { display: none !important; }
    .stFileUploader small { display: none !important; }
    .stFileUploader > div > div > div > span { display: none !important; }
    .stFileUploader [data-testid="stMarkdownContainer"] { display: none !important; }
    /* Hide the 'Browse files' button and native dropzone text */
    [data-testid="stFileUploadDropzone"] button { display: none !important; }
    [data-testid="stFileUploadDropzone"] span { display: none !important; }
    [data-testid="stFileUploadDropzone"] small { display: none !important; }
    /* Wrapper to allow overlay positioning */
    .upload-zone-wrapper { position: relative; }
    .upload-zone-wrapper .stFileUploader { 
        position: absolute !important; 
        inset: 0 !important; 
        z-index: 5 !important;
        opacity: 0 !important;
    }
    /* Pull the file uploader widget UP to overlap the custom upload zone above it */
    .stFileUploader {
        margin-top: -145px !important;
        height: 130px !important;
        overflow: hidden !important;
        opacity: 0 !important;
        position: relative !important;
        z-index: 50 !important;
        cursor: pointer !important;
    }
    .stFileUploader > div {
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
    }
    /* Ensure ALL child elements of the file uploader are transparent */
    .stFileUploader * {
        opacity: 0 !important;
        cursor: pointer !important;
    }
    
    .kpi{background:#0d0f1a;border:0.5px solid #1e2235;border-radius:10px;padding:12px 14px;margin-bottom:10px}
    .kpi-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
    .kpi-label{font-size:10px;color:#3a3f5c;text-transform:uppercase;letter-spacing:.06em}
    .kpi-icon{width:26px;height:26px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:13px}
    .kpi-icon.p{background:#1e1a3a;color:#9d8ff5}
    .kpi-icon.g{background:#0f1f16;color:#4ade80}
    .kpi-icon.b{background:#0a1525;color:#60a5fa}
    .kpi-icon.o{background:#1f1500;color:#fbbf24}
    .kpi-val{font-size:20px;font-weight:600;color:#e0e4ff;margin-bottom:2px}
    .kpi-change{font-size:10px;color:#4ade80}
    .kpi-change.neg{color:#f87171}
    
    .chart-card{background:#0d0f1a;border:0.5px solid #1e2235;border-radius:10px;padding:14px;margin-bottom:14px}
    .chart-title{font-size:11px;font-weight:500;color:#6b7199;margin-bottom:12px;display:flex;align-items:center;justify-content:space-between}
    .chart-title span{font-size:10px;color:#3a3f5c}
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 0.5px solid #1e2235; padding-bottom:0; background:#0d0f1a; border-radius:8px; width:fit-content; padding:4px;}
    .stTabs [data-baseweb="tab"] { font-size:10px; padding:6px 16px; border-radius:6px; color:#3a3f5c; font-weight:500; border:none; background:transparent;}
    .stTabs [aria-selected="true"] { background:#1a1d2e !important; color:#9d8ff5 !important; border:none !important;}
    
    .insight{background:#0d0f1a;border:0.5px solid #1e2235;border-radius:10px;padding:12px 14px;display:flex;gap:10px;align-items:flex-start;margin-bottom:10px}
    .ins-dot{width:8px;height:8px;border-radius:50%;margin-top:4px;flex-shrink:0}
    .ins-text{font-size:11px;color:#6b7199;line-height:1.5}
    .ins-val{font-size:11px;font-weight:500;color:#c8cde8}
    
    .quality-row{display:flex;align-items:center;gap:10px;margin-bottom:8px}
    .q-label{font-size:10px;color:#4a5080;width:80px;flex-shrink:0}
    .q-track{flex:1;background:#111424;border-radius:3px;height:5px;overflow:hidden}
    .q-fill{height:100%;border-radius:3px}
    .q-val{font-size:10px;color:#6b7199;width:28px;text-align:right}
    
    .dl-btn{background:#0d0f1a;border:0.5px solid #1e2235;border-radius:8px;padding:10px 12px;display:flex;align-items:center;gap:8px;margin-bottom:10px}
    .dl-btn-icon{width:28px;height:28px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
    .dl-btn-text{font-size:10px;font-weight:500;color:#c8cde8}
    .dl-btn-sub{font-size:9px;color:#3a3f5c}
    
    .section-label{font-size:10px;font-weight:500;color:#3a3f5c;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px;margin-top:10px}

    /* AI Assistant Chat Styles */
    .ai-chat-container { display:flex; flex-direction:column; gap:14px; padding:4px 0; }
    .ai-msg-user { display:flex; justify-content:flex-end; }
    .ai-msg-user .bubble { background:linear-gradient(135deg,#5b4fcf,#7c6df0); color:#fff; border-radius:16px 16px 4px 16px; padding:10px 14px; font-size:12px; max-width:70%; line-height:1.5; box-shadow:0 4px 12px rgba(91,79,207,0.3); }
    .ai-msg-bot { display:flex; align-items:flex-start; gap:10px; }
    .ai-bot-avatar { width:30px; height:30px; border-radius:8px; background:linear-gradient(135deg,#1e1a3a,#3d3480); display:flex; align-items:center; justify-content:center; font-size:14px; flex-shrink:0; border:0.5px solid #3d3480; }
    .ai-msg-bot .bubble { background:#0d0f1a; border:0.5px solid #1e2235; color:#c8cde8; border-radius:4px 16px 16px 16px; padding:12px 16px; font-size:12px; max-width:80%; line-height:1.7; }
    .ai-section-title { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:.08em; margin-bottom:4px; }
    .ai-summary-label { color:#9d8ff5; }
    .ai-analysis-label { color:#60a5fa; }
    .ai-rec-label { color:#4ade80; }
    .ai-error { color:#f87171; font-size:12px; }
    .ai-welcome { background:#0d0f1a; border:0.5px solid #1e2235; border-radius:12px; padding:20px; text-align:center; margin-bottom:16px; }
    .ai-welcome-icon { font-size:32px; margin-bottom:10px; }
    .ai-welcome-title { font-size:15px; font-weight:600; color:#e0e4ff; margin-bottom:6px; }
    .ai-welcome-sub { font-size:12px; color:#6b7199; line-height:1.6; }
    .ai-chips { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; justify-content:center; }
    .ai-chip { background:#1a1d2e; border:0.5px solid #2a2f4a; border-radius:20px; padding:5px 12px; font-size:11px; color:#9d8ff5; cursor:pointer; transition:all 0.2s; }
    .ai-chip:hover { border-color:#5b4fcf; background:#1e1a3a; }
</style>

<div class="sidebar" id="custom-sidebar">
  <div class="sb-logo">B</div>
  <div class="sb-icon active" data-tab="0"><i class="ti ti-layout-dashboard"></i></div>
  <div class="sb-icon" data-tab="1"><i class="ti ti-chart-bar"></i></div>
  <div class="sb-icon" data-tab="2"><i class="ti ti-bulb"></i></div>
  <div class="sb-icon" data-tab="3"><i class="ti ti-table"></i></div>
  <div class="sb-div"></div>
  <div class="sb-icon" data-tab="4"><i class="ti ti-settings"></i></div>
  <div class="sb-div"></div>
  <div class="sb-icon" data-tab="5"><i class="ti ti-message-chatbot"></i></div>
</div>
""", unsafe_allow_html=True)

components.html("""
<script>
function initSidebar() {
    var doc = window.parent.document;
    var icons = doc.querySelectorAll('#custom-sidebar .sb-icon');
    icons.forEach(function(icon) {
        icon.onclick = function() {
            var idx = this.getAttribute('data-tab');
            if(idx !== null) {
                var tabs = doc.querySelectorAll('button[data-baseweb="tab"]');
                if (tabs && tabs.length > parseInt(idx)) {
                    tabs[parseInt(idx)].click();
                }
            }
        };
    });
}
function syncActiveTab() {
    var doc = window.parent.document;
    var icons = doc.querySelectorAll('#custom-sidebar .sb-icon');
    var tabs = doc.querySelectorAll('button[data-baseweb="tab"]');
    if(!icons.length || !tabs.length) return;
    var activeIndex = 0;
    tabs.forEach(function(tab, index) {
        if(tab.getAttribute('aria-selected') === 'true') {
            activeIndex = index;
        }
    });
    icons.forEach(function(icon) {
        var idx = icon.getAttribute('data-tab');
        if(idx !== null && parseInt(idx) === activeIndex) {
            if(!icon.classList.contains('active')) icon.classList.add('active');
        } else {
            icon.classList.remove('active');
        }
    });
}
setTimeout(initSidebar, 500);
setInterval(initSidebar, 2000);
setInterval(syncActiveTab, 300);
</script>
""", height=0)

# ---------------------------------------------------------
# CORE DATA LOGIC
# ---------------------------------------------------------
def clean_and_classify_data(df):
    report = {
        'initial_rows': len(df),
        'initial_cols': len(df.columns),
        'logs': [],
        'missing_pct': {},
        'col_types': {},
        'col_concepts': {}
    }
    
    unnamed_cols = [c for c in df.columns if 'Unnamed:' in str(c)]
    if len(unnamed_cols) >= len(df.columns) * 0.3:
        for i in range(min(5, len(df))):
            if df.iloc[i].notnull().sum() > len(df.columns) * 0.5:
                df.columns = df.iloc[i].fillna('Unnamed').astype(str)
                df = df.iloc[i+1:].reset_index(drop=True)
                report['logs'].append("✅ Fixed table headers")
                break
                
    for col in df.columns:
        if df[col].dtype == 'object': df[col] = df[col].ffill()
            
    df.columns = df.columns.astype(str).str.strip()
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)
    df = df.drop_duplicates()
    report['final_rows'] = len(df)
    
    for col in df.select_dtypes(['object']).columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
        
    for col in df.columns:
        report['missing_pct'][col] = df[col].isna().mean() * 100
        col_lower = str(col).lower()
        
        is_id_name = any(k in col_lower for k in ['id', 'code', 'no', 'number'])
        unique_ratio = df[col].nunique() / len(df) if len(df) > 0 else 0
        if is_id_name and unique_ratio > 0.9:
            report['col_types'][col] = 'ID'
            continue
            
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            report['col_types'][col] = 'DATE'
            df[f'{col}_Year'] = df[col].dt.year
            df[f'{col}_Month'] = df[col].dt.month_name()
            continue
            
        non_nulls = df[col].notna().sum()
        if non_nulls == 0:
            report['col_types'][col] = 'UNKNOWN'
            continue

        if df[col].dtype == 'object':
            date_parsed = pd.to_datetime(df[col], errors='coerce')
            if date_parsed.notna().sum() / non_nulls > 0.6:
                df[col] = date_parsed
                report['col_types'][col] = 'DATE'
                df[f'{col}_Year'] = df[col].dt.year
                df[f'{col}_Month'] = df[col].dt.month_name()
                continue
                
        if df[col].dtype == 'object':
            cleaned_col = df[col].astype(str).str.replace(r'[$,₹€£%,\s]', '', regex=True)
            num_parsed = pd.to_numeric(cleaned_col, errors='coerce')
            if num_parsed.notna().sum() / non_nulls > 0.7:
                df[col] = num_parsed
                report['col_types'][col] = 'NUMERIC'
                continue
        else:
            num_parsed = pd.to_numeric(df[col], errors='coerce')
            if num_parsed.notna().sum() / non_nulls > 0.7:
                df[col] = num_parsed
                report['col_types'][col] = 'NUMERIC'
                continue
            
        if df[col].dtype == 'object' or str(df[col].dtype) == 'category':
            num_unique = df[col].nunique()
            avg_len = df[col].astype(str).str.len().mean()
            if avg_len > 50: report['col_types'][col] = 'TEXT'
            elif num_unique < 50: report['col_types'][col] = 'CATEGORICAL'
            else: report['col_types'][col] = 'HIGH_CARDINALITY'
        else:
            report['col_types'][col] = 'UNKNOWN'

    for col in df.columns:
        if col not in report['col_types']: continue
        cl = str(col).lower()
        if any(k in cl for k in ['revenue', 'sales', 'amount', 'income', 'turnover']): report['col_concepts'][col] = 'Revenue'
        elif any(k in cl for k in ['profit', 'margin', 'net', 'earnings']): report['col_concepts'][col] = 'Profit'
        elif any(k in cl for k in ['cost', 'expense', 'spend', 'price', 'rate']): report['col_concepts'][col] = 'Cost'
        elif any(k in cl for k in ['quantity', 'units', 'volume']): report['col_concepts'][col] = 'Quantity'
        elif any(k in cl for k in ['date', 'time', 'month', 'year']): report['col_concepts'][col] = 'Date'
        elif any(k in cl for k in ['name', 'product', 'category', 'type', 'region']): report['col_concepts'][col] = 'Category'
        else: report['col_concepts'][col] = 'Other'

    for col, ctype in report['col_types'].items():
        if ctype == 'NUMERIC':
            q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            outliers = df[(df[col] < (q1 - 1.5*(q3-q1))) | (df[col] > (q3 + 1.5*(q3-q1)))]
            if len(outliers) > 0: report['logs'].append(f"⚠️ {len(outliers)} outliers in '{col}'")

    return df, report

def detect_dataset_type(report):
    concepts = list(report['col_concepts'].values())
    types = list(report['col_types'].values())
    
    has_date = 'DATE' in types or 'Date' in concepts
    has_rev = 'Revenue' in concepts
    has_cat = 'CATEGORICAL' in types or 'Category' in concepts
    has_cost = 'Cost' in concepts
    has_qty = 'Quantity' in concepts
    
    if has_date and has_rev and has_cat: return "Sales Dataset"
    elif has_cost and 'Person' in concepts: return "HR/Payroll Dataset"
    elif has_qty and has_cat: return "Inventory Dataset"
    else: return "General Dataset"

def get_kpi_icon(concept):
    if concept == 'Revenue': return 'p', 'ti-coin'
    elif concept == 'Profit': return 'g', 'ti-trending-up'
    elif concept == 'Quantity': return 'b', 'ti-box'
    elif concept == 'Cost': return 'o', 'ti-cash'
    return 'p', 'ti-chart-bar'

# ---------------------------------------------------------
# AI BUSINESS ASSISTANT ENGINE
# ---------------------------------------------------------
def ai_business_assistant(question, df, report, ds_type):
    """Smart data-driven Q&A engine for business analytics."""
    q = question.lower().strip()
    num_cols = [c for c, t in report['col_types'].items() if t == 'NUMERIC']
    cat_cols = [c for c, t in report['col_types'].items() if t == 'CATEGORICAL']
    date_cols = [c for c, t in report['col_types'].items() if t == 'DATE']

    # Off-topic guard
    business_keywords = [
        'revenue','profit','sales','customer','product','region','growth','forecast',
        'total','average','max','min','top','bottom','highest','lowest','best','worst',
        'trend','performance','cost','quantity','amount','value','count','sum','mean',
        'column','row','data','dataset','analyze','analysis','compare','distribution',
        'anomaly','outlier','missing','quality','category','breakdown','report'
    ]
    if not any(k in q for k in business_keywords) and len(q) > 10:
        return {
            'type': 'off_topic',
            'summary': 'I cannot answer that question.',
            'analysis': 'I am a Business Analytics Assistant trained only on your uploaded dataset. I can only answer questions about revenue, profit, sales, customers, products, regions, growth, and business performance.',
            'recommendation': 'Please ask a business or data-related question about your uploaded file.'
        }

    # ---- FIND MOST RELEVANT NUMERIC COLUMN ----
    def find_col(keywords):
        for kw in keywords:
            for c in num_cols:
                if kw in c.lower(): return c
        return num_cols[0] if num_cols else None

    revenue_col = find_col(['revenue','sales','amount','value','income','turnover','price'])
    profit_col  = find_col(['profit','margin','net','earning','gain'])
    cost_col    = find_col(['cost','expense','spending'])
    qty_col     = find_col(['quantity','qty','unit','volume','count'])

    # ---- TOTAL / SUM ----
    if any(k in q for k in ['total','sum','overall','aggregate']):
        results = []
        for c in num_cols[:5]:
            results.append(f"• **{c}**: {df[c].sum():,.2f}")
        return {
            'summary': f"Total figures for all numeric columns in the dataset ({report['final_rows']} rows).",
            'analysis': 'Totals across all numeric columns:\n' + '\n'.join(results),
            'recommendation': f"Focus on maximizing the highest-value metric. The top metric is **{num_cols[0]}** with a total of **{df[num_cols[0]].sum():,.2f}**."
        }

    # ---- REVENUE ----
    if any(k in q for k in ['revenue','income','turnover','earnings']):
        if revenue_col:
            total = df[revenue_col].sum()
            avg   = df[revenue_col].mean()
            mx    = df[revenue_col].max()
            mn    = df[revenue_col].min()
            top_cat = ''
            if cat_cols:
                grp = df.groupby(cat_cols[0])[revenue_col].sum().sort_values(ascending=False)
                top_cat = f"\n• Top {cat_cols[0]}: **{grp.index[0]}** with {grp.iloc[0]:,.2f} ({(grp.iloc[0]/total*100):.1f}%)"
            return {
                'summary': f"Total {revenue_col}: **{total:,.2f}** across {report['final_rows']} records.",
                'analysis': f"Revenue Analysis for **{revenue_col}**:\n• Total: {total:,.2f}\n• Average per record: {avg:,.2f}\n• Highest single value: {mx:,.2f}\n• Lowest single value: {mn:,.2f}{top_cat}",
                'recommendation': f"Average revenue per record is {avg:,.2f}. Records below this average may need attention. Consider investigating the bottom performers to improve overall revenue."
            }
        return {'type':'not_found','summary':'Revenue column not identified.','analysis':'No revenue, sales, or amount column detected in the dataset.','recommendation':'Ensure your data has a column labeled Revenue, Sales, or Amount.'}

    # ---- PROFIT ----
    if any(k in q for k in ['profit','margin','net','earning']):
        col = profit_col or revenue_col
        if col:
            total = df[col].sum()
            avg   = df[col].mean()
            neg_count = (df[col] < 0).sum()
            return {
                'summary': f"Profit/Margin column: **{col}** | Total: **{total:,.2f}**",
                'analysis': f"Profit Analysis:\n• Total: {total:,.2f}\n• Average: {avg:,.2f}\n• Records with negative values (losses): **{neg_count}**\n• Records with positive values (gains): {report['final_rows']-neg_count}",
                'recommendation': f"{'⚠️ There are ' + str(neg_count) + ' loss-making records. Investigate and reduce these.' if neg_count > 0 else '✅ All records show positive profit. Maintain current strategy and seek growth opportunities.'}"
            }

    # ---- TOP / BEST / HIGHEST ----
    if any(k in q for k in ['top','best','highest','most','leading','maximum','max']):
        col = revenue_col or (num_cols[0] if num_cols else None)
        if col and cat_cols:
            grp = df.groupby(cat_cols[0])[col].sum().sort_values(ascending=False).head(5)
            rows = '\n'.join([f"• {i+1}. **{k}**: {v:,.2f}" for i,(k,v) in enumerate(grp.items())])
            return {
                'summary': f"Top 5 {cat_cols[0]}s by {col}.",
                'analysis': f"Top performers by **{col}**:\n{rows}",
                'recommendation': f"**{grp.index[0]}** is the top performer. Replicate its success strategy across other {cat_cols[0]}s to drive overall growth."
            }
        elif col:
            top = df.nlargest(5, col)[col]
            rows = '\n'.join([f"• Row {i}: **{v:,.2f}**" for i,v in top.items()])
            return {'summary': f"Top 5 values in {col}.", 'analysis': rows, 'recommendation': 'Investigate what drives these top-performing records.'}

    # ---- BOTTOM / WORST / LOWEST ----
    if any(k in q for k in ['bottom','worst','lowest','least','minimum','min','poor']):
        col = revenue_col or (num_cols[0] if num_cols else None)
        if col and cat_cols:
            grp = df.groupby(cat_cols[0])[col].sum().sort_values().head(5)
            rows = '\n'.join([f"• {i+1}. **{k}**: {v:,.2f}" for i,(k,v) in enumerate(grp.items())])
            return {
                'summary': f"Bottom 5 {cat_cols[0]}s by {col}.",
                'analysis': f"Lowest performers by **{col}**:\n{rows}",
                'recommendation': f"**{grp.index[0]}** is the lowest performer. Conduct a root-cause analysis and consider targeted improvement plans or resource reallocation."
            }

    # ---- AVERAGE ----
    if any(k in q for k in ['average','mean','avg']):
        col = revenue_col or (num_cols[0] if num_cols else None)
        if col:
            avg  = df[col].mean()
            med  = df[col].median()
            std  = df[col].std()
            return {
                'summary': f"Average {col}: **{avg:,.2f}**",
                'analysis': f"Statistical Summary for **{col}**:\n• Mean (Average): {avg:,.2f}\n• Median: {med:,.2f}\n• Std Deviation: {std:,.2f}\n• Min: {df[col].min():,.2f}\n• Max: {df[col].max():,.2f}",
                'recommendation': f"{'The median (' + f"{med:,.2f}" + ') is lower than the mean (' + f"{avg:,.2f}" + '), indicating a skew from high-value outliers. Focus on raising the median.' if med < avg else 'The distribution is fairly balanced. Focus on consistent growth.'}"
            }

    # ---- GROWTH / TREND ----
    if any(k in q for k in ['growth','trend','over time','month','year','period','forecast']):
        col = revenue_col or (num_cols[0] if num_cols else None)
        if date_cols and col:
            date_c = date_cols[0]
            try:
                df['_dt'] = pd.to_datetime(df[date_c], errors='coerce')
                df['_yr'] = df['_dt'].dt.year
                grp = df.groupby('_yr')[col].sum().sort_index()
                if len(grp) > 1:
                    growth = ((grp.iloc[-1] - grp.iloc[0]) / grp.iloc[0] * 100)
                    rows = '\n'.join([f"• {yr}: {v:,.2f}" for yr,v in grp.items()])
                    return {
                        'summary': f"Overall growth in {col}: **{growth:+.1f}%** from {grp.index[0]} to {grp.index[-1]}.",
                        'analysis': f"Year-over-year **{col}** trend:\n{rows}",
                        'recommendation': f"{'📈 Positive growth trend. Invest in scaling top-performing channels.' if growth > 0 else '📉 Declining trend detected. Immediate review of strategy required.'}"
                    }
            except: pass
        return {'summary': 'Trend analysis requires a date column.', 'analysis': f"{'Date column found: ' + ', '.join(date_cols) if date_cols else 'No date column detected in the dataset.'}",'recommendation': 'Ensure your data has a Date, Month, or Year column for trend analysis.'}

    # ---- ANOMALY / OUTLIER ----
    if any(k in q for k in ['anomaly','outlier','unusual','spike','drop','abnormal']):
        col = revenue_col or (num_cols[0] if num_cols else None)
        if col:
            mean, std = df[col].mean(), df[col].std()
            outliers = df[np.abs(df[col] - mean) > 2.5 * std]
            return {
                'summary': f"Found **{len(outliers)}** anomalies in {col} (values beyond 2.5 standard deviations).",
                'analysis': f"Anomaly Detection on **{col}**:\n• Normal range: {mean - 2.5*std:,.2f} to {mean + 2.5*std:,.2f}\n• Outliers detected: **{len(outliers)}** records\n• Outlier values range: {outliers[col].min():,.2f} to {outliers[col].max():,.2f}" if len(outliers) > 0 else f"No significant anomalies found in {col}. Data appears consistent.",
                'recommendation': 'Investigate the flagged anomaly records to determine if they represent data errors or genuine business spikes/drops that need attention.'
            }

    # ---- CUSTOMERS ----
    if any(k in q for k in ['customer','client','buyer','purchaser']):
        cust_col = next((c for c in cat_cols if any(k in c.lower() for k in ['customer','client','name','buyer'])), cat_cols[0] if cat_cols else None)
        if cust_col:
            total_customers = df[cust_col].nunique()
            top_cust = df.groupby(cust_col)[revenue_col].sum().sort_values(ascending=False).head(3) if revenue_col else None
            top_text = ''
            if top_cust is not None:
                top_text = '\n' + '\n'.join([f"• {k}: {v:,.2f}" for k,v in top_cust.items()])
            return {
                'summary': f"Total unique {cust_col}s: **{total_customers}**",
                'analysis': f"Customer Analysis:\n• Unique {cust_col}s: {total_customers}\n• Total records: {report['final_rows']}{('\n\nTop 3 customers by revenue:' + top_text) if top_text else ''}",
                'recommendation': 'Apply Pareto analysis (80/20 rule): focus retention efforts on top customers who likely drive the majority of revenue.'
            }

    # ---- PRODUCT ----
    if any(k in q for k in ['product','item','sku','goods','service']):
        prod_col = next((c for c in cat_cols if any(k in c.lower() for k in ['product','item','sku','name','category'])), cat_cols[0] if cat_cols else None)
        if prod_col:
            total_products = df[prod_col].nunique()
            col = revenue_col or (num_cols[0] if num_cols else None)
            top_prod = df.groupby(prod_col)[col].sum().sort_values(ascending=False).head(5) if col else None
            top_text = '\n'.join([f"• {k}: {v:,.2f}" for k,v in top_prod.items()]) if top_prod is not None else ''
            return {
                'summary': f"Total unique {prod_col}s: **{total_products}**",
                'analysis': f"Product Analysis:\n• Unique products: {total_products}\n• Top 5 products by {col}:\n{top_text}",
                'recommendation': f"**{top_prod.index[0]}** is the star product. Consider expanding its variants, increasing stock, or using it as an anchor for upselling."
            }

    # ---- DATA OVERVIEW / COLUMNS ----
    if any(k in q for k in ['column','data','dataset','overview','summary','describe','what','how many','rows','columns']):
        col_summary = ', '.join([f"{c} ({t})" for c,t in list(report['col_types'].items())[:10]])
        return {
            'summary': f"Dataset: **{ds_type}** | {report['final_rows']} rows × {report['initial_cols']} columns",
            'analysis': f"Dataset Overview:\n• Type: {ds_type}\n• Rows: {report['final_rows']}\n• Columns: {report['initial_cols']}\n• Numeric columns ({len(num_cols)}): {', '.join(num_cols[:5]) or 'None'}\n• Categorical columns ({len(cat_cols)}): {', '.join(cat_cols[:5]) or 'None'}\n• Date columns ({len(date_cols)}): {', '.join(date_cols[:3]) or 'None'}\n\nColumn types: {col_summary}",
            'recommendation': 'Use the Overview tab for KPIs, Charts tab for visuals, and Insights tab for automated findings.'
        }

    # ---- REGION ----
    if any(k in q for k in ['region','area','territory','location','city','country','state','zone']):
        region_col = next((c for c in cat_cols if any(k in c.lower() for k in ['region','area','territory','location','city','country','state','zone'])), None)
        col = revenue_col or (num_cols[0] if num_cols else None)
        if region_col and col:
            grp = df.groupby(region_col)[col].sum().sort_values(ascending=False)
            rows = '\n'.join([f"• {k}: {v:,.2f} ({(v/grp.sum()*100):.1f}%)" for k,v in grp.items()])
            return {
                'summary': f"Regional breakdown by {col} across {grp.shape[0]} {region_col}s.",
                'analysis': f"Regional Performance:\n{rows}",
                'recommendation': f"**{grp.index[0]}** is the top region. Consider allocating more resources there. Investigate underperforming regions for improvement opportunities."
            }
        return {'summary': 'No region column detected.', 'analysis': 'Could not find a region, area, or territory column in the dataset.', 'recommendation': 'Ensure your data includes a geographic column for regional analysis.'}

    # ---- GENERIC FALLBACK (still data-driven) ----
    col = num_cols[0] if num_cols else None
    if col:
        total = df[col].sum()
        avg   = df[col].mean()
        return {
            'summary': f"General analysis of **{col}**: Total = {total:,.2f}, Average = {avg:,.2f}",
            'analysis': f"Here is what I found in your {ds_type} dataset ({report['final_rows']} rows):\n• Primary metric **{col}**: Total {total:,.2f} | Avg {avg:,.2f} | Max {df[col].max():,.2f} | Min {df[col].min():,.2f}\n\nAvailable columns: {', '.join(list(report['col_types'].keys())[:8])}",
            'recommendation': 'Try asking more specific questions like: "What is the total revenue?", "Who are the top customers?", or "Show me the product breakdown."'
        }
    return {
        'summary': 'I cannot find that information in the uploaded dataset.',
        'analysis': 'The question could not be matched to any column or metric in your data.',
        'recommendation': 'Try rephrasing your question using column names from your dataset.'
    }


# ---------------------------------------------------------
# UI RENDERING
# ---------------------------------------------------------
def main():
    st.markdown('<div style="margin-top: 50px;"></div>', unsafe_allow_html=True)
    
    hero_container = st.empty()
    
    if not st.session_state.get('_uploaded_file_present', False):
        st.markdown("""
        <div class="topbar">
            <div style="display:flex;align-items:center;gap:10px">
              <span class="topbar-title">BusinessMind AI</span>
              <span class="badge badge-purple">Universal Analyzer</span>
              <span class="badge badge-green">● Ready</span>
            </div>
            <div class="topbar-right"><div class="avatar">BM</div></div>
        </div>
        """, unsafe_allow_html=True)
        
        with hero_container.container():
            st.markdown("""
            <style>
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes float {
                    0% { transform: translateY(0px); }
                    50% { transform: translateY(-8px); }
                    100% { transform: translateY(0px); }
                }
                @keyframes gradientBG {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }

                .hero-section {
                    text-align: center;
                    margin-top: 20px;
                    margin-bottom: 30px;
                }
                .hero-title {
                    font-size: 52px;
                    font-weight: 700;
                    color: #e0e4ff;
                    margin-bottom: 16px;
                    letter-spacing: -0.02em;
                    opacity: 0;
                    animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                }
                .hero-accent {
                    background: linear-gradient(270deg, #5b4fcf, #c084fc, #5b4fcf);
                    background-size: 200% 200%;
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    animation: gradientBG 4s ease infinite;
                }
                .hero-subtitle {
                    font-size: 16px;
                    color: #6b7199;
                    max-width: 600px;
                    margin: 0 auto;
                    line-height: 1.6;
                    opacity: 0;
                    animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.15s forwards;
                }
                .hero-cards-wrapper {
                    display: flex;
                    gap: 16px;
                    margin-top: 40px;
                    opacity: 0;
                    animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards;
                }
                .hero-card {
                    flex: 1;
                    background: #0d0f1a;
                    border: 0.5px solid #1e2235;
                    border-radius: 16px;
                    padding: 30px 20px;
                    text-align: center;
                    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                    position: relative;
                    overflow: hidden;
                }
                .hero-card::before {
                    content: '';
                    position: absolute;
                    top: 0; left: 0; right: 0; height: 1px;
                    background: linear-gradient(90deg, transparent, rgba(91, 79, 207, 0.5), transparent);
                    opacity: 0;
                    transition: opacity 0.4s ease;
                }
                .hero-card:hover {
                    border-color: #3d3480;
                    transform: translateY(-6px);
                    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
                }
                .hero-card:hover::before {
                    opacity: 1;
                }
                .hero-card-icon {
                    width: 56px;
                    height: 56px;
                    border-radius: 14px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 28px;
                    margin: 0 auto 20px;
                    animation: float 4s ease-in-out infinite;
                }
                .icon-p { background: #1e1a3a; color: #9d8ff5; animation-delay: 0s; }
                .icon-g { background: #0f1f16; color: #4ade80; animation-delay: 0.5s; }
                .icon-b { background: #0a1525; color: #60a5fa; animation-delay: 1s; }
            </style>
            
            <div class="hero-section">
                <div class="hero-title">
                    Turn Raw Data Into <br>
                    <span class="hero-accent">Instant Intelligence</span>
                </div>
                <div class="hero-subtitle">
                    Upload any Excel file and our Universal Analyzer will automatically clean, classify, and generate a comprehensive CEO dashboard in seconds.
                </div>
                

            </div>
            
            <div class="upload-zone" style="margin-top:20px; animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.45s forwards; opacity: 0; position:relative; min-height: 130px;">
                <div class="upload-icon" style="animation: float 4s ease-in-out 1.5s infinite;"><i class="ti ti-cloud-upload"></i></div>
                <div class="upload-title">Drag &amp; Drop your Excel file here</div>
                <div class="upload-sub">We support .xlsx and .xls up to 200MB</div>
                <div class="upload-sub" style="margin-top:6px; color: #2a2f4a;">— or click to browse —</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Place the actual Streamlit uploader — it will be made invisible by CSS
        # and positioned as a transparent overlay on the upload zone above
        uploaded_file = st.file_uploader("", type=["xlsx", "xls"], label_visibility="collapsed")
        if uploaded_file:
            st.session_state['_uploaded_file_present'] = True
            st.session_state['_uploaded_file'] = uploaded_file
            st.rerun()
        return
    else:
        uploaded_file = st.session_state.get('_uploaded_file', None)
        if uploaded_file is None:
            st.session_state['_uploaded_file_present'] = False
            st.rerun()
            return

    # Show a reset button in topbar area
    col_reset, _ = st.columns([1, 8])
    with col_reset:
        if st.button("↩ Upload New File", key="reset_btn", help="Upload a different file"):
            st.session_state['_uploaded_file_present'] = False
            st.session_state['_uploaded_file'] = None
            st.rerun()

    with st.spinner("🤖 Analyzing your data..."):
        try:
            engine = 'openpyxl' if uploaded_file.name.endswith('xlsx') else 'xlrd'
            raw_df = pd.read_excel(uploaded_file, engine=engine)
            if raw_df.empty: st.stop()
                
            df, report = clean_and_classify_data(raw_df)
            ds_type = detect_dataset_type(report)
            quality_score = 100 - (sum(report['missing_pct'].values()) / len(report['missing_pct'])) if report['missing_pct'] else 100
            
            # Topbar dynamically updated
            st.markdown(f"""
            <div class="topbar">
                <div style="display:flex;align-items:center;gap:10px">
                  <span class="topbar-title">BusinessMind AI</span>
                  <span class="badge badge-purple">Universal Analyzer</span>
                  <span class="badge badge-green">● Live</span>
                </div>
                <div class="topbar-right">
                  <span class="badge badge-amber">{ds_type} · {report['final_rows']} rows</span>
                  <div class="avatar">BM</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Upload Status Bar
            num_c = list(report['col_types'].values()).count('NUMERIC')
            date_c = list(report['col_types'].values()).count('DATE')
            cat_c = list(report['col_types'].values()).count('CATEGORICAL')
            
            st.markdown(f"""
            <div class="upload-zone" style="padding:14px;margin-bottom:14px;border:0.5px solid #1e2235;border-style:solid;">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="upload-icon" style="width:32px;height:32px;font-size:15px;margin:0"><i class="ti ti-circle-check"></i></div>
                <div style="text-align:left">
                  <div class="upload-title" style="font-size:12px">{uploaded_file.name} · uploaded</div>
                  <div class="upload-sub">{report['final_rows']} rows · {len(df.columns)} columns · {int(quality_score)}% quality</div>
                </div>
                <div style="margin-left:auto;display:flex;gap:6px">
                  <span class="badge badge-purple">🔢 {num_c} numeric</span>
                  <span class="badge badge-green">📅 {date_c} date</span>
                  <span class="badge" style="background:#1a1520;color:#c084fc;border:0.5px solid #4a2880">🏷️ {cat_c} category</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabs
            t1, t2, t3, t4, t5, t6 = st.tabs(["Overview", "Charts", "Insights", "Data Quality", "Export", "🤖 AI Assistant"])
            
            num_cols = [c for c, t in report['col_types'].items() if t == 'NUMERIC']
            cat_cols = [c for c, t in report['col_types'].items() if t == 'CATEGORICAL']
            date_cols = [c for c, t in report['col_types'].items() if t == 'DATE']
            
            with t1:
                st.markdown('<div class="section-label">Key Metrics</div>', unsafe_allow_html=True)
                cols = st.columns(4)
                for i, col in enumerate(num_cols[:4]):
                    with cols[i % 4]:
                        concept = report['col_concepts'].get(col, 'Other')
                        ic, i_glyph = get_kpi_icon(concept)
                        val = df[col].sum()
                        avg = df[col].mean()
                        st.markdown(f"""
                        <div class="kpi">
                            <div class="kpi-top">
                              <span class="kpi-label">{col}</span>
                              <div class="kpi-icon {ic}"><i class="{i_glyph}"></i></div>
                            </div>
                            <div class="kpi-val">{val:,.0f}</div>
                            <div class="kpi-change">Avg: {avg:,.1f}</div>
                        </div>
                        """, unsafe_allow_html=True)

            with t2:
                st.markdown('<div class="section-label">Visualizations</div>', unsafe_allow_html=True)
                def config_fig(fig):
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0d0f1a", font_color="#6b7199", margin=dict(l=8, r=8, t=36, b=8), title_font=dict(size=11, color="#6b7199"))
                    fig.update_xaxes(gridcolor="#1e2235", linecolor="#1e2235")
                    fig.update_yaxes(gridcolor="#1e2235", linecolor="#1e2235")
                    return fig

                cc1, cc2 = st.columns(2)
                with cc1:
                    if cat_cols and num_cols:
                        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                        agg = df.groupby(cat_cols[0])[num_cols[0]].sum().nlargest(5).sort_values()
                        fig = go.Figure(go.Bar(x=agg.values, y=agg.index, orientation='h', marker_color=["#3d3480"]*2 + ["#5b4fcf"]*3))
                        fig.update_layout(title=f"Top 5 {cat_cols[0]} by {num_cols[0]}")
                        st.plotly_chart(config_fig(fig), use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                with cc2:
                    if date_cols and num_cols:
                        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                        monthly = df.groupby(pd.Grouper(key=date_cols[0], freq='ME'))[num_cols[0]].sum().reset_index()
                        fig = px.line(monthly, x=date_cols[0], y=num_cols[0], title=f"{num_cols[0]} Trend")
                        fig.update_traces(line_color="#5b4fcf", fill='tozeroy', fillcolor="rgba(91, 79, 207, 0.08)")
                        st.plotly_chart(config_fig(fig), use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

            with t3:
                st.markdown('<div class="section-label">Auto-generated insights</div>', unsafe_allow_html=True)
                ic1, ic2 = st.columns(2)
                dots = ["#9d8ff5", "#4ade80", "#60a5fa", "#fbbf24"]
                idx = 0
                
                if date_cols and num_cols:
                    best_m = df.groupby(df[date_cols[0]].dt.month_name())[num_cols[0]].sum().idxmax()
                    with (ic1 if idx%2==0 else ic2):
                        st.markdown(f'<div class="insight"><div class="ins-dot" style="background:{dots[idx%4]}"></div><div><div class="ins-text">Peak month was <span class="ins-val">{best_m}</span> for {num_cols[0]}</div></div></div>', unsafe_allow_html=True)
                        idx+=1
                if cat_cols and num_cols:
                    tc = df.groupby(cat_cols[0])[num_cols[0]].sum().idxmax()
                    with (ic1 if idx%2==0 else ic2):
                        st.markdown(f'<div class="insight"><div class="ins-dot" style="background:{dots[idx%4]}"></div><div><div class="ins-text">Top {cat_cols[0]} is <span class="ins-val">{tc}</span> leading the overall volume.</div></div></div>', unsafe_allow_html=True)
                        idx+=1
                if len(num_cols) >= 2:
                    corr = df[num_cols[0]].corr(df[num_cols[1]])
                    with (ic1 if idx%2==0 else ic2):
                        st.markdown(f'<div class="insight"><div class="ins-dot" style="background:{dots[idx%4]}"></div><div><div class="ins-text">Correlation of <span class="ins-val">{corr:.2f}</span> between {num_cols[0]} and {num_cols[1]}.</div></div></div>', unsafe_allow_html=True)

                # ── CEO DASHBOARD VERDICT ──────────────────────────────
                st.markdown('<div class="section-label" style="margin-top:24px;">CEO Dashboard Verdict</div>', unsafe_allow_html=True)

                # ── Compute Business Health Score ──
                score = 0
                score += 2 if quality_score >= 90 else (1 if quality_score >= 70 else 0)
                score += 2 if len(num_cols) >= 3 else (1 if len(num_cols) >= 1 else 0)
                score += 1 if len(cat_cols) >= 2 else 0
                score += 1 if len(date_cols) >= 1 else 0
                score += 2 if report['final_rows'] >= 100 else (1 if report['final_rows'] >= 20 else 0)
                score += 1 if len(num_cols) >= 1 and df[num_cols[0]].std() / (df[num_cols[0]].mean() + 1e-9) < 1.5 else 0
                score += 1 if len(num_cols) >= 2 and abs(df[num_cols[0]].corr(df[num_cols[1]])) > 0.3 else 0
                score = min(score, 10)
                score_color = "#4ade80" if score >= 7 else ("#fbbf24" if score >= 5 else "#f87171")
                score_label = "Strong" if score >= 7 else ("Moderate" if score >= 5 else "Needs Attention")

                # ── Dynamic narrative builders ──
                primary_col = num_cols[0] if num_cols else None
                total_val   = df[primary_col].sum()   if primary_col else 0
                avg_val     = df[primary_col].mean()  if primary_col else 0
                max_val     = df[primary_col].max()   if primary_col else 0
                min_val     = df[primary_col].min()   if primary_col else 0
                std_val     = df[primary_col].std()   if primary_col else 0
                top_cat_str = ""
                bot_cat_str = ""
                neg_count   = 0
                if cat_cols and primary_col:
                    grp = df.groupby(cat_cols[0])[primary_col].sum().sort_values(ascending=False)
                    top_cat_str = f"{grp.index[0]} ({grp.iloc[0]:,.0f})"
                    bot_cat_str = f"{grp.index[-1]} ({grp.iloc[-1]:,.0f})"
                if primary_col:
                    neg_count = int((df[primary_col] < 0).sum())

                import html as _html
                import re as _re

                def safe(val):
                    """HTML-escape a dynamic value and strip whitespace."""
                    return _html.escape(str(val).strip())

                def bold(val):
                    """Wrap a value in HTML bold tags after escaping."""
                    return f"<strong>{safe(val)}</strong>"

                def md_bold(text):
                    """Convert **markdown bold** to HTML strong tags (multiline safe)."""
                    return _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text, flags=_re.DOTALL)

                # Safe aliases for display
                pc   = safe(primary_col) if primary_col else "primary metric"
                tc   = safe(top_cat_str)
                bc   = safe(bot_cat_str)
                cc0  = safe(cat_cols[0]) if cat_cols else "category"

                strengths_text = (
                    f"Your dataset demonstrates solid business fundamentals across "
                    f"{bold(report['final_rows'])} records and {bold(report['initial_cols'])} data dimensions, "
                    f"achieving a data quality score of {bold(str(int(quality_score)) + '%')}. "
                    f"The primary metric {bold(pc)} shows a healthy total of {bold(f'{total_val:,.0f}')} "
                    f"with an average of {bold(f'{avg_val:,.1f}')} per record. "
                    + (f"{bold(tc)} leads as the top-performing {cc0}, demonstrating strong category concentration and a clear market leader. " if top_cat_str else "")
                    + (f"With {bold(len(num_cols))} numeric and {bold(len(cat_cols))} categorical dimensions available, the dataset supports multi-dimensional analysis. " if len(num_cols) > 1 else "")
                    + ("Temporal data is available, enabling trend and seasonality analysis. " if date_cols else "")
                    + "Overall, the business data is well-structured and analytically rich, supporting strategic decision-making."
                )

                ai_recs_text = (
                    f"Based on the data profile, the following AI-driven recommendations are prioritized: "
                    f"<strong>First</strong>, with an average {pc} of {bold(f'{avg_val:,.1f}')}, focus resources on records "
                    f"and segments performing below this benchmark to uplift laggards. "
                    + (f"<strong>Second</strong>, {bold(bc)} is the weakest {cc0} — a targeted intervention plan, pricing review, or demand-generation campaign should be initiated immediately. " if bot_cat_str else "")
                    + (f"<strong>Third</strong>, the {bold(len(date_cols))} date dimension(s) in the data suggest time-based segmentation is possible — deploy monthly cohort tracking to identify seasonality and plan inventory or staffing accordingly. " if date_cols else "<strong>Third</strong>, enrich the dataset with date fields to unlock time-series forecasting capabilities. ")
                    + f"<strong>Fourth</strong>, leverage the correlation between top numeric metrics to build predictive models for demand forecasting. "
                    f"Data completeness at {bold(str(int(quality_score)) + '%')} is "
                    f"{'sufficient for reliable analysis and modelling' if quality_score > 80 else 'improvable — fill missing values to increase model accuracy'}."
                )

                missing_pct = int(100 - quality_score)
                if quality_score >= 99:
                    data_gap_action = "<strong>1. Data Integrity Confirmed</strong> — Your dataset has zero missing values (100% complete). This is excellent. Maintain this standard by enforcing data entry validations at source systems to preserve long-term data integrity. "
                elif missing_pct > 0:
                    data_gap_action = f"<strong>1. Address Data Gaps</strong> — With {bold(str(missing_pct) + '%')} missing data, prioritize filling or flagging incomplete records, especially in high-value columns to prevent skewed reporting. "
                else:
                    data_gap_action = "<strong>1. Data Quality Verified</strong> — Data quality is strong. Continue monitoring for drift or inconsistencies as new records are added. "

                immediate_text = (
                    "The following actions should be executed within the next 30 days: "
                    + data_gap_action
                    + (f"<strong>2. Rescue Bottom Performer</strong> — {bold(bc)} is critically underperforming. Assign a dedicated review team to diagnose the root cause — whether pricing, distribution, or market fit. " if bot_cat_str else "")
                    + (f"<strong>3. Fix Loss-Making Records</strong> — {bold(neg_count)} records show negative {pc}. Conduct a line-by-line audit to eliminate returns, discounts, or write-offs dragging overall performance. " if neg_count > 0 else f"<strong>3. Sustain Positive Performance</strong> — All {pc} records are positive. Introduce tiered incentive programs and performance bonuses to sustain and accelerate this momentum. ")
                    + f"<strong>4. Standardize Reporting</strong> — Establish a weekly CEO dashboard review cadence using this dataset to track {pc} trends and category shifts in near-real-time."
                )

                growth_text = (
                    "The dataset reveals several high-potential growth opportunities: "
                    + (f"<strong>1. Scale Top Performer</strong> — {bold(tc)} is the star segment. Increasing investment, marketing spend, or operational capacity in this area can yield disproportionate returns with relatively low incremental risk. " if top_cat_str else "")
                    + (f"<strong>2. Unlock Seasonality</strong> — With date data available, identify peak periods and pre-position supply chains, promotions, and headcount to capture demand surges before competitors. " if date_cols else "<strong>2. Add Time Dimension</strong> — Integrating date fields will unlock forecasting, seasonality, and growth-rate tracking — a critical upgrade for strategic planning. ")
                    + f"<strong>3. Cross-Sell &amp; Upsell</strong> — The {bold(len(cat_cols))} categorical segment(s) offer natural bundling opportunities. Analyse which {cc0} combinations co-occur most frequently and design bundle offers to increase average transaction value. "
                    + f"<strong>4. Predictive Expansion</strong> — With {bold(report['final_rows'])} records and {bold(len(num_cols))} numeric dimensions, a machine learning model can predict future {pc} with reasonable accuracy — enabling proactive rather than reactive business strategy."
                )

                # ── CSS + score card header (no dynamic text here) ──
                st.markdown("""
                <style>
                    .verdict-card {background:#0d0f1a;border:0.5px solid #1e2235;border-radius:14px;padding:20px 22px;margin-bottom:14px;}
                    .verdict-score-row {display:flex;align-items:center;gap:16px;margin-bottom:18px;}
                    .verdict-score-circle {border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;flex-shrink:0;background:rgba(0,0,0,0.3);}
                    .verdict-score-num {font-size:22px;font-weight:700;line-height:1;}
                    .verdict-score-denom {font-size:10px;color:#3a3f5c;}
                    .verdict-score-label {font-size:13px;font-weight:600;}
                    .verdict-score-sub {font-size:11px;color:#6b7199;margin-top:2px;}
                    .verdict-section {margin-bottom:16px;}
                    .verdict-section-hdr {display:flex;align-items:center;gap:8px;margin-bottom:8px;}
                    .verdict-section-icon {width:28px;height:28px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
                    .verdict-section-title {font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;}
                    .verdict-body {font-size:12.5px;color:#8b91b5;line-height:1.8;}
                    .verdict-body strong {color:#d0d5f5;font-weight:600;}
                    .verdict-divider {height:0.5px;background:#1e2235;margin:14px 0;}
                </style>
                <div class="verdict-card">
                """, unsafe_allow_html=True)

                # Score row — use safe string concat, not f-string for HTML wrapper
                score_html = (
                    '<div class="verdict-score-row">'
                    '<div class="verdict-score-circle" style="width:72px;height:72px;border:3px solid ' + score_color + ';">'
                    '<div class="verdict-score-num" style="color:' + score_color + ';">' + str(score) + '</div>'
                    '<div class="verdict-score-denom">/10</div>'
                    '</div>'
                    '<div>'
                    '<div class="verdict-score-label" style="color:' + score_color + ';">Business Health Score: ' + score_label + '</div>'
                    '<div class="verdict-score-sub">Evaluated across data quality, metric depth, category richness &amp; record volume</div>'
                    '</div></div>'
                )
                st.markdown(score_html, unsafe_allow_html=True)

                def render_section(icon, title, color, body_html):
                    """Render one verdict section cleanly without f-string nesting."""
                    html = (
                        '<div class="verdict-section">'
                        '<div class="verdict-section-hdr">'
                        '<div class="verdict-section-icon" style="background:' + color[0] + ';color:' + color[1] + ';">' + icon + '</div>'
                        '<div class="verdict-section-title" style="color:' + color[1] + ';">' + title + '</div>'
                        '</div>'
                        '<div class="verdict-body">' + body_html + '</div>'
                        '</div>'
                    )
                    st.markdown(html, unsafe_allow_html=True)

                render_section("💪", "Strengths", ("#1e1a3a", "#9d8ff5"), strengths_text)
                st.markdown('<div class="verdict-divider"></div>', unsafe_allow_html=True)
                render_section("🤖", "AI Recommendations", ("#0a1525", "#60a5fa"), ai_recs_text)
                st.markdown('<div class="verdict-divider"></div>', unsafe_allow_html=True)
                render_section("⚡", "Immediate Actions", ("#1f1500", "#fbbf24"), immediate_text)
                st.markdown('<div class="verdict-divider"></div>', unsafe_allow_html=True)
                render_section("📈", "Growth Opportunities", ("#0f1f16", "#4ade80"), growth_text)

                st.markdown('</div>', unsafe_allow_html=True)

            with t4:
                st.markdown('<div class="section-label">Data quality</div>', unsafe_allow_html=True)
                st.markdown('<div style="background:#0d0f1a;border:0.5px solid #1e2235;border-radius:10px;padding:12px 14px;margin-bottom:14px">', unsafe_allow_html=True)
                for col, pct in report['missing_pct'].items():
                    fr = 100 - pct
                    colr = "#4ade80" if fr > 90 else ("#fbbf24" if fr > 70 else "#f87171")
                    st.markdown(f"""
                    <div class="quality-row">
                        <div class="q-label">{col}</div>
                        <div class="q-track"><div class="q-fill" style="width:{fr}%;background:{colr}"></div></div>
                        <div class="q-val" style="color:{colr}">{fr:.0f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with t6:
                st.markdown('<div class="section-label">AI Business Assistant</div>', unsafe_allow_html=True)
                
                # Welcome card
                st.markdown("""
                <div class="ai-welcome">
                    <div class="ai-welcome-icon">🤖</div>
                    <div class="ai-welcome-title">AI Business Analytics Assistant</div>
                    <div class="ai-welcome-sub">
                        Ask me anything about your data — revenue, profit, customers, products, trends, anomalies, and more.<br>
                        I answer <strong>only</strong> from your uploaded dataset. No guessing. Pure data-driven insights.
                    </div>
                    <div class="ai-chips">
                        <span class="ai-chip">💰 Total Revenue</span>
                        <span class="ai-chip">📈 Growth Trend</span>
                        <span class="ai-chip">🏆 Top Products</span>
                        <span class="ai-chip">👥 Customer Analysis</span>
                        <span class="ai-chip">🌍 Regional Breakdown</span>
                        <span class="ai-chip">⚠️ Anomalies</span>
                        <span class="ai-chip">📊 Data Overview</span>
                        <span class="ai-chip">📉 Profit Analysis</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Initialize chat history
                if 'ai_chat_history' not in st.session_state:
                    st.session_state['ai_chat_history'] = []

                # Chat history display
                if st.session_state['ai_chat_history']:
                    st.markdown('<div class="ai-chat-container">', unsafe_allow_html=True)
                    for msg in st.session_state['ai_chat_history']:
                        if msg['role'] == 'user':
                            st.markdown(f'<div class="ai-msg-user"><div class="bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
                        else:
                            result = msg['content']
                            msg_type = result.get('type', 'answer')
                            if msg_type == 'off_topic':
                                icon = '🚫'
                                color = '#f87171'
                            elif msg_type == 'not_found':
                                icon = '🔍'
                                color = '#fbbf24'
                            else:
                                icon = '🤖'
                                color = '#9d8ff5'
                            
                            summary_html  = f'<div class="ai-section-title ai-summary-label">📋 SUMMARY</div><div>{result["summary"]}</div>'
                            analysis_html = f'<div class="ai-section-title ai-analysis-label" style="margin-top:10px">🔍 ANALYSIS</div><div style="white-space:pre-line">{result["analysis"]}</div>' if result.get('analysis') else ''
                            rec_html      = f'<div class="ai-section-title ai-rec-label" style="margin-top:10px">💡 RECOMMENDATION</div><div>{result["recommendation"]}</div>' if result.get('recommendation') else ''
                            
                            st.markdown(f"""
                            <div class="ai-msg-bot">
                                <div class="ai-bot-avatar">{icon}</div>
                                <div class="bubble">{summary_html}{analysis_html}{rec_html}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Clear chat button
                    if st.button("🗑️ Clear Chat", key="clear_chat"):
                        st.session_state['ai_chat_history'] = []
                        st.rerun()

                # Input area
                st.markdown('<div style="margin-top:12px"></div>', unsafe_allow_html=True)
                with st.form(key='ai_chat_form', clear_on_submit=True):
                    user_q = st.text_input(
                        "Ask a business question",
                        placeholder="e.g. What is the total revenue? Who are the top customers? Show me regional breakdown...",
                        label_visibility="collapsed"
                    )
                    submitted = st.form_submit_button("Send ➤")
                    if submitted and user_q.strip():
                        result = ai_business_assistant(user_q.strip(), df, report, ds_type)
                        st.session_state['ai_chat_history'].append({'role': 'user', 'content': user_q.strip()})
                        st.session_state['ai_chat_history'].append({'role': 'assistant', 'content': result})
                        st.rerun()

            with t5:
                st.markdown('<div class="section-label">Export</div>', unsafe_allow_html=True)
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer: df.to_excel(writer, index=False)
                
                ec1, ec2, ec3 = st.columns(3)
                with ec1:
                    st.markdown('<div class="dl-btn"><div class="dl-btn-icon" style="background:#1e1a3a;color:#9d8ff5"><i class="ti ti-file-text"></i></div><div><div class="dl-btn-text">Summary Report</div><div class="dl-btn-sub">.txt · full analysis</div></div></div>', unsafe_allow_html=True)
                    st.download_button("Download", "Report", "summary.txt", key="d1")
                with ec2:
                    st.markdown('<div class="dl-btn"><div class="dl-btn-icon" style="background:#0f1f16;color:#4ade80"><i class="ti ti-table-export"></i></div><div><div class="dl-btn-text">Cleaned Data</div><div class="dl-btn-sub">.xlsx · structured</div></div></div>', unsafe_allow_html=True)
                    st.download_button("Download", buffer.getvalue(), "cleaned.xlsx", key="d2")
                with ec3:
                    st.markdown('<div class="dl-btn"><div class="dl-btn-icon" style="background:#0a1525;color:#60a5fa"><i class="ti ti-report"></i></div><div><div class="dl-btn-text">Column Map</div><div class="dl-btn-sub">.txt · type report</div></div></div>', unsafe_allow_html=True)
                    st.download_button("Download", "Intel", "intel.txt", key="d3")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
