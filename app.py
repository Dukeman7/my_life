import streamlit as st
from datetime import date
import pandas as pd

# Configuración de página romántica y técnica
st.set_page_config(page_title="Conexión Vital 14-10", layout="centered")

st.title("💖 REPORTE DE ESTADO: CONEXIÓN ININTERRUMPIDA")
st.subheader("Análisis de Disponibilidad y Crecimiento del Sistema")

# Fechas Maestras
f_ella = date(1978, 3, 4)
f_juancho = date(1969, 6, 28)
f_novios = date(1998, 7, 4)
hoy = date.today()

# Cálculos de Tiempo
dias_juntos = (hoy - f_novios).days
vida_juancho = (hoy - f_juancho).days
vida_ella = (hoy - f_ella).days
dias_medio = (date(2026, 6, 23)- f_juancho).days /2
dias_vida = (date(2026, 6, 23)- f_juancho).days
dias_crossover = (date(2026, 6, 23)- hoy).days

# El Crossover de Juancho (Cálculo exacto)
# x = dias sin ella + dias con ella. Queremos dias con ella > dias sin ella.
# Ocurre cuando dias_con_ella = vida_total / 2
dias_para_crossover = vida_juancho - (2 * dias_juntos)
fecha_crossover = date(2026, 6, 23)

# --- INTERFAZ ---
st.info(f"📍 **Estado del Enlace:** Activo y Sincronizado desde hace {dias_juntos:,} días.")

col1, col2 = st.columns(2)
with col1:
    st.metric("DISPONIBILIDAD SIN LUZ", f"{(dias_juntos/vida_ella)*100:.1f}%")
    st.write("Más de la mitad de MI vida caminando a tu lado.")

with col2:
    st.metric("DISPONIBILIDAD CON LUZ", f"{(dias_juntos/vida_juancho)*100:.1f}%")
    st.write("A solo meses del Crossover Total (50%+).")

st.divider()
st.subheader("⏳ Hitos del Cronograma de Red")

hitos = {
    "04/07/1998": "Establecimiento de Sesión (Novios)",
    "14/10/1999": "Protocolo Civil (Boda)",
    "14/10/2000": "Startup: Empresa Registrada",
    "14/10/2001": "Expansión de Nodo: Primer Hijo",
    "14/10/2014": "Cifrado de Alta Seguridad (Iglesia)",
    "23/06/2026": "EL CROSSOVER (Más vida con Luz que sin Luz)",
    "14/10/2028": "Roaming Global (Viaje por el Mundo)"
}

for fecha, evento in hitos.items():
    st.write(f"📅 **{fecha}** — {evento}")

st.success(f"🚀 **Próximo Gran Salto:** El 23 de junio de 2026, mi vida tendrá más días compartidos que días en solitario")

st.sidebar.markdown("---")
st.sidebar.write("🛠️ **Ingeniería de Sistemas Amorosos**")
st.sidebar.write("Release: 14-10-Ever")
st.sidebar.write(dias_medio)
st.sidebar.write(vida_juancho)
st.sidebar.write(dias_vida)
st.sidebar.write(dias_crossover)
