# ============================================================
# app.py - TariKenali Streamlit App
# Fasya Maulinada (202251155) - Universitas Muria Kudus
# ============================================================
import streamlit as st
import numpy as np
import os, json, sys
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    APP_TITLE, APP_SUBTITLE, APP_VERSION,
    RESEARCHER, NIM, UNIVERSITY, SUPERVISOR_1, SUPERVISOR_2, YEAR,
    CLASS_DISPLAY_NAMES, CLASS_COLORS, CLASS_EMOJIS,
    DANCE_INFO, MODEL_FILE, MODEL_FILE_H5
)
from utils.predictor import (
    load_model, predict, validate_image,
    load_metadata, get_top_k_predictions
)

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title=f'{APP_TITLE} - {APP_SUBTITLE}',
    page_icon='🎭', layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
:root{--primary:#8B1A1A;--secondary:#C9A84C;--text-dark:#1C1C1E;--text-muted:#6B7280;--border:#E5E7EB;}
.stApp{background:linear-gradient(135deg,#F9F5F0 0%,#F0EBE3 100%);font-family:'Inter',sans-serif;}
.hero-container{background:linear-gradient(135deg,#6B0F1A 0%,#8B1A1A 40%,#C9A84C 100%);border-radius:20px;padding:48px 40px;margin-bottom:32px;text-align:center;box-shadow:0 8px 32px rgba(139,26,26,.25);}
.hero-title{font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:700;color:#FFF;margin:0 0 8px;text-shadow:0 2px 8px rgba(0,0,0,.3);}
.hero-subtitle{font-size:1.1rem;color:rgba(255,255,255,.88);margin:0 0 16px;font-weight:300;}
.hero-badge{display:inline-block;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);border-radius:50px;padding:6px 20px;color:#F5E6C8;font-size:.82rem;font-weight:500;}
.card{background:#FFF;border-radius:16px;padding:24px;box-shadow:0 2px 16px rgba(0,0,0,.06);border:1px solid var(--border);margin-bottom:20px;}
.card-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--primary);margin-bottom:14px;}
.result-main{background:linear-gradient(135deg,#6B0F1A,#8B1A1A);border-radius:20px;padding:28px;text-align:center;color:white;box-shadow:0 8px 32px rgba(139,26,26,.3);margin-bottom:20px;}
.result-dance-name{font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:#F5E6C8;margin:8px 0;}
.result-emoji{font-size:3.5rem;display:block;margin-bottom:8px;}
.stat-box{background:#F9F5F0;border-radius:12px;padding:14px;text-align:center;border:1px solid #E5E7EB;margin-bottom:8px;}
.stat-value{font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:700;color:var(--primary);}
.stat-label{font-size:.75rem;color:var(--text-muted);font-weight:500;text-transform:uppercase;letter-spacing:.5px;}
.section-divider{height:2px;background:linear-gradient(90deg,var(--primary),var(--secondary),transparent);border-radius:2px;margin:24px 0;opacity:.4;}
.keunikan-item{display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);font-size:.88rem;color:var(--text-dark);}
.keunikan-item:last-child{border-bottom:none;}
.info-tag{display:inline-block;background:#F3E8FF;color:#6B21A8;border-radius:8px;padding:3px 10px;margin:3px;font-size:.8rem;font-weight:500;}
.conf-badge-high{background:#D1FAE5;color:#065F46;padding:4px 14px;border-radius:50px;font-weight:600;font-size:.83rem;}
.conf-badge-medium{background:#FEF3C7;color:#92400E;padding:4px 14px;border-radius:50px;font-weight:600;font-size:.83rem;}
.conf-badge-low{background:#FEE2E2;color:#991B1B;padding:4px 14px;border-radius:50px;font-weight:600;font-size:.83rem;}
.sidebar-header{text-align:center;padding:16px;background:linear-gradient(135deg,#6B0F1A,#8B1A1A);border-radius:12px;color:white;margin-bottom:20px;}
#MainMenu,footer{visibility:hidden;}
.stDeployButton{display:none;}
</style>
""", unsafe_allow_html=True)


# ── UI HELPERS ─────────────────────────────────────────────────────
def render_hero():
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-title">🎭 {APP_TITLE}</div>
        <div class="hero-subtitle">{APP_SUBTITLE}</div>
        <div class="hero-badge">
            🎓 {RESEARCHER} &nbsp;•&nbsp; {NIM} &nbsp;•&nbsp; {UNIVERSITY} &nbsp;•&nbsp; {YEAR}
        </div>
    </div>""", unsafe_allow_html=True)


def render_confidence_bar(probabilities):
    names  = list(probabilities.keys())
    values = [v*100 for v in probabilities.values()]
    colors_list = [CLASS_COLORS.get(n,'#6B7280') for n in names]
    data = sorted(zip(names,values,colors_list), key=lambda x:x[1], reverse=True)
    ns,vs,cs = zip(*data)
    fig = go.Figure(go.Bar(
        x=vs, y=ns, orientation='h',
        marker=dict(color=cs, line=dict(color='rgba(0,0,0,.1)',width=1)),
        text=[f'{v:.1f}%' for v in vs], textposition='outside',
        hovertemplate='<b>%{y}</b><br>%{x:.2f}%<extra></extra>'
    ))
    fig.update_layout(
        height=240, margin=dict(l=5,r=55,t=5,b=5),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0,115],showgrid=True,gridcolor='rgba(0,0,0,.05)',ticksuffix='%'),
        yaxis=dict(tickfont=dict(size=11)), showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})


def render_dance_info(dance_name):
    if dance_name not in DANCE_INFO: return
    info  = DANCE_INFO[dance_name]
    color = CLASS_COLORS.get(dance_name,'#8B1A1A')
    emoji = CLASS_EMOJIS.get(dance_name,'🎭')
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{emoji} Tentang {dance_name}</div>
        <p style="color:#4B5563;font-size:.92rem;line-height:1.7;margin-bottom:14px;">{info['deskripsi']}</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
            <span class="info-tag">📍 {info['asal']}</span>
            <span class="info-tag">⏳ {info['era']}</span>
            <span class="info-tag">💃 {info['penari']}</span>
            <span class="info-tag">🎯 {info['fungsi']}</span>
        </div>
    </div>""", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="card"><div class="card-title">👘 Kostum & Busana</div>
        <p style="color:#4B5563;font-size:.87rem;line-height:1.7;">{info['kostum']}</p></div>""",
        unsafe_allow_html=True)
    with c2:
        keunikan_html = ''.join(
            f'<div class="keunikan-item"><span style="color:{color}">◆</span><span>{k}</span></div>'
            for k in info['keunikan']
        )
        st.markdown(f"""<div class="card"><div class="card-title">✨ Keunikan</div>
        {keunikan_html}</div>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card" style="border-left:4px solid {color};">
        <div class="card-title">🪷 Nilai Filosofis</div>
        <p style="font-style:italic;color:#374151;font-size:.92rem;line-height:1.6;">"{info['nilai_filosofis']}"</p>
    </div>""", unsafe_allow_html=True)


def render_sidebar(metadata):
    with st.sidebar:
        st.markdown("""<div class="sidebar-header">
            <div style="font-size:1.25rem;font-weight:700;">🎭 TariKenali</div>
            <div style="font-size:.78rem;opacity:.85;margin-top:4px;">Sistem Klasifikasi Kostum Tari</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("#### 📌 Navigasi")
        page = st.radio("Pilih Halaman",
            ["🔍 Klasifikasi","📚 Katalog Tari","📊 Tentang Model"],
            label_visibility='collapsed')
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        if metadata:
            perf = metadata.get('performance',{})
            st.markdown("#### 📊 Performa Model")
            c1,c2 = st.columns(2)
            for col,(lbl,key) in zip([c1,c2,c1,c2],[
                ('Akurasi','accuracy'),('F1-Score','f1_score'),
                ('Presisi','precision'),('Recall','recall')
            ]):
                val = perf.get(key,0)*100
                with col:
                    st.markdown(f"""<div class="stat-box">
                    <div class="stat-value">{val:.1f}%</div>
                    <div class="stat-label">{lbl}</div></div>""", unsafe_allow_html=True)
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("#### 🎭 Kelas Tarian")
        for name in CLASS_DISPLAY_NAMES:
            color = CLASS_COLORS.get(name,'#6B7280')
            emoji = CLASS_EMOJIS.get(name,'🎭')
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:6px 10px;
                        margin:3px 0;border-radius:8px;background:#F9F5F0;
                        border-left:3px solid {color};">
                <span>{emoji}</span>
                <span style="font-size:.83rem;color:#374151;font-weight:500;">{name}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:.8rem;color:#4B5563;line-height:1.9;">
            <b>{RESEARCHER}</b><br>NIM: {NIM}<br>{UNIVERSITY}<br><br>
            <b>Pembimbing:</b><br>{SUPERVISOR_1}<br>{SUPERVISOR_2}
        </div>""", unsafe_allow_html=True)
    return page


# ── HALAMAN KLASIFIKASI ────────────────────────────────────────────
def page_klasifikasi(model):
    st.markdown("""<div class="card">
        <div class="card-title">🔍 Klasifikasi Kostum Tari</div>
        <p style="color:#6B7280;font-size:.88rem;margin:0;">
            Upload foto kostum tari tradisional Jawa Tengah untuk diidentifikasi secara otomatis
            menggunakan model CNN berbasis MobileNetV2 dengan Transfer Learning.
        </p></div>""", unsafe_allow_html=True)

    col_up, col_res = st.columns([1,1], gap='large')
    image = None

    with col_up:
        st.markdown("""<div class="card"><div class="card-title">📸 Upload Gambar</div></div>""",
                    unsafe_allow_html=True)
        uploaded = st.file_uploader("Pilih gambar", type=['jpg','jpeg','png','webp'],
                                    label_visibility='collapsed',
                                    help="Format: JPG/JPEG/PNG/WEBP. Maks 10MB.")
        st.markdown("<br>", unsafe_allow_html=True)
        use_cam = st.toggle("📷 Gunakan Kamera", value=False)
        cam_file = None
        if use_cam:
            cam_file = st.camera_input("Ambil Foto", label_visibility='collapsed')
        source = cam_file if (use_cam and cam_file) else uploaded

        if source:
            image = Image.open(source)
            st.image(image, use_container_width=True, caption='Gambar input')
            st.markdown(f"""
            <div style="background:#F3F4F6;border-radius:10px;padding:10px 14px;
                        font-size:.8rem;color:#6B7280;margin-top:6px;">
                📐 {image.width}×{image.height}px &nbsp;|&nbsp; 🎨 {image.mode}
                &nbsp;|&nbsp; ➡️ Resize ke 224×224
            </div>""", unsafe_allow_html=True)

    with col_res:
        if image:
            is_valid, val_msg = validate_image(image)
            if not is_valid:
                st.error(f"❌ {val_msg}")
                return

            btn = st.button("🔮 Identifikasi Kostum Sekarang",
                            type='primary', use_container_width=True)
            if btn:
                with st.spinner('🧠 Model sedang menganalisis...'):
                    result = predict(model, image)

                dance  = result['predicted_class']
                conf   = result['confidence_pct']
                level  = result['confidence_level']
                t_ms   = result['inference_time_ms']
                emoji  = CLASS_EMOJIS.get(dance,'🎭')
                badge_map = {
                    'high'  :('conf-badge-high','✅ Sangat Yakin'),
                    'medium':('conf-badge-medium','⚡ Cukup Yakin'),
                    'low'   :('conf-badge-low','⚠️ Kurang Yakin'),
                }
                bclass, btext = badge_map[level]

                st.markdown(f"""
                <div class="result-main">
                    <span class="result-emoji">{emoji}</span>
                    <div style="font-size:.82rem;color:rgba(255,255,255,.7);
                                text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">
                        Teridentifikasi Sebagai
                    </div>
                    <div class="result-dance-name">{dance}</div>
                    <div style="font-size:1rem;color:rgba(255,255,255,.9);margin-top:6px;">
                        Kepercayaan: <b>{conf:.2f}%</b>
                    </div>
                    <div style="margin-top:10px;"><span class="{bclass}">{btext}</span></div>
                    <div style="margin-top:10px;font-size:.76rem;color:rgba(255,255,255,.5);">
                        ⚡ {t_ms:.1f} ms
                    </div>
                </div>""", unsafe_allow_html=True)

                st.markdown("""<div class="card"><div class="card-title">📊 Distribusi Probabilitas</div></div>""",
                            unsafe_allow_html=True)
                render_confidence_bar(result['all_probabilities'])

                st.markdown("**🏆 Top 3 Prediksi:**")
                for rank,(name,prob) in enumerate(get_top_k_predictions(result,3),1):
                    color = CLASS_COLORS.get(name,'#6B7280')
                    medal = ['🥇','🥈','🥉'][rank-1]
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;padding:8px 12px;
                                border-radius:8px;margin:4px 0;background:#F9F5F0;
                                border-left:3px solid {color};">
                        <span style="font-size:1rem;">{medal}</span>
                        <span style="flex:1;font-weight:500;color:#374151;font-size:.88rem;">{name}</span>
                        <span style="color:{color};font-weight:700;font-size:.92rem;">{prob*100:.2f}%</span>
                    </div>""", unsafe_allow_html=True)

                # Info tarian di bawah
                st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="font-family:'Playfair Display';font-size:1.4rem;font-weight:700;
                            color:#6B0F1A;text-align:center;margin-bottom:20px;">
                    📖 Informasi Lengkap {dance}
                </div>""", unsafe_allow_html=True)
                render_dance_info(dance)

            else:
                st.markdown("""
                <div class="card" style="text-align:center;padding:48px 24px;">
                    <div style="font-size:3.2rem;margin-bottom:14px;">🔮</div>
                    <div style="font-size:1rem;font-weight:600;color:#374151;margin-bottom:8px;">
                        Siap Mengidentifikasi!
                    </div>
                    <div style="color:#9CA3AF;font-size:.85rem;line-height:1.6;">
                        Klik tombol <b>"Identifikasi Kostum Sekarang"</b> untuk mulai.
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:60px 24px;">
                <div style="font-size:4rem;margin-bottom:14px;">🎭</div>
                <div style="font-size:1.1rem;font-weight:600;color:#374151;margin-bottom:10px;">
                    Upload Gambar Kostum Tari
                </div>
                <div style="color:#9CA3AF;font-size:.85rem;line-height:1.7;">
                    Upload foto kostum tari tradisional Jawa Tengah melalui panel kiri.<br><br>
                    <b>5 kelas:</b> Bedhaya · Dolalak · Gambyong · Golek · Srimpi
                </div>
            </div>""", unsafe_allow_html=True)


# ── HALAMAN KATALOG ────────────────────────────────────────────────
def page_katalog():
    st.markdown("""<div class="card">
        <div class="card-title">📚 Katalog Tari Tradisional Jawa Tengah</div>
        <p style="color:#6B7280;font-size:.88rem;margin:0;">
            Pelajari kelima jenis tari tradisional Jawa Tengah yang menjadi objek klasifikasi penelitian ini.
        </p></div>""", unsafe_allow_html=True)

    selected = st.multiselect("Filter:", CLASS_DISPLAY_NAMES, default=CLASS_DISPLAY_NAMES)
    if not selected:
        st.info("Pilih minimal satu tarian.")
        return

    for dance in selected:
        if dance not in DANCE_INFO: continue
        info  = DANCE_INFO[dance]
        color = CLASS_COLORS.get(dance,'#8B1A1A')
        emoji = CLASS_EMOJIS.get(dance,'🎭')
        with st.expander(f"{emoji} {dance}", expanded=(len(selected)==1)):
            c1,c2 = st.columns([2,1])
            with c1:
                st.markdown(f"""
                <p style="color:#374151;font-size:.9rem;line-height:1.7;background:#F9FAFB;
                           padding:16px;border-radius:10px;border-left:3px solid {color};">
                    {info['deskripsi']}
                </p>
                <p style="color:#4B5563;font-size:.87rem;line-height:1.7;
                          background:#F9FAFB;padding:14px;border-radius:10px;margin-top:10px;">
                    <b>👘 Kostum:</b> {info['kostum']}
                </p>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="background:{color};border-radius:16px;padding:20px;
                            color:white;text-align:center;margin-bottom:12px;">
                    <div style="font-size:3rem;margin-bottom:6px;">{emoji}</div>
                    <div style="font-size:1.1rem;font-weight:700;">{dance}</div>
                </div>
                <div style="background:#F9F5F0;border-radius:10px;padding:14px;
                            font-size:.82rem;line-height:2.1;">
                    <div>📍 <b>Asal:</b> {info['asal']}</div>
                    <div>⏳ <b>Era:</b> {info['era']}</div>
                    <div>💃 <b>Penari:</b> {info['penari']}</div>
                    <div>🎯 <b>Fungsi:</b> {info['fungsi']}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("**✨ Keunikan:**")
            for k in info['keunikan']:
                st.markdown(f"""
                <div style="display:flex;gap:10px;padding:6px 0;border-bottom:1px solid #F3F4F6;
                            font-size:.87rem;color:#374151;">
                    <span style="color:{color};flex-shrink:0;">◆</span><span>{k}</span>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="margin-top:12px;padding:12px;background:#FFF8E8;border-radius:10px;
                        border-left:3px solid {color};font-style:italic;font-size:.88rem;color:#374151;">
                🪷 {info['nilai_filosofis']}
            </div>""", unsafe_allow_html=True)


# ── HALAMAN TENTANG MODEL ──────────────────────────────────────────
def page_tentang_model(metadata):
    st.markdown("""<div class="card">
        <div class="card-title">📊 Informasi & Spesifikasi Model</div>
        <p style="color:#6B7280;font-size:.88rem;margin:0;">
            Detail teknis model CNN MobileNetV2 untuk klasifikasi kostum tari.
        </p></div>""", unsafe_allow_html=True)

    st.markdown("### 🏗️ Arsitektur Model")
    c1,c2 = st.columns(2)
    with c1:
        rows = [
            ("Base Model","MobileNetV2 (ImageNet)"),
            ("Input Size","224 × 224 × 3"),
            ("Pooling","Global Average Pooling 2D"),
            ("Dense Layer 1","256 neuron (ReLU + L2)"),
            ("Dense Layer 2","128 neuron (ReLU + L2)"),
            ("Batch Norm","Setelah setiap Dense Layer"),
            ("Dropout Rate","0.3 (30%)"),
            ("Output","5 neuron (Softmax)"),
        ]
        html = '<div class="card"><div class="card-title">🔧 Komponen Model</div>'
        for lbl,val in rows:
            html += f'<div style="display:flex;justify-content:space-between;border-bottom:1px solid #F3F4F6;padding:6px 0;font-size:.86rem;color:#374151;"><span>{lbl}</span><b>{val}</b></div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with c2:
        if metadata:
            tc = metadata.get('training_config',{})
            rows2 = [
                ("Optimizer","Adam"),
                ("Loss","Categorical Crossentropy"),
                ("LR Fase 1",str(tc.get('lr_fase1','N/A'))),
                ("LR Fase 2",str(tc.get('lr_fase2','N/A'))),
                ("Batch Size",str(tc.get('batch_size','N/A'))),
                ("Total Data",f"{tc.get('total_samples','N/A')} gambar"),
                ("Train/Val/Test","70% / 15% / 15%"),
                ("Stratified Split","Ya"),
            ]
            html2 = '<div class="card"><div class="card-title">⚙️ Konfigurasi Training</div>'
            for lbl,val in rows2:
                html2 += f'<div style="display:flex;justify-content:space-between;border-bottom:1px solid #F3F4F6;padding:6px 0;font-size:.86rem;color:#374151;"><span>{lbl}</span><b>{val}</b></div>'
            html2 += '</div>'
            st.markdown(html2, unsafe_allow_html=True)

    if metadata:
        perf = metadata.get('performance',{})
        st.markdown("### 📈 Hasil Evaluasi")
        metrics = {
            'Akurasi'  : perf.get('accuracy',0)*100,
            'Precision': perf.get('precision',0)*100,
            'Recall'   : perf.get('recall',0)*100,
            'F1-Score' : perf.get('f1_score',0)*100,
        }
        cols = st.columns(4)
        for col,(name,val) in zip(cols,metrics.items()):
            with col:
                st.metric(f"{'✅' if val>=80 else '⚠️'} {name}", f"{val:.2f}%",
                          delta=f"{val-80:.2f}% vs target")
        fig = px.bar(x=list(metrics.keys()), y=list(metrics.values()),
                     color=list(metrics.keys()),
                     color_discrete_map={'Akurasi':'#8B0000','Precision':'#1A5276',
                                         'Recall':'#1E8449','F1-Score':'#6C3483'},
                     text=[f'{v:.2f}%' for v in metrics.values()],
                     title='Perbandingan Metrik Evaluasi Model')
        fig.add_hline(y=80, line_dash='dash', line_color='orange',
                      annotation_text='Target 80%', annotation_position='top right')
        fig.update_traces(textposition='outside')
        fig.update_layout(height=340, showlegend=False,
                          yaxis=dict(range=[0,115],ticksuffix='%'),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    st.markdown("### 📋 Panduan Penggunaan")
    steps = [
        ("1️⃣ Upload Gambar","Klik 'Browse files' atau drag & drop gambar kostum tari (JPG/PNG/WEBP)."),
        ("2️⃣ Klik Identifikasi","Tekan tombol 'Identifikasi Kostum Sekarang' untuk mulai analisis AI."),
        ("3️⃣ Lihat Hasil","Model menampilkan nama tarian + tingkat kepercayaan prediksi."),
        ("4️⃣ Baca Informasi","Pelajari detail kostum dan sejarah tarian yang teridentifikasi."),
        ("5️⃣ Eksplorasi Katalog","Kunjungi halaman Katalog untuk mempelajari semua jenis tari."),
    ]
    for title,desc in steps:
        num  = title.split()[0]
        rest = ' '.join(title.split()[1:])
        st.markdown(f"""
        <div style="display:flex;gap:14px;padding:10px;border-radius:10px;
                    background:#F9F5F0;margin-bottom:7px;align-items:flex-start;">
            <span style="font-size:1.1rem;flex-shrink:0;">{num}</span>
            <div>
                <div style="font-weight:600;color:#374151;font-size:.88rem;">{rest}</div>
                <div style="color:#6B7280;font-size:.82rem;margin-top:2px;">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ── MAIN ───────────────────────────────────────────────────────────
def main():
    model    = None
    metadata = load_metadata(MODEL_DIR)
    err      = None

    try:
        with st.spinner('⏳ Memuat model AI...'):
            model = load_model(MODEL_DIR)
    except Exception as e:
        err = str(e)

    render_hero()
    page = render_sidebar(metadata)

    if page == "🔍 Klasifikasi":
        if model:
            page_klasifikasi(model)
        else:
            st.error(f"⚠️ **Model tidak dapat dimuat!**\n\n{err}\n\n"
                     "**Solusi:** Pastikan `model_kostum_tari.keras` ada di folder yang sama dengan `app.py`.")
            st.info("💡 Anda tetap dapat menjelajahi **Katalog Tari** dan **Tentang Model**.")

    elif page == "📚 Katalog Tari":
        page_katalog()

    elif page == "📊 Tentang Model":
        page_tentang_model(metadata)

    st.markdown(f"""
    <div style="text-align:center;padding:20px;color:#9CA3AF;font-size:.75rem;
                border-top:1px solid #E5E7EB;margin-top:32px;">
        🎭 <b>TariKenali</b> v{APP_VERSION} &nbsp;|&nbsp;
        {RESEARCHER} ({NIM}) &nbsp;|&nbsp; {UNIVERSITY} &nbsp;|&nbsp; {YEAR}<br>
        <span style="opacity:.6;">TensorFlow · MobileNetV2 · Streamlit</span>
    </div>""", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
