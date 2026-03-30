import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuración de la página con estética "Bunker"
st.set_page_config(page_title="LDK - Bunker Central", page_icon="🚀", layout="wide")

# Estilo CSS para las tarjetas (Cards)
st.markdown("""
    <style>
    .link-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .link-card:hover {
        border-color: #ff4b4b;
        background-color: #262626;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 LDK Control Center")
st.write("Bienvenido al Búnker, Comandante. Todos sus sistemas en un solo lugar.")

# 1. Conexión con el Google Sheet
# Recuerda configurar tus SECRETS en Streamlit Cloud con la URL del Sheet
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    # Limpiamos filas vacías por si acaso
    df = df.dropna(subset=['NOMBRE', 'ENLACE'])
except Exception as e:
    st.error(f"Error de conexión: Verifique que el Sheet sea público o las credenciales. {e}")
    st.stop()

# --- SECCIÓN DE FAVORITOS (Los del Check) ---
# En el Sheet, el check se lee como True/False
favoritos = df[df['FAVORITO'] == True]

if not favoritos.empty:
    st.subheader("⭐ Sistemas Críticos (Favoritos)")
    cols_fav = st.columns(3)
    for i, (_, row) in enumerate(favoritos.iterrows()):
        with cols_fav[i % 3]:
            # Generamos thumbnail automático usando el icono del dominio
            thumb = f"https://www.google.com/s2/favicons?domain={row['ENLACE']}&sz=128"
            st.markdown(f"""
                <div class="link-card">
                    <img src="{thumb}" width="40" style="margin-bottom:10px;">
                    <h3 style="margin:0;">{row['NOMBRE']}</h3>
                    <p style="font-size:0.8em; color:#888;">{row['DESCRIPCION']}</p>
                    <a href="{row['ENLACE']}" target="_blank" style="color:#ff4b4b; text-decoration:none;">🚀 ABRIR SISTEMA</a>
                </div>
            """, unsafe_allow_html=True)

st.divider()

# --- SECCIÓN POR CATEGORÍAS ---
st.subheader("📁 Directorio General")
categorias = sorted(df['CATEGORIA'].unique())
tabs = st.tabs(categorias)

for i, cat in enumerate(categorias):
    with tabs[i]:
        subset = df[df['CATEGORIA'] == cat]
        cols = st.columns(3)
        for j, (_, row) in enumerate(subset.iterrows()):
            with cols[j % 3]:
                thumb = f"https://www.google.com/s2/favicons?domain={row['ENLACE']}&sz=64"
                with st.container(border=True):
                    st.image(thumb, width=32)
                    st.write(f"**{row['NOMBRE']}**")
                    st.caption(row['DESCRIPCION'])
                    st.link_button(f"Ir a {cat}", row['ENLACE'], use_container_width=True)

# Footer con el sello de la casa
st.sidebar.markdown("---")
st.sidebar.write("👤 **Desarrollo:** Ing. Luis Duque")
st.sidebar.caption("Modo Gumersinda: Activo 🛡️")
