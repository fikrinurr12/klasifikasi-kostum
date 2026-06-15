# ============================================================
# FILE: utils/styles.py
# DESKRIPSI: Custom CSS untuk tampilan Streamlit
# ============================================================

import streamlit as st


def inject_custom_css():
    """Inject custom CSS ke aplikasi Streamlit."""
    st.markdown("""
    <style>
    /* ─── GLOBAL ─── */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Sembunyikan elemen default Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ─── SCROLLBAR ─── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: #9C6B9E; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #7B4F7D; }

    /* ─── SIDEBAR ─── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2C1654 0%, #4A235A 50%, #6B3570 100%);
    }
    [data-testid="stSidebar"] * {
        color: #F8F0FB !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #F8F0FB !important;
        font-weight: 500;
        padding: 6px 0;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2) !important;
    }

    /* ─── HERO BOX ─── */
    .hero-box {
        background: linear-gradient(135deg, #6B3570 0%, #9C6B9E 50%, #C4A2C6 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(107, 53, 112, 0.3);
    }
    .hero-box h1 {
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 0.8rem;
    }
    .hero-sub {
        color: rgba(255,255,255,0.9) !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ─── STAT BOX ─── */
    .stat-box {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        gap: 1rem;
    }
    .stat-item {
        text-align: center;
        padding: 0.8rem;
        background: linear-gradient(135deg, #F3E5F5 0%, #E8D5F0 100%);
        border-radius: 12px;
    }
    .stat-number {
        display: block;
        font-size: 1.4rem;
        font-weight: 700;
        color: #6B3570;
    }
    .stat-label {
        display: block;
        font-size: 0.8rem;
        color: #888;
        margin-top: 2px;
    }

    /* ─── STEP CARDS ─── */
    .step-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-top: 4px solid #9C6B9E;
        height: 100%;
        transition: transform 0.2s;
    }
    .step-card:hover { transform: translateY(-3px); }
    .step-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .step-card h4 {
        color: #6B3570;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .step-card p {
        color: #666;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* ─── TARI PREVIEW CARDS ─── */
    .tari-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-bottom: 3px solid #9C6B9E;
        transition: all 0.2s;
        height: 100%;
    }
    .tari-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(107,53,112,0.15);
    }
    .tari-icon { font-size: 2.5rem; margin-bottom: 0.4rem; }
    .tari-card h4 {
        color: #4A235A;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .tari-asal {
        color: #888;
        font-size: 0.73rem;
        margin-bottom: 0.4rem;
    }
    .tari-short {
        color: #555;
        font-size: 0.76rem;
        line-height: 1.4;
    }

    /* ─── RESULT BADGE ─── */
    .result-badge {
        background: linear-gradient(135deg, #F8F0FB 0%, #EDD6F2 100%);
        border: 3px solid #9C6B9E;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(107,53,112,0.15);
    }
    .result-icon { font-size: 3rem; margin-bottom: 0.5rem; display: block; }
    .result-name {
        color: #4A235A !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    .confidence-bar-container {
        background: #E0E0E0;
        border-radius: 10px;
        height: 12px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .confidence-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.8s ease;
    }
    .confidence-text {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.4rem;
    }

    /* ─── PROBABILITY BARS ─── */
    .prob-bar-wrap {
        background: #F0F0F0;
        border-radius: 8px;
        height: 20px;
        overflow: hidden;
        margin-top: 4px;
    }
    .prob-bar {
        height: 100%;
        border-radius: 8px;
        min-width: 2px;
        transition: width 0.5s ease;
    }

    /* ─── PLACEHOLDER BOX ─── */
    .placeholder-box {
        background: #FAFAFA;
        border: 2px dashed #CCC;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        color: #999;
    }
    .placeholder-box h3 { color: #777; margin-top: 0.5rem; }
    .placeholder-box p  { color: #999; font-size: 0.9rem; }
    .placeholder-box ul { color: #888; font-size: 0.85rem; }

    /* ─── METRIC CARDS ─── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #F8F0FB 0%, #F0E0F5 100%);
        border-radius: 10px;
        padding: 0.8rem;
        border-left: 4px solid #9C6B9E;
    }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; color: #666 !important; }
    [data-testid="stMetricValue"] { font-size: 0.95rem !important; color: #4A235A !important; font-weight: 600 !important; }

    /* ─── BUTTONS ─── */
    .stButton > button {
        background: linear-gradient(135deg, #6B3570 0%, #9C6B9E 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s;
        box-shadow: 0 3px 10px rgba(107,53,112,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(107,53,112,0.4);
    }

    /* ─── EXPANDER ─── */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #F8F0FB 0%, #EDD6F2 100%) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        color: #4A235A !important;
    }
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #EDD6F2 0%, #D9B8E0 100%) !important;
    }

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #F3E5F5;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #6B3570;
        font-weight: 500;
        padding: 6px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #4A235A !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(107,53,112,0.15);
    }

    /* ─── INFO/WARNING/SUCCESS BOXES ─── */
    .stAlert {
        border-radius: 10px !important;
    }

    /* ─── FILE UPLOADER ─── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #9C6B9E !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }

    /* ─── DIVIDER ─── */
    hr {
        border-color: #E8D5F0 !important;
        margin: 1.5rem 0 !important;
    }

    /* ─── RESPONSIVE ─── */
    @media (max-width: 768px) {
        .hero-box h1 { font-size: 1.3rem !important; }
        .stat-number { font-size: 1.1rem; }
    }
    </style>
    """, unsafe_allow_html=True)
