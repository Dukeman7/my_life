import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Calculadora RF - Trópico", layout="wide")
st.title("📡 Simulador de Enlace Microondas (Zona Tropical)")
st.markdown("Cálculo de Margen de Desvanecimiento y Atenuación por Lluvia (UIT-R P.838)")

# --- BARRA LATERAL: ENTRADA DE DATOS ---
st.sidebar.header("Parámetros del Enlace")
distancia = st.sidebar.slider("Longitud del Enlace (km)", 1.0, 50.0, 27.0, 0.5)
frecuencia = st.sidebar.slider("Frecuencia (GHz)", 5.0, 11.0, 7.1, 0.1)

st.sidebar.header("Equipamiento")
tx_power = st.sidebar.number_input("Potencia TX (dBm)", value=25.0)
ant_tx_gain = st.sidebar.number_input("Ganancia Antena TX (dBi)", value=34.0)
ant_rx_gain = st.sidebar.number_input("Ganancia Antena RX (dBi)", value=34.0)
rx_sens = st.sidebar.number_input("Umbral RX deseado (dBm)", value=-65.0)

st.sidebar.header("Climatología (Región Norte de Suramérica)")
# Tasa de lluvia típica UIT Zona P/N
lluvia_mmh = st.sidebar.slider("Intensidad de Lluvia (mm/h)", 0.0, 150.0, 95.0, 5.0)

# --- CÁLCULOS FÍSICOS ---
# 1. Pérdida en Espacio Libre (FSPL)
fspl = 92.4 + 20 * math.log10(distancia) + 20 * math.log10(frecuencia)

# 2. Atenuación por Lluvia (Modelo UIT-R P.838 Simplificado para 7GHz Horizontal)
# Valores aproximados de k y alpha para 7 GHz
k_h = 0.00301
alpha_h = 1.332
gamma_r = k_h * (lluvia_mmh ** alpha_h) # Atenuación específica dB/km
atenuacion_lluvia_total = gamma_r * distancia

# 3. Cálculo de Potencia Recibida (PIRE - Pérdidas + Ganancia RX)
pire = tx_power + ant_tx_gain
rx_level_clear = pire - fspl + ant_rx_gain
rx_level_rain = rx_level_clear - atenuacion_lluvia_total

margen_desvanecimiento = rx_level_rain - rx_sens

# --- MÉTRICAS EN PANTALLA ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("PIRE", f"{pire:.1f} dBm")
col2.metric("Nivel RX (Cielo Claro)", f"{rx_level_clear:.1f} dBm")
col3.metric("Pérdida por Lluvia", f"{atenuacion_lluvia_total:.1f} dB")
col4.metric("Nivel RX (Bajo Lluvia)", f"{rx_level_rain:.1f} dBm", 
            delta=f"{margen_desvanecimiento:.1f} dB vs Umbral", 
            delta_color="normal" if margen_desvanecimiento > 0 else "inverse")

# --- GRÁFICO CON PLOTLY ---
st.subheader("Perfil de Atenuación vs Distancia")
distancias = np.linspace(1, 50, 100)
rx_clear_array = pire - (92.4 + 20 * np.log10(distancias) + 20 * np.log10(frecuencia)) + ant_rx_gain
rx_rain_array = rx_clear_array - (gamma_r * distancias)

fig = go.Figure()

# Curva sin lluvia
fig.add_trace(go.Scatter(x=distancias, y=rx_clear_array, mode='lines', 
                         name='Nivel RX (Despejado)', line=dict(color='blue', width=2)))
# Curva con lluvia
fig.add_trace(go.Scatter(x=distancias, y=rx_rain_array, mode='lines', 
                         name=f'Nivel RX (Lluvia {lluvia_mmh} mm/h)', line=dict(color='red', width=2, dash='dash')))
# Línea de umbral (Sensibilidad)
fig.add_hline(y=rx_sens, line_dash="dot", annotation_text="Umbral de Sensibilidad (MCS Objetivo)", 
              annotation_position="bottom right", line_color="orange")
# Punto del enlace actual
fig.add_vline(x=distancia, line_dash="solid", line_color="gray", opacity=0.5)

fig.update_layout(
    xaxis_title='Distancia (km)',
    yaxis_title='Nivel de Señal Recibida (dBm)',
    template='plotly_dark',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)
