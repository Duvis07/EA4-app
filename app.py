import streamlit as st
st.set_page_config(
    page_title="Análisis de Ventas - TechNova Retail",
    page_icon="📊",
    layout="wide"
)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from caso_estudio import mostrar_caso_estudio
    from analisis_estrategico import mostrar_analisis_estrategico
except ImportError:
    mostrar_caso_estudio = None
    mostrar_analisis_estrategico = None

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

# --- Tabs para caso de estudio, visualizaciones y análisis estratégico ---
tabs = st.tabs(["Caso de estudio", "Visualizaciones de ventas", "Análisis Estratégico"])

with tabs[0]:
    if mostrar_caso_estudio:
        st.markdown("""
        <div class='insight-card'>
        <h2>Análisis de Datos para la Optimización de Estrategia Comercial</h2>
        <p>Explora el caso de estudio y descubre cómo se puede aplicar el análisis de ventas en un escenario real.</p>
        </div>
        """, unsafe_allow_html=True)
        mostrar_caso_estudio()
        # Solo texto y conclusiones, nunca gráficos ni insights de ventas
    else:
        st.subheader("Caso de estudio no disponible")
        st.write("No se encontró el módulo 'caso_estudio.py'.")

with tabs[1]:
    st.markdown("""
    <div class='insight-card'>
    <h2>Análisis de Ventas de TechNova Retail</h2>
    <p>Explora los datos de ventas y observa tendencias clave para la toma de decisiones estratégicas.</p>
    </div>
    """, unsafe_allow_html=True)

    import unicodedata
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

    st.markdown(f"""
    <div style="
        max-width: 240px;
        margin: 22px auto 18px auto;
        background: linear-gradient(90deg, #e0e7ff 0%, #f8fafc 100%);
        box-shadow: 0 3px 12px rgba(76, 110, 245, 0.10), 0 0.5px 2px rgba(44, 82, 130, 0.07);
        border-radius: 13px;
        padding: 13px 16px 12px 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        border-left: 5px solid #4a86e8;
        border-right: 1.5px solid #e2e8f0;
    ">
        <div style="font-size: 27px; color: #4a86e8; margin-bottom: 3px; font-weight: 900; letter-spacing: -1px;">📈</div>
        <div style="font-size: 22px; font-weight: 900; color: #1a365d; letter-spacing: -0.5px; line-height: 1;">
            {len(df):,}
        </div>
        <div style="font-size: 13px; color: #2c5282; margin-top: 1px; font-weight: 600; letter-spacing: 0.2px;">
            registros analizados
        </div>
        <div style="font-size:11px; color:#4a5568; margin-top: 2px; text-align:center;">
            <span style='font-style:italic;'>Filas procesadas</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>Ventas Totales por Categoría de Producto</h3>", unsafe_allow_html=True)
        if 'categoria' in df.columns and 'ventas' in df.columns:
            ventas_categoria = df.groupby('categoria')['ventas'].sum().sort_values(ascending=False)
            import matplotlib.ticker as mticker
            import seaborn as sns
            ventas_categoria = ventas_categoria.sort_values(ascending=True)
            fig1, ax1 = plt.subplots(figsize=(8, 4))
            sns.set_style("whitegrid")
            bars = ax1.barh(
                ventas_categoria.index, ventas_categoria.values,
                color=sns.color_palette("crest", len(ventas_categoria)),
                edgecolor="black", linewidth=1.5, height=0.7
            )
            ax1.set_facecolor("#f8f9fa")
            ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
            ax1.set_xlabel("Ventas Totales", fontsize=13, fontweight="bold")
            ax1.set_ylabel("Categoría de Producto", fontsize=13, fontweight="bold")
            for i, v in enumerate(ventas_categoria.values):
                ax1.text(v + max(ventas_categoria.values)*0.01, i, f'${v:,.0f}'.replace(",", "."),
                         color='black', va='center', fontweight='bold', fontsize=13,
                         bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.25', alpha=0.85))
            sns.despine(left=True, bottom=True)
            fig1.tight_layout()
            st.pyplot(fig1)
            # Insight profesional para ventas por categoría
            if len(ventas_categoria) > 1:
                lider = ventas_categoria.index[-1]
                monto_lider = ventas_categoria.values[-1]
                segunda = ventas_categoria.index[-2]
                monto_segunda = ventas_categoria.values[-2]
                diff = int(round(monto_lider - monto_segunda, 0))
                st.markdown(f"""
                <div class='insight-card'>
                <h3>Insight: Ventas Totales por Categoría</h3>
                <p>La categoría líder en ventas es <b>{lider.capitalize()}</b> con <b>${int(monto_lider):,}</b>, superando a <b>{segunda.capitalize()}</b> por <b>${diff:,}</b>. Esto indica una clara preferencia del mercado por esta categoría.</p>
                </div>
                """, unsafe_allow_html=True)
            elif len(ventas_categoria) == 1:
                lider = ventas_categoria.index[0]
                monto_lider = ventas_categoria.values[0]
                st.markdown(f"""
                <div class='insight-card'>
                <h3>Insight: Ventas Totales por Categoría</h3>
                <p>Solo existe una categoría registrada: <b>{lider.capitalize()}</b> con ventas totales de <b>${monto_lider:,.2f}</b>.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No se encontraron las columnas 'categoria' y 'ventas' en el archivo.")

        st.markdown("<h3>Distribución de Ventas</h3>", unsafe_allow_html=True)
        if 'ventas' in df.columns:
            import numpy as np
            from matplotlib import cm
            fig2, ax2 = plt.subplots(figsize=(9, 5))
            sns.set_style("whitegrid")
            # Color degradado para las barras
            cmap = cm.get_cmap('Blues')
            n_bins = 20
            n, bins, patches = ax2.hist(
                df['ventas'].dropna(), bins=n_bins, color=cmap(0.6), alpha=0.85, edgecolor="white", linewidth=2, rwidth=0.92
            )
            for i, patch in enumerate(patches):
                color = cmap(0.3 + 0.7*i/len(patches))
                patch.set_facecolor(color)
            # Línea KDE profesional
            sns.kdeplot(df['ventas'].dropna(), ax=ax2, color="#2c5282", linewidth=3, fill=False, alpha=0.7)
            ax2.set_xlabel("Ventas", fontsize=15, fontweight="bold")
            ax2.set_ylabel("Frecuencia", fontsize=15, fontweight="bold")
            ax2.set_facecolor("#f8f9fa")
            ax2.grid(True, linestyle='--', alpha=0.2)
            # Etiquetas sobre todas las barras
            for rect, freq in zip(patches, n):
                if freq > 0:
                    ax2.text(rect.get_x() + rect.get_width()/2, freq + 2, int(freq), ha='center', va='bottom', fontweight='bold', fontsize=12, color='#2c5282', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.13', alpha=0.8))
            sns.despine(left=True, bottom=True)
            fig2.tight_layout()
            st.pyplot(fig2)
            # Insight profesional para el histograma
            ventas_min = df['ventas'].min()
            ventas_max = df['ventas'].max()
            ventas_mediana = df['ventas'].median()
            ventas_p25 = df['ventas'].quantile(0.25)
            ventas_p75 = df['ventas'].quantile(0.75)
            st.markdown(f"""
            <div class='insight-card'>
            <h3>Insight: Distribución de Ventas</h3>
            <p>La mayoría de las ventas ({(df['ventas'] <= ventas_p75).mean()*100:.1f}%) están por debajo de <b>${ventas_p75:,.2f}</b>. El 50% central de las ventas se encuentra entre <b>${ventas_p25:,.2f}</b> y <b>${ventas_p75:,.2f}</b>. El valor mediano es <b>${ventas_mediana:,.2f}</b>. El rango completo va de <b>${ventas_min:,.2f}</b> a <b>${ventas_max:,.2f}</b>.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No se encontró la columna 'ventas' en el archivo.")

    with col2:
        st.markdown("<h3>Evolución de Ventas en el Tiempo</h3>", unsafe_allow_html=True)
        if 'fecha' in df.columns and 'ventas' in df.columns:
            import matplotlib.dates as mdates
            ventas_tiempo = df.groupby('fecha')['ventas'].sum().sort_index()
            rolling = ventas_tiempo.rolling(window=7, min_periods=1).mean()
            fig3, ax3 = plt.subplots(figsize=(9, 4))
            sns.set_style("whitegrid")
            ax3.plot(ventas_tiempo.index, ventas_tiempo.values, color="#2c5282", linewidth=1.5, label="Ventas diarias")
            ax3.plot(rolling.index, rolling.values, color="#4a86e8", linewidth=2.5, linestyle="--", label="Promedio móvil (7 días)")
            ax3.set_xlabel("Fecha", fontsize=13, fontweight="bold")
            ax3.set_ylabel("Ventas Totales", fontsize=13, fontweight="bold")
            ax3.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax3.grid(True, linestyle='--', alpha=0.3)
            # Pico máximo destacado
            max_idx = ventas_tiempo.idxmax()
            max_val = ventas_tiempo.max()
            ax3.scatter([max_idx], [max_val], color="crimson", s=100, zorder=5)
            ax3.annotate(f"Máximo: ${max_val:,.0f}".replace(",", "."),
                         xy=(max_idx, max_val), xytext=(30, -40),
                         textcoords="offset points", arrowprops=dict(arrowstyle="->", color="crimson", lw=2),
                         fontsize=12, color="crimson", fontweight="bold", bbox=dict(facecolor='white', alpha=0.9, boxstyle='round,pad=0.2'))
            fig3.autofmt_xdate()
            sns.despine(left=True, bottom=True)
            fig3.tight_layout()
            ax3.legend()
            st.pyplot(fig3)
            # Formatear fechas solo como mes y año
            fecha_inicio = pd.to_datetime(ventas_tiempo.index[0]).strftime('%B %Y')
            fecha_fin = pd.to_datetime(ventas_tiempo.index[-1]).strftime('%B %Y')
            porcentaje = (ventas_tiempo.values[-1] - ventas_tiempo.values[0]) / ventas_tiempo.values[0] * 100
            st.markdown(f"""
            <div class='insight-card'>
            <h3>Insight: Evolución de Ventas</h3>
            <p>Las ventas han aumentado un {porcentaje:.2f}% desde <b>{fecha_inicio}</b> hasta <b>{fecha_fin}</b>.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No se encontraron las columnas 'fecha' y 'ventas' en el archivo.")

        st.markdown("<h3>Distribución de Ventas por Categoría</h3>", unsafe_allow_html=True)
        if 'categoria' in df.columns and 'ventas' in df.columns:
            fig4, ax4 = plt.subplots(figsize=(9, 5))
            sns.set_style("whitegrid")
            # Dispersión profesional: puntos grandes, alpha, color por categoría, jitter, líneas de mediana
            sns.stripplot(x='categoria', y='ventas', data=df, jitter=0.28, size=9, alpha=0.45, ax=ax4,
                         palette="crest", edgecolor='k', linewidth=0.8)
            # Línea de mediana por categoría
            cats = df['categoria'].unique()
            for i, cat in enumerate(cats):
                mediana = df[df['categoria'] == cat]['ventas'].median()
                ax4.hlines(mediana, i-0.25, i+0.25, colors='#2c5282', linestyles='--', linewidth=3, label=f"Mediana {cat}" if i==0 else "")
            ax4.set_xlabel("Categoría de Producto", fontsize=15, fontweight="bold")
            ax4.set_ylabel("Ventas", fontsize=15, fontweight="bold")
            ax4.set_facecolor("#f8f9fa")
            ax4.grid(True, linestyle='--', alpha=0.2)
            plt.xticks(rotation=28, ha='right', fontsize=13)
            plt.yticks(fontsize=13)
            sns.despine(left=True, bottom=True)
            fig4.tight_layout()
            st.pyplot(fig4)
            # Insight avanzado y comparativo para dispersión por categoría (ahora sí, justo debajo del gráfico de dispersión)
            dispersions = df.groupby('categoria')['ventas'].std().sort_values(ascending=False)
            rango = df.groupby('categoria')['ventas'].agg(lambda x: x.max()-x.min())
            top_disp_cat = dispersions.index[0]
            top_disp_val = dispersions.iloc[0]
            top_rango = rango[top_disp_cat]
            ejemplo_max = df[df['categoria'] == top_disp_cat]['ventas'].max()
            ejemplo_min = df[df['categoria'] == top_disp_cat]['ventas'].min()
            low_disp_cat = dispersions.index[-1]
            low_disp_val = dispersions.iloc[-1]
            low_rango = rango[low_disp_cat]
            ejemplo_max_low = df[df['categoria'] == low_disp_cat]['ventas'].max()
            ejemplo_min_low = df[df['categoria'] == low_disp_cat]['ventas'].min()
            interpretacion = (f"La alta dispersión en <b>{top_disp_cat.capitalize()}</b> puede indicar una oferta diversa y oportunidades para potenciar productos exitosos, pero también sugiere inconsistencia en ventas que debe analizarse. "
                              f"En contraste, <b>{low_disp_cat.capitalize()}</b> muestra ventas mucho más concentradas, lo que puede facilitar la predicción y planeación.")
            st.markdown(f"""
            <div class='insight-card'>
            <h3>Insight: Distribución de Ventas por Categoría</h3>
            <ul>
                <li><b>Mayor dispersión:</b> {top_disp_cat.capitalize()} (std: ${top_disp_val:,.2f}, rango: ${top_rango:,.2f}, de ${ejemplo_min:,.2f} a ${ejemplo_max:,.2f})</li>
                <li><b>Menor dispersión:</b> {low_disp_cat.capitalize()} (std: ${low_disp_val:,.2f}, rango: ${low_rango:,.2f}, de ${ejemplo_min_low:,.2f} a ${ejemplo_max_low:,.2f})</li>
            </ul>
            <p>{interpretacion}</p>
            </div>
            """, unsafe_allow_html=True)

    # Mostrar la gráfica de tendencia de edad promedio solo en la pestaña de visualizaciones
    st.markdown("<hr style='margin:40px 0 20px 0;border: none; border-top: 2px solid #4a86e8;background: none;' />", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Tendencia de Edad Promedio de los Clientes</h3>", unsafe_allow_html=True)

    # Validación de columnas necesarias
    if 'fecha' in df.columns and 'edad_cliente' in df.columns:
        
        # Centrar gráfico
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            # Preprocesamiento
            df_fecha_edad = df.copy()
            df_fecha_edad['fecha'] = pd.to_datetime(df_fecha_edad['fecha'])
            df_fecha_edad['año_mes'] = df_fecha_edad['fecha'].dt.to_period('M')

            # Agrupación por mes y cálculo de edad promedio
            edad_media = df_fecha_edad.groupby('año_mes')['edad_cliente'].mean()

            # Visualización
            fig_edad, ax_edad = plt.subplots(figsize=(9, 4))
            sns.set_style("whitegrid")

            # Línea de edad promedio
            ax_edad.plot(
                edad_media.index.astype(str), 
                edad_media.values, 
                marker='o', 
                color="#4a86e8", 
                linewidth=2.5, 
                label="Edad promedio"
            )

            # Línea de tendencia
            x = np.arange(len(edad_media))
            z = np.polyfit(x, edad_media.values, 1)
            p = np.poly1d(z)
            ax_edad.plot(
                edad_media.index.astype(str), 
                p(x), 
                color="#2c5282", 
                linestyle="--", 
                linewidth=2, 
                label="Tendencia"
            )

            # Etiquetas y estilo
            ax_edad.set_xlabel("Mes", fontsize=13, fontweight="bold")
            ax_edad.set_ylabel("Edad Promedio", fontsize=13, fontweight="bold")
            ax_edad.grid(True, linestyle='--', alpha=0.2)
            ax_edad.legend()
            fig_edad.tight_layout()
            st.pyplot(fig_edad)

            # Insight
            cambio = edad_media.values[-1] - edad_media.values[0]
            sentido = "aumentado" if cambio > 0 else "disminuido"

            # Formato más legible de fechas (ej. Octubre 2023)
            fecha_inicio = edad_media.index[0].to_timestamp().strftime("%B %Y")
            fecha_fin = edad_media.index[-1].to_timestamp().strftime("%B %Y")

            st.markdown(f"""
            <div class='insight-card' style='margin:auto;max-width:600px; padding: 15px 20px; background-color: #f9f9f9; border-left: 5px solid #4a86e8; border-radius: 8px;'>
                <h3 style='text-align:center; color:#1a365d;'>Insight: Tendencia de Edad</h3>
                <p style='text-align:center; font-size:16px;'>
                    La edad promedio de los clientes ha <b>{sentido}</b> {abs(cambio):.1f} años desde <b>{fecha_inicio}</b> hasta <b>{fecha_fin}</b>.<br>
                    Esto puede reflejar cambios en el perfil demográfico de los compradores.
                </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("No se encontraron las columnas 'fecha' y 'edad_cliente' en el archivo para graficar la tendencia de edad.")

with tabs[2]:
    if mostrar_analisis_estrategico:
        st.markdown("""
        <div class='insight-card'>
        <h2>Análisis Estratégico</h2>
        <p>Visualizaciones avanzadas para el análisis estratégico de ventas y comportamiento del cliente.</p>
        </div>
        """, unsafe_allow_html=True)
        mostrar_analisis_estrategico()
    else:
        st.subheader("Análisis estratégico no disponible")
        st.write("No se encontró el módulo 'analisis_estrategico.py'.")


