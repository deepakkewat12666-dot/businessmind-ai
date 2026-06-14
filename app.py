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
</style>

<div class="sidebar" id="custom-sidebar">
  <div class="sb-logo">B</div>
  <div class="sb-icon active" data-tab="0"><i class="ti ti-layout-dashboard"></i></div>
  <div class="sb-icon" data-tab="1"><i class="ti ti-chart-bar"></i></div>
  <div class="sb-icon" data-tab="2"><i class="ti ti-bulb"></i></div>
  <div class="sb-icon" data-tab="3"><i class="ti ti-table"></i></div>
  <div class="sb-div"></div>
  <div class="sb-icon" data-tab="4"><i class="ti ti-settings"></i></div>
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
            t1, t2, t3, t4, t5 = st.tabs(["Overview", "Charts", "Insights", "Data Quality", "Export"])
            
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
