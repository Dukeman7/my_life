import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="LDK - Bunker Central", page_icon="🚀", layout="wide")

st.title("🚀 LDK Control Center")
st.write("Conexión segura. Bienvenido al Búnker, Comandante.")

# 2. CONEXIÓN Y LIMPIEZA DE DATOS
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    # Limpiamos espacios en blanco en los títulos
    df.columns = df.columns.str.strip()
    
    # Quitamos filas vacías
    df = df.dropna(subset=['NOMBRE', 'ENLACE'])
    
    # Convertimos FAVORITO a booleano real
    df['FAVORITO'] = df['FAVORITO'].astype(bool)
    
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# 3. SECCIÓN DE FAVORITOS (ACCESO RÁPIDO)
favoritos = df[df['FAVORITO'] == True]

if not favoritos.empty:
    st.subheader("⭐ Sistemas Críticos")
    cols_fav = st.columns(3)
    for i, (_, row) in enumerate(favoritos.iterrows()):
        with cols_fav[i % 3]:
            with st.container(border=True):
                # Logo automático
                thumb = f"https://www.google.com/s2/favicons?domain={row['ENLACE']}&sz=128"
                st.image(thumb, width=48)
                st.subheader(row['NOMBRE'])
                st.write(row['DESCRIPCION'])
                st.link_button("🚀 ABRIR SISTEMA", row['ENLACE'], use_container_width=True)

st.divider()

# 4. DIRECTORIO POR CATEGORÍAS
if not df.empty:
    categorias = sorted(df['CATEGORIA'].unique())
    tabs = st.tabs(categorias)

    for i, cat in enumerate(categorias):
        with tabs[i]:
            subset = df[df['CATEGORIA'] == cat]
            cols = st.columns(3)
            for j, (_, row) in enumerate(subset.iterrows()):
                with cols[j % 3]:
                    with st.container(border=True):
                        thumb_mini = f"https://www.google.com/s2/favicons?domain={row['ENLACE']}&sz=64"
                        st.image(thumb_mini, width=32)
                        st.markdown(f"**{row['NOMBRE']}**")
                        st.caption(row['DESCRIPCION'])
                        st.link_button(f"Abrir", row['ENLACE'], use_container_width=True)

# 5. FOOTER
st.sidebar.markdown("---")
st.sidebar.write("👤 **Ing. Luis Duque**")
st.sidebar.caption("Modo Gumersinda: ONLINE 🛡️")
