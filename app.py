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

# --- CSS para diseño moderno tipo "app de turismo" con pestañas más profesionales ---
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    
    /* Mejora en el espaciado y diseño de las pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f0f6ff;
        padding: 10px 10px 0 10px;
        border-radius: 12px 12px 0 0;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Estilo mejorado para las pestañas individuales */
    .stTabs [data-baseweb="tab"] {
        background-color: #e6f2ff; 
        border-radius: 10px 10px 0 0; 
        padding: 14px 24px;  /* Corregido: añadido punto y coma */
        font-size: 18px;
        font-weight: 500;
        font-family: Arial, sans-serif;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    /* Estilo mejorado para la pestaña activa */
    .stTabs [aria-selected="true"] {
        background-color: #4a86e8; 
        color: white;
        font-weight: 600;
        font-family: Arial, sans-serif;
        border-bottom: 2px solid #1a56db;
        box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-4px);
    }
    
    /* Hover effect para las pestañas */
    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        background-color: #d0e3fc;
        border-bottom: 2px solid #90b4f9;
        cursor: pointer;
    }
    
    /* Contenedor de pestañas con borde mejorado */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: white;
        border-radius: 0 0 12px 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        border-top: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* Resto de tus estilos existentes */
    h1 {
        color: #1a365d; 
        font-weight: 800; 
        margin-bottom: 0.5em;
        font-family: Arial, sans-serif;
    }
    h2 {
        color: #2a4365; 
        font-weight: 700;
        font-family: Arial, sans-serif;
    }
    h3 {
        color: #2c5282; 
        font-weight: 600;
        font-family: Arial, sans-serif;
    }
    .stMarkdown {
        line-height: 1.8;
        font-family: Arial, sans-serif;
    }
    div.block-container {padding-top: 2rem;}
    .insight-card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #4a86e8;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: Arial, sans-serif;
    }
    .metric-container {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        font-family: Arial, sans-serif;
    }
    .footer {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-top: 30px;
        border-top: 2px solid #e2e8f0;
        font-family: Arial, sans-serif;
    }

    /* Asegurar que todos los elementos usen Arial */
    .main h1, .main h2, .main h3, .main p, .main span, .main div, .stText {
        font-family: Arial, sans-serif !important;
    }
    
    /* Asegurar que los widgets de Streamlit también usen Arial */
    .stMarkdown, .stButton, .stSelectbox, .stRadio, .stCheckbox, .stSlider, .stText, .stDateInput {
        font-family: Arial, sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# CSS mejorado para pestañas más profesionales y con mejor contraste
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    
    /* Mejora en el espaciado y diseño de las pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #eaf0f9;
        padding: 15px 15px 0 15px;
        border-radius: 12px 12px 0 0;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.08);
        border-bottom: 1px solid #d0d9e6;
    }
    
    /* Estilo mejorado para las pestañas individuales con mejor contraste */
    .stTabs [data-baseweb="tab"] {
        background-color: #d0e0f7; 
        border-radius: 10px 10px 0 0; 
        padding: 16px 28px;
        font-size: 17px;
        font-weight: 600;
        font-family: Arial, sans-serif;
        color: #2c5282;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
        box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.05);
        border: 1px solid #c0d0e9;
        border-bottom: none;
        min-width: 160px;
        text-align: center;
    }
    
    /* Estilo mejorado para la pestaña activa con mayor contraste */
    .stTabs [aria-selected="true"] {
        background-color: #4a86e8; 
        color: white;
        font-weight: 700;
        font-family: Arial, sans-serif;
        border: 1px solid #3a76d8;
        border-bottom: none;
        box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
        position: relative;
        z-index: 10;
        text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.1);
    }
    
    /* Pestaña activa con indicador en la parte inferior */
    .stTabs [aria-selected="true"]::after {
        content: "";
        position: absolute;
        bottom: -2px;
        left: 0;
        right: 0;
        height: 4px;
        background-color: #4a86e8;
        border-radius: 0 0 4px 4px;
    }
    
    /* Hover effect para las pestañas con mejor feedback visual */
    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        background-color: #e2ecf9;
        border: 1px solid #a0c0e9;
        border-bottom: none;
        transform: translateY(-2px);
        cursor: pointer;
        color: #1a4b91;
    }
    
    /* Contenedor de pestañas con borde mejorado */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: white;
        border-radius: 0 0 12px 12px;
        padding: 25px;
        border: 1px solid #d0d9e6;
        border-top: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        position: relative;
        top: -1px;
    }

    /* Iconos de pestañas con mejor posición y tamaño */
    .stTabs [data-baseweb="tab"] span {
        display: inline-block;
        margin-right: 8px;
        font-size: 18px;
        vertical-align: middle;
    }

    /* Resto de tus estilos existentes */
    h1 {
        color: #1a365d; 
        font-weight: 800; 
        margin-bottom: 0.5em;
        font-family: Arial, sans-serif;
    }
    h2 {
        color: #2a4365; 
        font-weight: 700;
        font-family: Arial, sans-serif;
    }
    h3 {
        color: #2c5282; 
        font-weight: 600;
        font-family: Arial, sans-serif;
    }
    .stMarkdown {
        line-height: 1.8;
        font-family: Arial, sans-serif;
    }
    div.block-container {padding-top: 2rem;}
    .insight-card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #4a86e8;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: Arial, sans-serif;
    }
    .metric-container {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        font-family: Arial, sans-serif;
    }
    .footer {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-top: 30px;
        border-top: 2px solid #e2e8f0;
        font-family: Arial, sans-serif;
    }

    /* Asegurar que todos los elementos usen Arial */
    .main h1, .main h2, .main h3, .main p, .main span, .main div, .stText {
        font-family: Arial, sans-serif !important;
    }
    
    /* Asegurar que los widgets de Streamlit también usen Arial */
    .stMarkdown, .stButton, .stSelectbox, .stRadio, .stCheckbox, .stSlider, .stText, .stDateInput {
        font-family: Arial, sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Definir constantes de estilo para mantener consistencia
HEADING_FONT = "font-family: Arial, sans-serif; font-weight: 700; color: #1a365d;"
BODY_FONT = "font-family: Arial, sans-serif; font-weight: 400; color: #2d3748;"
ACCENT_COLOR = "#4a86e8"

# Título principal primero
st.title("📊 Análisis de Ventas - TechNova Retail")

# Banner de autores y descripción después del título
st.markdown(f"""
<div style='background-color: #f9f9fc; border-radius: 8px; box-shadow: 0 2px 8px rgba(76, 110, 245, 0.05); padding: 20px 26px 14px 26px; margin-bottom: 24px;'>
    <p style='{HEADING_FONT} font-size: 20px; margin: 0;'>Desarrollado por: <span style='color:{ACCENT_COLOR};'>Duván, Daniel y Angelo</span></p>
    <span style='{BODY_FONT} font-size: 16px; line-height: 1.6;'>Esta aplicación interactiva analiza los patrones de ventas en TechNova Retail para identificar tendencias clave que pueden mejorar las ofertas y estrategias de marketing de la empresa. Utiliza los filtros a continuación para personalizar el análisis según tus necesidades específicas.</span>
</div>
""", unsafe_allow_html=True)

# --- Modificación: Pestañas más grandes con texto más descriptivo ---
tabs = st.tabs(["📚 **Caso de estudio**", "📊 **Análisis estratégico**"])  # Añadidos emojis y simplificado nombres

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




