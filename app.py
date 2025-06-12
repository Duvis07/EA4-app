import streamlit as st
st.set_page_config(
    page_title="Análisis de Ventas - TechNova Retail",
    page_icon="📊",
    layout="wide"
)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import unicodedata
from datetime import datetime
from plotly.subplots import make_subplots

# Importar las funciones desde los módulos correspondientes
try:
    from caso_estudio import mostrar_caso_estudio
except ImportError:
    mostrar_caso_estudio = None

# Importar la función desde el módulo analisis_estrategico.py
from analisis_estrategico import mostrar_analisis_estrategico

# --- CSS para diseño moderno tipo "app de turismo" ---
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .stTabs [data-baseweb="tab-list"] {gap: 24px;}
    .stTabs [data-baseweb="tab"] {background-color: #e6f2ff; border-radius: 4px; padding: 10px 20px;}
    .stTabs [aria-selected="true"] {background-color: #4a86e8; color: white;}
    h1 {color: #1a365d; font-weight: 800; margin-bottom: 0.5em;}
    h2 {color: #2a4365; font-weight: 700;}
    h3 {color: #2c5282; font-weight: 600;}
    .stMarkdown {line-height: 1.8;}
    div.block-container {padding-top: 2rem;}
    .insight-card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #4a86e8;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .footer {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-top: 30px;
        border-top: 2px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal primero
st.title("📊 Análisis de Ventas - TechNova Retail")

# Banner de autores y descripción después del título
st.markdown("""
<div style='background-color: #f9f9fc; border-radius: 8px; box-shadow: 0 2px 8px rgba(76, 110, 245, 0.05); padding: 20px 26px 14px 26px; margin-bottom: 24px;'>
    <p style='margin:0; font-size: 20px; font-weight: bold; color: #1a365d;'>Desarrollado por: <span style='color:#2563eb;'>Duván, Daniel y Angelo</span></p>
    <span style='font-size:15px; color:#222;'>Esta aplicación interactiva analiza los patrones de ventas en TechNova Retail para identificar tendencias clave que pueden mejorar las ofertas y estrategias de marketing de la empresa. Utiliza los filtros a continuación para personalizar el análisis según tus necesidades específicas.</span>
</div>
""", unsafe_allow_html=True)

# --- Modificación: Mostrar pestañas "Caso de estudio" y "Análisis estratégico" (ocultar "Visualizaciones de ventas") ---
tabs = st.tabs(["Caso de estudio", "Visualizaciones Análisis estratégico"])  # Cambio de nombre de la tercera pestaña

with tabs[0]:
    if mostrar_caso_estudio:
        st.markdown("""
        """, unsafe_allow_html=True)
        mostrar_caso_estudio()
        # Solo texto y conclusiones, nunca gráficos ni insights de ventas
    else:
        st.subheader("Caso de estudio no disponible")
        st.write("No se encontró el módulo 'caso_estudio.py'.")

with tabs[1]:
    st.markdown("""
    <div class='insight-card'>
    <h2>Análisis Estratégico de Ventas</h2>
    <p>Explora el análisis estratégico de ventas con métricas avanzadas y visualizaciones interactivas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Llamar a la función de análisis estratégico
    mostrar_analisis_estrategico()

# --- Cargar y preparar datos (esto se mantiene fuera de las pestañas) ---
@st.cache_data
def load_data():
    df = pd.read_excel("static/Ventas_Minoristas.xlsx")
    # Renombrar columnas para quitar espacios y caracteres especiales
    df = df.rename(columns={
        "ID_cliente": "id_cliente",
        "Nombre_producto": "nombre_producto",
        "Cantidad": "cantidad",
        "Precio_unitario(USD)": "precio_unitario_usd",
        "Fecha": "fecha",
        "categoria": "categoria",
        "pais": "pais",
        "ciudad": "ciudad",
        "metodo_pago": "metodo_pago",
        "edad_cliente": "edad_cliente",
        "genero_cliente": "genero_cliente",
        "calificaci�n_satisfaccion": "calificacion_satisfaccion"
    })
    # Limpiar strings: minúsculas, sin tildes, sin espacios extras
    def limpiar_texto(x):
        if isinstance(x, str):
            x = x.strip().lower()
            x = unicodedata.normalize('NFKD', x).encode('ascii', errors='ignore').decode('utf-8')
        return x
    for col in ["categoria", "pais", "ciudad", "metodo_pago", "genero_cliente", "nombre_producto"]:
        df[col] = df[col].apply(limpiar_texto)
    # Corregir tipos numéricos
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["precio_unitario_usd"] = pd.to_numeric(df["precio_unitario_usd"], errors="coerce")
    df["edad_cliente"] = pd.to_numeric(df["edad_cliente"], errors="coerce")
    if "calificacion_satisfaccion" in df.columns:
        df["calificacion_satisfaccion"] = pd.to_numeric(df["calificacion_satisfaccion"], errors="coerce")
    # Crear columna de ventas
    df["ventas"] = df["cantidad"] * df["precio_unitario_usd"]
    # Quitar filas con datos faltantes críticos (solo columnas que existen)
    columnas_criticas = [col for col in ["cantidad", "precio_unitario_usd", "ventas", "categoria", "fecha"] if col in df.columns]
    if columnas_criticas:
        df = df.dropna(subset=columnas_criticas)
    # Opcional: filtrar ventas no positivas
    df = df[df["ventas"] > 0]
    return df

df = load_data()




