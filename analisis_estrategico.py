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

def mostrar_analisis_estrategico():
    # Definir constantes para estandarizar estilos de fuente
    TITLE_FONT = dict(size=24, color='#1a365d', family='Arial', weight='bold')
    SUBTITLE_FONT = dict(size=20, color='#2c5282', family='Arial', weight='bold')
    AXIS_TITLE_FONT = dict(size=16, color='#2c5282', family='Arial', weight='bold')
    LABEL_FONT = dict(size=14, color='#2d3748', family='Arial')
    LEGEND_FONT = dict(size=14, color='#2c5282', family='Arial')
    ANNOTATION_FONT = dict(size=14, color='#1a365d', family='Arial', weight='bold')
    ACCENT_COLOR = '#4a86e8'
    
    # Estilo CSS para insights
    INSIGHT_STYLE = """
    <style>
    .insight-card {
        font-family: Arial, sans-serif;
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4a86e8;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .insight-card h3 {
        color: #1a365d;
        font-weight: 700;
        font-size: 20px;
        margin-bottom: 15px;
    }
    .insight-card p {
        color: #2d3748;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    .insight-card b {
        font-weight: 700;
    }
    </style>
    """
    
    # Inyectar estilos CSS para insights
    st.markdown(INSIGHT_STYLE, unsafe_allow_html=True)

    # Cargar datos
    @st.cache_data
    def load_data():
        try:
            df = pd.read_excel("static/Ventas_Minoristas.xlsx")

        except Exception as e:
            st.error(f"Error al cargar el archivo: {str(e)}")
            return pd.DataFrame()
        
        # Renombrar columnas para quitar espacios y caracteres especiales
        rename_dict = {
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
            "calificación_satisfaccion": "satisfaccion"  # Este es el correcto
        }
        
        # Aplicar el renombramiento
        df = df.rename(columns=rename_dict)
        
        # Limpiar strings: minúsculas, sin tildes, sin espacios extras
        def limpiar_texto(x):
            if isinstance(x, str):
                x = x.strip().lower()
                # Solo quitamos tildes y caracteres especiales para la mayoría de los campos
                x = unicodedata.normalize('NFKD', x).encode('ascii', errors='ignore').decode('utf-8')
                return x
            return x
        
        # Función especial de mapeo para países para asegurar compatibilidad con los mapas
        def normalizar_pais(nombre_pais):
            if not isinstance(nombre_pais, str):
                return nombre_pais
                
            nombre_pais = nombre_pais.strip().lower()
            
            # Diccionario de mapeo para países comunes que pueden tener problemas
            mapeo_paises = {
                'espana': 'Spain',
                'españa': 'Spain',
                'espa\xf1a': 'Spain',
                'espanya': 'Spain',
                'spain': 'Spain',
                'mexico': 'Mexico',
                'méxico': 'Mexico',
                'peru': 'Peru',
                'perú': 'Peru',
                'argentina': 'Argentina',
                'chile': 'Chile',
                'colombia': 'Colombia',
                'venezuela': 'Venezuela',
                'brasil': 'Brazil',
                'brazil': 'Brazil'
            }
            
            # Devolver el nombre de país normalizado si existe en el mapeo
            return mapeo_paises.get(nombre_pais, nombre_pais.title())
                
        # Aplicar limpieza a columnas de texto comunes
        for col in ["categoria", "ciudad", "metodo_pago", "genero_cliente", "nombre_producto"]:
            if col in df.columns:
                df[col] = df[col].apply(limpiar_texto)
        
        # Aplicar la normalización especial para países
        if "pais" in df.columns:
            df["pais"] = df["pais"].apply(normalizar_pais)

        # Corregir tipos numéricos
        df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
        df["precio_unitario_usd"] = pd.to_numeric(df["precio_unitario_usd"], errors="coerce")
        df["edad_cliente"] = pd.to_numeric(df["edad_cliente"], errors="coerce")
        
        # Procesar la columna de satisfacción
        if "satisfaccion" in df.columns:
            df["satisfaccion"] = pd.to_numeric(df["satisfaccion"], errors="coerce")
        else:
            # Si la columna no existe, buscarla silenciosamente con otros nombres posibles
            for col in df.columns:
                if "satisfac" in col.lower():
                    df = df.rename(columns={col: "satisfaccion"})
                    df["satisfaccion"] = pd.to_numeric(df["satisfaccion"], errors="coerce")
                    break
            else:
                # Si no se encuentra, usar valor neutral sin mostrar advertencia
                df["satisfaccion"] = 3.0  # Valor neutral por defecto
        
        # Crear columna de ventas
        df["ventas"] = df["cantidad"] * df["precio_unitario_usd"]
        
        # Quitar filas con datos faltantes críticos
        columnas_criticas = ["cantidad", "precio_unitario_usd", "ventas", "categoria", "fecha"]
        df = df.dropna(subset=columnas_criticas)
        
        # Filtrar ventas no positivas
        df = df[df["ventas"] > 0]
        
        # Asegurar que fecha sea datetime
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        
        return df

    df = load_data()
    
    if df.empty:
        st.error("No se pudieron cargar los datos para el análisis estratégico.")
        return
    

    # Crear columna de mes-año para análisis temporales
    df["mes_ano"] = df["fecha"].dt.strftime('%Y-%m')
    
    # Segmentación por edad para usarla en varios gráficos
    bins = [0, 30, 45, 100]
    labels = ['<30', '30-45', '>45']
    df['rango_edad'] = pd.cut(df['edad_cliente'], bins=bins, labels=labels)

    # Sidebar con filtros - Mejorado visualmente
    st.sidebar.markdown("""
    <div style="background: linear-gradient(120deg, #e0e7ff 0%, #f0f6ff 100%); padding: 15px; border-radius: 10px; 
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #4a86e8;">
        <h2 style="color: #1a365d; font-weight: 700; margin-bottom: 15px; text-align: center;">
            🔍 Filtros de Análisis
        </h2>
        <p style="color: #2c5282; font-size: 14px; margin-bottom: 20px; text-align: center;">
            Personaliza tu análisis estratégico seleccionando los parámetros deseados
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtro de países - Simplificado y estandarizado
    st.sidebar.markdown("""
    <div style="background-color: #f8fafc; padding: 10px 15px 5px; border-radius: 8px; margin-bottom: 15px; 
    border-left: 3px solid #4a86e8; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <h3 style="color: #2c5282; font-size: 16px; font-weight: 600; margin-bottom: 5px;">
            🌎 Países
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # Obtener lista de países con datos
    paises_disponibles = sorted(df["pais"].unique())

    # Selección por defecto - todos los países
    default_paises = paises_disponibles  # Por defecto seleccionar todos los países

    # Multiselect simple, igual que las otras categorías
    paises_seleccionados = st.sidebar.multiselect(
        "Seleccione uno o varios países",
        options=paises_disponibles,
        default=default_paises,
        key="paises_filter"
    )

    # Si no se selecciona ningún país, usar TODOS los países
    if not paises_seleccionados:
        paises_seleccionados = paises_disponibles.copy()
        st.sidebar.info(f"Se han seleccionado todos los países por defecto.")

    # Filtro de categorías - Con estilo mejorado
    st.sidebar.markdown("""
    <div style="background-color: #f8fafc; padding: 10px 15px 5px; border-radius: 8px; margin: 20px 0 15px 0; 
    border-left: 3px solid #4a86e8; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <h3 style="color: #2c5282; font-size: 16px; font-weight: 600; margin-bottom: 5px;">
            📊 Categorías de Producto
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Cambiar cómo funciona el filtro de categorías
    categorias_disponibles = sorted(df["categoria"].unique())
    categorias_seleccionadas = st.sidebar.multiselect(
        "Seleccione una o varias categorías",
        options=categorias_disponibles,
        default=categorias_disponibles,  # Por defecto, todas seleccionadas
        key="categorias_filter"
    )
    
    # Si no se selecciona ninguna categoría, usar TODAS las categorías disponibles
    if not categorias_seleccionadas:
        categorias_seleccionadas = categorias_disponibles.copy()
        st.sidebar.info(f"Se han seleccionado todas las categorías por defecto.")

    # Filtro de rango de fechas - Con estilo mejorado
    st.sidebar.markdown("""
    <div style="background-color: #f8fafc; padding: 10px 15px 5px; border-radius: 8px; margin: 20px 0 15px 0; 
    border-left: 3px solid #4a86e8; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <h3 style="color: #2c5282; font-size: 16px; font-weight: 600; margin-bottom: 5px;">
            📅 Período de Análisis
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    min_date = df["fecha"].min().date()
    max_date = df["fecha"].max().date()
    
    fecha_inicio, fecha_fin = st.sidebar.date_input(
        "Seleccione rango de fechas",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        key="date_filter"
    )
    
    # Botón para aplicar filtros con estilo mejorado
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Aplicar filtros automáticamente
    df_filtrado = df.copy()
    
    # Aplicar filtro de países - sin lógica especial para ropa
    if paises_seleccionados:
        df_filtrado = df_filtrado[df_filtrado["pais"].isin(paises_seleccionados)]
    

    # AGREGADA ESTA SECCIÓN QUE FALTABA
    # Aplicar filtro de categorías
    if categorias_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado["categoria"].isin(categorias_seleccionadas)]

    df_filtrado = df_filtrado[(df_filtrado["fecha"].dt.date >= fecha_inicio) & 
                            (df_filtrado["fecha"].dt.date <= fecha_fin)]
    
    # Mostrar indicadores de filtros aplicados
    st.sidebar.markdown("""
    <div style="background: linear-gradient(120deg, #edf2ff 0%, #f0f6ff 100%); padding: 15px; border-radius: 10px; 
    margin-top: 30px; border: 1px dashed #4a86e8;">
        <h3 style="color: #2c5282; font-size: 15px; font-weight: 600; margin-bottom: 10px; text-align: center;">
            ✅ Filtros Aplicados
        </h3>
        <ul style="color: #4a5568; font-size: 13px; margin-left: 0; padding-left: 20px;">
            <li style="margin-bottom: 5px;">Países: <b>{}</b></li>
            <li style="margin-bottom: 5px;">Categorías: <b>{}</b></li>
            <li>Período: <b>{} a {}</b></li>
        </ul>
    </div>
    """.format(
        f"{len(paises_seleccionados)} seleccionados" if paises_seleccionados else "Todos",
        f"{len(categorias_seleccionadas)} seleccionadas" if len(categorias_seleccionadas) < len(categorias_disponibles) else "Todas",
        fecha_inicio.strftime("%d/%m/%Y"), 
        fecha_fin.strftime("%d/%m/%Y")
    ), unsafe_allow_html=True)
    
    # Resumen de datos filtrados con estilo mejorado y animación
    st.markdown(f"""
    <div style="
        max-width: 290px;
        margin: 20px auto 24px auto;
        background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%);
        box-shadow: 0 5px 14px rgba(76, 110, 245, 0.13), 0 1.5px 4px rgba(44, 82, 130, 0.09);
        border-radius: 13px;
        padding: 15px 18px 14px 18px;
        display: flex;
        flex-direction: column;
        align-items: center;
        border-left: 5px solid #4a86e8;
        border-right: 1.5px solid #e2e8f0;
        transform: translateY(0);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    ">
        <div style="font-size: 28px; color: #4a86e8; margin-bottom: 4px; font-weight: 900;">📊</div>
        <div class="animate-counter" style="font-size: 23px; font-weight: 900; color: #1a365d; letter-spacing: -0.7px; line-height: 1.1;">
            {len(df_filtrado):,}
        </div>
        <div style="font-size: 13px; color: #2c5282; margin-top: 3px; font-weight: 600; letter-spacing: 0.25px;">
            transacciones analizadas
        </div>
        <div style="font-size: 11px; color: #4a5568; margin-top: 4px; text-align: center;">
            <span style='font-style: italic;'>Datos del <b>{fecha_inicio.strftime('%d %b %Y')}</b> al <b>{fecha_fin.strftime('%d %b %Y')}</b></span>
        </div>
    </div>
    <style>
        @keyframes countUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .animate-counter {{
            animation: countUp 1.2s ease-out forwards;
        }}
    </style>
    """, unsafe_allow_html=True)

    # 1. Gráfico de Barras Apiladas mejorado: Ventas por categoría desglosado por método de pago
    st.markdown("<h2 style='text-align:center; color:#1a365d; margin-bottom:20px; font-weight:700; font-size:28px; font-family:Arial, sans-serif;'>Ventas por Categoría y Método de Pago</h2>", unsafe_allow_html=True)
    
    # MODIFICADO: Usar solo las categorías filtradas, no todas las categorías originales
    todos_metodos = sorted(df_filtrado["metodo_pago"].unique())
    categorias_filtradas = sorted(df_filtrado["categoria"].unique())

    # MODIFICADO: Crear combinaciones solo con las categorías filtradas
    from itertools import product
    combinaciones_filtradas = pd.DataFrame(
        list(product(categorias_filtradas, todos_metodos)),
        columns=['categoria', 'metodo_pago']
    )
    
    # Hacer groupby con los datos filtrados
    ventas_cat_pago_raw = df_filtrado.groupby(['categoria', 'metodo_pago'])['ventas'].sum().reset_index()
    
    # Hacer merge solo con las categorías filtradas
    ventas_cat_pago = combinaciones_filtradas.merge(
        ventas_cat_pago_raw, 
        on=['categoria', 'metodo_pago'], 
        how='left'
    ).fillna(0)
    
    # Ordenar categorías filtradas por ventas totales
    cat_totals = ventas_cat_pago.groupby('categoria')['ventas'].sum().sort_values(ascending=False)
    cat_order = cat_totals.index.tolist()
    

    # Crear gráfico solo con categorías filtradas
    fig_barras = px.bar(
        ventas_cat_pago,
        x='categoria',
        y='ventas',
        color='metodo_pago',
        color_discrete_sequence=px.colors.qualitative.Bold,
        barmode='stack',
        category_orders={"categoria": cat_order},
        labels={'ventas': 'Ventas totales (USD)', 'categoria': 'Categoría', 'metodo_pago': 'Método de pago'},
        height=600,
        custom_data=['metodo_pago']
    )
    
    fig_barras.update_layout(
        title={
            'text': 'Distribución de Ventas por Categoría y Método de Pago',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': TITLE_FONT
        },
        xaxis_title={
            'text': '<b>Categoría de Producto</b>',
            'font': AXIS_TITLE_FONT
        },
        yaxis_title={
            'text': '<b>Ventas Totales (USD)</b>',
            'font': AXIS_TITLE_FONT
        },
        legend_title={
            'text': '<b>Método de Pago</b>',
            'font': LEGEND_FONT
        },
        font=LABEL_FONT,
        plot_bgcolor='rgba(240,249,255,0.95)',
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial"),
        xaxis=dict(
            tickfont=dict(size=12),
            tickangle=-45
        ),
        yaxis=dict(
            tickfont=dict(size=12),
            tickprefix='$',
            tickformat=',d',
            gridcolor='rgba(200,210,220,0.25)'
        ),
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.03,  # A la derecha, fuera del área del gráfico
            title='<b>Método de Pago</b>',
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(200,210,220,0.5)',
            borderwidth=1
        ),
        margin=dict(l=60, r=30, t=80, b=60),
        shapes=[{
            'type': 'rect',
            'xref': 'paper',
            'yref': 'paper',
            'x0': 0,
            'y0': 0,
            'x1': 1,
            'y1': 1,
            'line': {'width': 2, 'color': 'rgba(200,210,220,0.5)'},
        }]
    )
    
    # Agregar texto con valores totales sobre cada barra
    for categoria in cat_order:
        total = cat_totals[categoria]
        fig_barras.add_annotation(
            x=categoria,
            y=total,
            text=f"${total:,.0f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#1a365d",
            ax=0,
            ay=-40,
            font=dict(size=12, color="#1a365d", family="Arial", weight="bold"),
            bgcolor="white",
            bordercolor="#4a86e8",
            borderwidth=1.5,
            borderpad=4,
            opacity=0.9
        )
    
    # Agregar efectos interactivos
    fig_barras.update_traces(
        hovertemplate='<b>Categoría:</b> %{x}<br><b>Método de Pago:</b> %{customdata[0]}<br><b>Ventas:</b> $%{y:,.2f}<extra></extra>',
        marker=dict(line=dict(width=1, color='white'))
    )
    
    st.plotly_chart(fig_barras, use_container_width=True)
    
    # Insight para barras apiladas
    metodo_principal = ventas_cat_pago.groupby('metodo_pago')['ventas'].sum().idxmax()
    porcentaje_principal = (ventas_cat_pago[ventas_cat_pago['metodo_pago'] == metodo_principal]['ventas'].sum() / 
                          ventas_cat_pago['ventas'].sum() * 100)
    
    cat_principal = ventas_cat_pago.groupby('categoria')['ventas'].sum().idxmax()
    
    # Obtener segundo método de pago más popular
    metodos_ventas = ventas_cat_pago.groupby('metodo_pago')['ventas'].sum().sort_values(ascending=False)
    segundo_metodo = metodos_ventas.index[1] if len(metodos_ventas) > 1 else None
    porcentaje_segundo = (metodos_ventas[1] / metodos_ventas.sum() * 100) if len(metodos_ventas) > 1 else 0
    
    # Calcular crecimiento del método principal vs año anterior si hay datos temporales
    tendencia_texto = ""
    if 'fecha' in df_filtrado.columns:
        df_actual = df_filtrado[df_filtrado['fecha'] >= (df_filtrado['fecha'].max() - pd.Timedelta(days=180))]
        df_anterior = df_filtrado[df_filtrado['fecha'] < (df_filtrado['fecha'].max() - pd.Timedelta(days=180))]
        
        if not df_anterior.empty and not df_actual.empty:
            # Calcular porcentaje actual
            pct_actual = (df_actual[df_actual['metodo_pago'] == metodo_principal]['ventas'].sum() / 
                        df_actual['ventas'].sum() * 100)
            
            # Calcular porcentaje anterior
            pct_anterior = (df_anterior[df_anterior['metodo_pago'] == metodo_principal]['ventas'].sum() / 
                          df_anterior['ventas'].sum() * 100) if df_anterior['ventas'].sum() > 0 else 0
            
            # Calcular diferencia
            if pct_anterior > 0:
                diff = pct_actual - pct_anterior
                tendencia_texto = f" Ha {('aumentado' if diff > 0 else 'disminuido')} un <b>{abs(diff):.1f}%</b> respecto al período anterior."
    
    st.markdown(f"""
    <div class='insight-card'>
    <h3>Insight: Preferencias de Pago</h3>
    <p>El método de pago preferido es <b>{metodo_principal.title()}</b>, representando el <b>{porcentaje_principal:.1f}%</b> 
    del total de ventas.{f" Le sigue <b>{segundo_metodo.title()}</b> con un <b>{porcentaje_segundo:.1f}%</b>." if segundo_metodo else ""}{tendencia_texto}</p>
    
    <p>La categoría con mayor volumen de ventas es <b>{cat_principal.title()}</b>, y muestra una preferencia de pago mediante 
    <b>{ventas_cat_pago[(ventas_cat_pago['categoria'] == cat_principal)].groupby('metodo_pago')['ventas'].sum().idxmax().title()}</b>.</p>
    
    <p><b>Implicaciones estratégicas:</b></p>
    <ul>
        <li>Optimizar la experiencia de <b>{metodo_principal.title()}</b> para agilizar el proceso de compra.</li>
        <li>Considerar promociones especiales para impulsar métodos de pago alternativos como 
        {segundo_metodo.title() if segundo_metodo else "tarjetas de crédito"}.</li>
        <li>Desarrollar campañas específicas que vinculen la categoría <b>{cat_principal.title()}</b> con 
        beneficios exclusivos según el método de pago.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Heatmap mejorado: Correlación entre variables clave
    st.markdown("<h2 style='text-align:center; color:#1a365d; margin-bottom:20px; margin-top:40px; font-weight:700; font-size:28px; font-family:Arial, sans-serif;'>Correlación entre Variables Clave</h2>", unsafe_allow_html=True)
    
    # Seleccionar columnas numéricas para correlación
    cols_disponibles = ['edad_cliente', 'cantidad', 'precio_unitario_usd', 'ventas', 'satisfaccion']
    
    # Verificar que existan en el DataFrame
    cols_correlacion = [col for col in cols_disponibles if col in df_filtrado.columns]
    
    # Asegurarse de que haya al menos dos columnas para calcular correlaciones
    if len(cols_correlacion) >= 2:
        matriz_corr = df_filtrado[cols_correlacion].corr().round(2)
        
        # Crear heatmap mejorado con plotly
        nombre_variables = {
            'edad_cliente': 'Edad',
            'cantidad': 'Cantidad',
            'precio_unitario_usd': 'Precio',
            'ventas': 'Ventas',
            'satisfaccion': 'Satisfacción'
        }
        
        # Transformar etiquetas para mejor visualización
        etiquetas_x = [nombre_variables.get(col, col) for col in matriz_corr.columns]
        etiquetas_y = [nombre_variables.get(col, col) for col in matriz_corr.index]
        
        # Crear máscara para la matriz triangular superior (incluyendo diagonal)
        mask = np.zeros_like(matriz_corr, dtype=bool)
        mask[np.triu_indices_from(mask, 0)] = True
        matriz_corr_lower = matriz_corr.mask(mask)
        
        # Crear heatmap con diseño mejorado
        fig_heatmap = px.imshow(
            matriz_corr_lower,
            text_auto=True,
            color_continuous_scale='RdBu_r',  # Escala rojo-azul, mejor para correlaciones
            labels=dict(color="Coeficiente"),
            x=etiquetas_x,
            y=etiquetas_y,
            zmin=-1,
            zmax=1,
            height=600,
            aspect="auto"
        )
        
        fig_heatmap.update_layout(
            title={
                'text': 'Matriz de Correlación entre Variables Clave',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': TITLE_FONT
            },
            xaxis={'title': ''},
            yaxis={'title': ''},
            font=LABEL_FONT,
            plot_bgcolor='rgba(240,249,255,0.95)',
            coloraxis_colorbar=dict(
                title=dict(text="<b>Correlación</b>", font=LEGEND_FONT),
                # titlefont=dict(size=14),  # Esta línea causa el error - eliminada
                ticks="outside",
                tickfont=dict(size=12),
                len=0.6,
                thickness=20,
                outlinewidth=1,
                outlinecolor='rgba(200,210,220,0.5)',
                x=1.1
            ),
        )
        
        # Mejorar texto y formato
        fig_heatmap.update_traces(
            text=[[f'{val:.2f}' if not np.isnan(val) else '' for val in row] for row in matriz_corr_lower.values],
            texttemplate='%{text}',
            textfont=dict(size=12, family='Arial', color='black'),
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlación: %{z:.3f}<extra></extra>'
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Insight para heatmap
        try:
            max_corr = matriz_corr.unstack().sort_values().drop_duplicates().tail(2).index[0]
            if len(max_corr) == 2 and max_corr[0] != max_corr[1]:
                max_val = matriz_corr.loc[max_corr[0], max_corr[1]]
                max_var1, max_var2 = max_corr
                
                # Obtener nombres legibles de las variables
                max_var1_nombre = nombre_variables.get(max_var1, max_var1)
                max_var2_nombre = nombre_variables.get(max_var2, max_var2)
                
                # Buscar la segunda correlación más fuerte
                second_corr = matriz_corr.unstack().sort_values().drop_duplicates().tail(3).index[1]
                if len(second_corr) == 2 and second_corr[0] != second_corr[1]:
                    second_val = matriz_corr.loc[second_corr[0], second_corr[1]]
                    second_var1, second_var2 = second_corr
                    second_var1_nombre = nombre_variables.get(second_var1, second_var1)
                    second_var2_nombre = nombre_variables.get(second_var2, second_var2)
                
                # Determinar fuerza de la correlación
                def evaluar_correlacion(val):
                    abs_val = abs(val)
                    if abs_val > 0.7:
                        return "muy fuerte"
                    elif abs_val > 0.5:
                        return "fuerte"
                    elif abs_val > 0.3:
                        return "moderada"
                    else:
                        return "débil"
                
                fuerza_corr = evaluar_correlacion(max_val)
                
                # Interpretación específica basada en las variables
                interpretacion = ""
                recomendaciones = ""
                
                if (max_var1 == 'precio_unitario_usd' and max_var2 == 'ventas') or (max_var2 == 'precio_unitario_usd' and max_var1 == 'ventas'):
                    if max_val > 0:
                        interpretacion = f"Esta correlación positiva {fuerza_corr} indica que productos con precios más altos generan mayores ingresos, sugiriendo que nuestros clientes valoran la calidad y exclusividad sobre el precio económico."
                        recomendaciones = "<li>Considerar estrategias de <b>premium pricing</b> para maximizar ingresos</li><li>Enfatizar el valor y calidad en la comunicación de marketing</li><li>Evaluar oportunidades para introducir productos de gama alta</li>"
                    else:
                        interpretacion = f"Esta correlación negativa {fuerza_corr} sugiere que los precios más bajos impulsan mayor volumen de ventas, indicando sensibilidad al precio en nuestro mercado."
                        recomendaciones = "<li>Implementar estrategias de precios competitivos</li><li>Considerar promociones y descuentos tácticos</li><li>Optimizar costos para mantener márgenes con precios más bajos</li>"
                
                elif (max_var1 == 'satisfaccion' and max_var2 == 'ventas') or (max_var2 == 'satisfaccion' and max_var1 == 'ventas'):
                    if max_val > 0:
                        interpretacion = f"La correlación positiva {fuerza_corr} entre satisfacción y ventas confirma que clientes más satisfechos generan mayor valor para el negocio, posiblemente a través de compras repetidas y mayor fidelidad."
                        recomendaciones = "<li>Invertir en mejorar la experiencia del cliente</li><li>Implementar programas de fidelización</li><li>Realizar seguimiento post-venta para aumentar la satisfacción</li>"
                    else:
                        interpretacion = f"La correlación negativa {fuerza_corr} entre satisfacción y ventas es inusual y puede indicar que estamos vendiendo más pero generando experiencias negativas, un riesgo para la sostenibilidad del negocio."
                        recomendaciones = "<li>Revisar urgentemente procesos de atención al cliente</li><li>Investigar causas de insatisfacción en productos de alto volumen</li><li>Equilibrar objetivos de ventas con métricas de satisfacción</li>"
                
                elif (max_var1 == 'edad_cliente' and max_var2 in ['ventas', 'precio_unitario_usd']) or (max_var2 == 'edad_cliente' and max_var1 in ['ventas', 'precio_unitario_usd']):
                    otra_var = max_var2 if max_var1 == 'edad_cliente' else max_var1
                    otra_var_nombre = nombre_variables.get(otra_var, otra_var)
                    
                    if max_val > 0:
                        interpretacion = f"La correlación positiva {fuerza_corr} entre edad y {otra_var_nombre.lower()} sugiere que los clientes de mayor edad tienden a generar {otra_var_nombre.lower()} más altos, posiblemente debido a mayor poder adquisitivo o preferencias de producto diferentes."
                        recomendaciones = "<li>Segmentar ofertas por grupos de edad</li><li>Desarrollar productos premium para el segmento de mayor edad</li><li>Ajustar la comunicación de marketing para resonar con diferentes generaciones</li>"
                    else:
                        interpretacion = f"La correlación negativa {fuerza_corr} entre edad y {otra_var_nombre.lower()} indica que los clientes más jóvenes tienden a generar {otra_var_nombre.lower()} más altos, contrario a la suposición común sobre poder adquisitivo."
                        recomendaciones = "<li>Investigar preferencias específicas del segmento joven</li><li>Revisar estrategia de precios para diferentes segmentos etarios</li><li>Desarrollar campañas específicas para maximizar valor en segmentos de mayor edad</li>"
                
                # Insight final más completo
                st.markdown(f"""
                <div class='insight-card'>
                <h3>Insight: Correlaciones Significativas</h3>
                <p>La correlación más fuerte es entre <b>{max_var1_nombre}</b> y <b>{max_var2_nombre}</b> (r = {max_val:.2f}), 
                lo que representa una relación <b>{fuerza_corr}</b> entre estas variables.</p>
                
                <p>{interpretacion}</p>
                
                
                <p><b>Implicaciones para el negocio:</b></p>
                <ul>
                    {recomendaciones if recomendaciones else "<li>Utilizar esta correlación para refinar estrategias de precios</li><li>Segmentar campañas de marketing basadas en esta relación</li><li>Monitorear estas variables clave para predecir tendencias de ventas</li>"}
                </ul>
                </div>
                """, unsafe_allow_html=True)
        except (IndexError, KeyError):
            st.markdown("""
            <div class='insight-card'>
            <h3>Insight: Correlaciones</h3>
            <p>No se identificaron correlaciones significativas entre las variables analizadas.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No hay suficientes columnas numéricas para calcular correlaciones.")

    # 3. Boxplot mejorado: Comparar distribución de precios por categoría
    st.markdown("<h2 style='text-align:center; color:#1a365d; margin-bottom:20px; margin-top:40px; font-weight:700; font-size:28px; font-family:Arial, sans-serif;'>Distribución de Precios por Categoría</h2>", unsafe_allow_html=True)
    
    # Ordenar categorías por precio mediano para mejor visualización
    cat_median = df_filtrado.groupby('categoria')['precio_unitario_usd'].median().sort_values(ascending=False)
    cat_order_price = cat_median.index.tolist()
    
    # Crear paleta de colores personalizada
    n_cats = len(cat_order_price)
    colors = px.colors.qualitative.Vivid[:n_cats] if n_cats <= len(px.colors.qualitative.Vivid) else px.colors.qualitative.Vivid
    
    fig_boxplot = px.box(
        df_filtrado,
        x="categoria",
        y="precio_unitario_usd",
        color="categoria",
        category_orders={"categoria": cat_order_price},
        points="outliers",  # Solo mostrar outliers para reducir carga visual
        notched=True,  # Agregar muescas para mejor comparación visual
        color_discrete_sequence=colors,
        labels={
            'precio_unitario_usd': 'Precio Unitario (USD)',
            'categoria': 'Categoría'
        },
        height=600
    )
    
    # Agregar violin plot superpuesto para ver distribución completa
    fig_violin = px.violin(
        df_filtrado,
        x="categoria",
        y="precio_unitario_usd",
        color="categoria",
        category_orders={"categoria": cat_order_price},
        color_discrete_sequence=colors,
        # opacity=0.2,  # Esta línea causa el error - eliminada
        box=False,
    )
    
    # Crear copia de las trazas violín con opacidad personalizada manualmente
    violin_traces = []
    for trace in fig_violin.data:
        # Crear una copia del trace original
        new_trace = go.Violin(
            x=trace.x,
            y=trace.y,
            name=trace.name,
            legendgroup=trace.legendgroup,
            scalegroup=trace.scalegroup,
            side=trace.side,
            line=trace.line,
            fillcolor=trace.fillcolor,
            marker=trace.marker,
            hoverinfo="skip",  # Ocultar información de hover para el violín
            showlegend=False,  # No mostrar en leyenda
            opacity=0.2  # Aquí aplicamos la opacidad directamente
        )
        violin_traces.append(new_trace)
    
    # Combinar gráficos (primero los violines con opacidad, luego el boxplot)
    for trace in violin_traces:
        fig_boxplot.add_trace(trace)
    
    # Agregar mediana y promedio como anotaciones
    precio_stats = df_filtrado.groupby('categoria')['precio_unitario_usd'].agg(['median', 'mean']).reset_index()
    
    for i, row in precio_stats.iterrows():
        fig_boxplot.add_annotation(
            x=row['categoria'],
            y=row['median'],
            text=f"Mediana: ${row['median']:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            ax=-40,
            ay=0,
            font=dict(size=10, color="#1a365d"),
            bgcolor="white",
            bordercolor="#4a86e8",
            borderwidth=1,
            borderpad=3,
            opacity=0.9
        )
    
    fig_boxplot.update_layout(
        title={
            'text': 'Distribución de Precios por Categoría de Producto',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': TITLE_FONT
        },
        xaxis_title={
            'text': '<b>Categoría de Producto</b>',
            'font': AXIS_TITLE_FONT
        },
        yaxis_title={
            'text': '<b>Precio Unitario (USD)</b>',
            'font': AXIS_TITLE_FONT
        },
        font=LABEL_FONT,
        showlegend=False,
        plot_bgcolor='rgba(240,249,255,0.95)',
        xaxis={'categoryorder': 'array', 'categoryarray': cat_order_price, 'tickangle': -45},
        yaxis=dict(
            tickfont=dict(size=12),
            tickprefix='$',
            gridcolor='rgba(200,210,220,0.25)',
            zeroline=True,
            zerolinecolor='rgba(0,0,0,0.2)',
            zerolinewidth=1
        ),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"),
        margin=dict(l=60, r=20, t=80, b=120)
    )
    
    # Agregar efectos interactivos
    fig_boxplot.update_traces(
        hovertemplate='<b>%{x}</b><br>Precio: $%{y:.2f}<extra></extra>',
        marker=dict(opacity=0.7)
    )
    
    st.plotly_chart(fig_boxplot, use_container_width=True)
    
    # Insight para boxplot
    # Cálculo dinámico de estadísticas por categoría con mejor separación de variables
    precio_stats = df_filtrado.groupby('categoria')['precio_unitario_usd'].agg(['median', 'mean', 'std', 'min', 'max'])
    categoria_mas_cara = precio_stats['median'].idxmax()
    categoria_mas_barata = precio_stats['median'].idxmin()
    categoria_mas_variada = precio_stats['std'].idxmax()

    # Si tenemos 3 categorías, asegurémonos de mostrar las tres
    todas_categorias = sorted(precio_stats.index)
    categoria_media = None

    if len(todas_categorias) == 3:
        # Identificar la categoría que no es ni la más cara ni la más barata
        for cat in todas_categorias:
            if cat != categoria_mas_cara and cat != categoria_mas_barata:
                categoria_media = cat
                break

    # Crear texto de comparación más informativo evitando repeticiones
    comparacion_texto = ""
    if categoria_mas_cara != categoria_mas_variada:
        comparacion_texto = f"La categoría <b>{categoria_mas_cara.title()}</b> tiene el precio mediano más alto (${precio_stats.loc[categoria_mas_cara, 'median']:.2f}), " + \
                          f"mientras que <b>{categoria_mas_variada.title()}</b> muestra la mayor variabilidad de precios " + \
                          f"(desviación estándar de ${precio_stats.loc[categoria_mas_variada, 'std']:.2f})."
    else:
        # Encontrar la segunda categoría con mayor variabilidad para evitar redundancia
        segunda_mas_variada = precio_stats['std'].nlargest(2).index[1] if len(precio_stats) > 1 else None
        
        comparacion_texto = f"La categoría <b>{categoria_mas_cara.title()}</b> tiene el precio mediano más alto (${precio_stats.loc[categoria_mas_cara, 'median']:.2f}). "
        
        if segunda_mas_variada:
            comparacion_texto += f"Además, muestra la mayor variabilidad de precios (desv. estándar de ${precio_stats.loc[categoria_mas_cara, 'std']:.2f}), " + \
                              f"seguida por <b>{segunda_mas_variada.title()}</b> (desv. estándar de ${precio_stats.loc[segunda_mas_variada, 'std']:.2f})."
        else:
            comparacion_texto += f"También muestra la mayor variabilidad de precios (desv. estándar de ${precio_stats.loc[categoria_mas_cara, 'std']:.2f})."

    # Añadir comparación con la categoría más barata
    rango_precios = f"El rango de precios va desde <b>{categoria_mas_barata.title()}</b> (${precio_stats.loc[categoria_mas_barata, 'median']:.2f}) " + \
                    f"hasta <b>{categoria_mas_cara.title()}</b> (${precio_stats.loc[categoria_mas_cara, 'median']:.2f}), " + \
                    f"una diferencia de ${precio_stats.loc[categoria_mas_cara, 'median'] - precio_stats.loc[categoria_mas_barata, 'median']:.2f}."

    # Construir recomendaciones para todas las categorías disponibles sin redundancia
    recomendaciones_html = "<ul>"

    # Siempre incluimos recomendaciones para la más cara y la más barata
    recomendaciones_html += f"<li>Para <b>{categoria_mas_cara.title()}</b>: Enfatizar la calidad y exclusividad para justificar los precios más altos.</li>"
    recomendaciones_html += f"<li>Para <b>{categoria_mas_barata.title()}</b>: Utilizar estrategias de volumen y ofertas para maximizar ventas.</li>"

    # Si la categoría más variada no es ni la más cara ni la más barata, incluirla
    if categoria_mas_variada != categoria_mas_cara and categoria_mas_variada != categoria_mas_barata:
        recomendaciones_html += f"<li>Para <b>{categoria_mas_variada.title()}</b>: Segmentar líneas de productos por nivel de precio para diferentes segmentos de mercado.</li>"
    # Si tenemos una categoría media identificada y no la hemos incluido aún
    elif categoria_media and categoria_media != categoria_mas_variada:
        recomendaciones_html += f"<li>Para <b>{categoria_media.title()}</b>: Balancear calidad y precio para posicionarse en el segmento medio del mercado.</li>"

    recomendaciones_html += "</ul>"

    st.markdown(f"""
    <div class='insight-card'>
    <h3>Insight: Estrategia de Precios</h3>
    <p>{comparacion_texto}</p>
    <p>{rango_precios}</p>
    <p><b>Recomendaciones:</b>
    {recomendaciones_html}
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. Gráfico de Líneas: Evolución de satisfacción
    st.markdown("<h2 style='text-align:center; color:#1a365d; margin-bottom:20px; margin-top:40px; font-weight:700; font-size:28px; font-family:Arial, sans-serif;'>Evolución de la Satisfacción del Cliente</h2>", unsafe_allow_html=True)
    
    if 'satisfaccion' in df_filtrado.columns:
        # Calcular satisfacción promedio por mes-año
        satisfaccion_tiempo = df_filtrado.groupby('mes_ano')['satisfaccion'].mean().reset_index()
        
        # Verificar que haya datos después del agrupamiento
        if not satisfaccion_tiempo.empty and len(satisfaccion_tiempo) > 1:
            # Crear un gráfico combinado: línea principal, área sombreada, y punto destacado
            fig_linea = go.Figure()
            
            # Añadir área sombreada bajo la línea
            fig_linea.add_trace(
                go.Scatter(
                    x=satisfaccion_tiempo['mes_ano'],
                    y=satisfaccion_tiempo['satisfaccion'],
                    fill='tozeroy',
                    fillcolor='rgba(74, 134, 232, 0.2)',
                    line=dict(color='rgba(0,0,0,0)'),
                    showlegend=False,
                    hoverinfo='skip'
                )
            )
            
            # Añadir línea de tendencia
            x_numeric = np.arange(len(satisfaccion_tiempo))
            y = satisfaccion_tiempo['satisfaccion'].values
            z = np.polyfit(x_numeric, y, 1)
            p = np.poly1d(z)
            trend_y = p(x_numeric)
            
            fig_linea.add_trace(
                go.Scatter(
                    x=satisfaccion_tiempo['mes_ano'],
                    y=trend_y,
                    mode='lines',
                    line=dict(color='rgba(200, 50, 100, 0.7)', width=2, dash='dash'),
                    name='Tendencia',
                    hovertemplate='Tendencia: %{y:.2f}<extra></extra>'
                )
            )
            
            # Añadir línea principal con marcadores
            fig_linea.add_trace(
                go.Scatter(
                    x=satisfaccion_tiempo['mes_ano'],
                    y=satisfaccion_tiempo['satisfaccion'],
                    mode='lines+markers',
                    line=dict(color='#4a86e8', width=3),
                    marker=dict(
                        size=10,
                        color='#4a86e8',
                        line=dict(color='white', width=2)
                    ),
                    name='Satisfacción',
                    hovertemplate='%{x}<br>Satisfacción: %{y:.2f}/5<extra></extra>'
                )
            )
            
            # Destacar punto máximo
            max_idx = satisfaccion_tiempo['satisfaccion'].idxmax()
            max_mes = satisfaccion_tiempo.loc[max_idx, 'mes_ano']
            max_sat = satisfaccion_tiempo.loc[max_idx, 'satisfaccion']
            
            # Punto destacado
            fig_linea.add_trace(
                go.Scatter(
                    x=[max_mes],
                    y=[max_sat],
                    mode='markers',
                    marker=dict(
                        symbol='star',
                        size=18,
                        color='gold',
                        line=dict(color='black', width=2)
                    ),
                    name='Máxima satisfacción',
                    hovertemplate='%{x}<br>Satisfacción máxima: %{y:.2f}/5<extra></extra>'
                )
            )
            
            # Mejoras visuales del layout
            fig_linea.update_layout(
                title={
                    'text': 'Evolución de la Satisfacción del Cliente a lo Largo del Tiempo',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': TITLE_FONT
                },
                xaxis_title={
                    'text': '<b>Período</b>',
                    'font': AXIS_TITLE_FONT
                },
                yaxis_title={
                    'text': '<b>Satisfacción Promedio (1-5)</b>',
                    'font': AXIS_TITLE_FONT
                },
                font=LABEL_FONT,
                plot_bgcolor='rgba(240,249,255,0.95)',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(200,210,220,0.25)',
                    tickfont=dict(size=12),
                    tickangle=-45
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(200,210,220,0.25)',
                    tickfont=dict(size=12),
                    range=[max(0, min(satisfaccion_tiempo['satisfaccion']) * 0.9), 5.1]
                ),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.25,
                    bgcolor='rgba(255,255,255,0.8)'
                ),
                shapes=[
                    # Línea horizontal en 4/5 (buena satisfacción)
                    dict(
                        type="line",
                        x0=0,
                        y0=4,
                        x1=1,
                        y1=4,
                        xref="paper",
                        line=dict(
                            color="rgba(0, 150, 0, 0.3)",
                            width=2,
                            dash="dot",
                        )
                    ),
                    # Línea horizontal en 3/5 (satisfacción neutral)
                    dict(
                        type="line",
                        x0=0,
                        y0=3,
                        x1=1,
                        y1=3,
                        xref="paper",
                        line=dict(
                            color="rgba(150, 150, 0, 0.3)",
                            width=2,
                            dash="dot",
                        )
                    )
                ],
                annotations=[
                    dict(
                        x=1.02,
                        y=4,
                        xref="paper",
                        yref="y",
                        text="Buena",
                        showarrow=False,
                        font=dict(size=12, color="rgba(0, 150, 0, 0.7)")
                    ),
                    dict(
                        x=1.02,
                        y=3,
                        xref="paper",
                        yref="y",
                        text="Neutral",
                        showarrow=False,
                        font=dict(size=12, color="rgba(150, 150, 0, 0.7)")
                    ),
                ],
                hovermode='x unified',
                margin=dict(l=60, r=400, t=80, b=140),
            )
            
            st.plotly_chart(fig_linea, use_container_width=True)
            
            # Insight para gráfico de líneas
            primer_valor = satisfaccion_tiempo.iloc[0]['satisfaccion']
            ultimo_valor = satisfaccion_tiempo.iloc[-1]['satisfaccion']
            
            # Evitar división por cero
            if primer_valor != 0:
                cambio = ((ultimo_valor - primer_valor) / primer_valor) * 100
            else:
                cambio = 0
                
            tendencia = "positiva" if cambio >= 0 else "negativa"
            signo = "+" if cambio >= 0 else "-"
            
            # Analizar la tendencia reciente (últimos 3 meses si hay suficientes datos)
            tendencia_reciente = ""
            if len(satisfaccion_tiempo) >= 4:
                ultimos_meses = satisfaccion_tiempo.iloc[-3:]
                primer_reciente = ultimos_meses.iloc[0]['satisfaccion']
                ultimo_reciente = ultimos_meses.iloc[-1]['satisfaccion']
                
                if primer_reciente != 0:
                    cambio_reciente = ((ultimo_reciente - primer_reciente) / primer_reciente) * 100
                    if (cambio_reciente >= 0) != (cambio >= 0):  # Si la tendencia reciente es diferente a la general
                        tendencia_reciente = f"<p>Sin embargo, en los últimos 3 meses se observa una tendencia <b>{'positiva' if cambio_reciente >= 0 else 'negativa'}</b> de <b>{abs(cambio_reciente):.1f}%</b>, lo que sugiere un <b>{'cambio favorable' if cambio_reciente >= 0 else 'punto de atención'}</b>.</p>"
            
            max_satisfaccion = satisfaccion_tiempo['satisfaccion'].max()
            mes_max = satisfaccion_tiempo.loc[satisfaccion_tiempo['satisfaccion'] == max_satisfaccion, 'mes_ano'].iloc[0]
            
            # Interpretar nivel de satisfacción
            nivel_texto = ""
            if max_satisfaccion >= 4.5:
                nivel_texto = "excelente"
            elif max_satisfaccion >= 4:
                nivel_texto = "muy bueno"
            elif max_satisfaccion >= 3.5:
                nivel_texto = "bueno"
            elif max_satisfaccion >= 3:
                nivel_texto = "aceptable"
            else:
                nivel_texto = "preocupante"
            
            # Formatear el mes para mostrarlo de forma más legible
            try:
                fecha_obj = datetime.strptime(mes_max, '%Y-%m')
                mes_formateado = fecha_obj.strftime('%B %Y').capitalize()
            except:
                mes_formateado = mes_max
            
            # Calcular meses con tendencias positivas y negativas
            meses_tendencia = []
            for i in range(1, len(satisfaccion_tiempo)):
                actual = satisfaccion_tiempo.iloc[i]['satisfaccion']
                anterior = satisfaccion_tiempo.iloc[i-1]['satisfaccion']
                if actual > anterior:
                    meses_tendencia.append(("positiva", satisfaccion_tiempo.iloc[i]['mes_ano']))
                elif actual < anterior:
                    meses_tendencia.append(("negativa", satisfaccion_tiempo.iloc[i]['mes_ano']))
            
            # Obtener recomendaciones basadas en los datos
            recomendaciones = []
            
            if tendencia == "negativa" and abs(cambio) > 5:
                recomendaciones.append("Realizar encuestas específicas para identificar los factores que están afectando la satisfacción")
                recomendaciones.append("Revisar cambios recientes en productos, servicios o procesos que puedan estar impactando negativamente")
            
            if any(t[0] == "positiva" for t in meses_tendencia):
                recomendaciones.append(f"Analizar las iniciativas implementadas en {', '.join([t[1] for t in meses_tendencia if t[0] == 'positiva'][:2])} para identificar prácticas exitosas")
            
            if max_satisfaccion < 4:
                recomendaciones.append("Implementar un programa integral de mejora de la experiencia del cliente")
                
            if len(recomendaciones) < 3:
                recomendaciones.append("Establecer un sistema de seguimiento continuo de la satisfacción para detectar cambios rápidamente")
            
            st.markdown(f"""
            <div class='insight-card'>
            <h3>Insight: Tendencia de Satisfacción</h3>
            <p>La satisfacción del cliente muestra una tendencia <b>{tendencia}</b> con un cambio del <b>{signo}{abs(cambio):.1f}%</b> 
            durante el período analizado. El mes con mayor satisfacción fue <b>{mes_formateado}</b> con un promedio de <b>{max_satisfaccion:.2f}/5</b>, 
            nivel considerado <b>{nivel_texto}</b>.</p>
            
            {tendencia_reciente}
            
            <p><b>Recomendaciones específicas:</b></p>
            <ul>
                {" ".join(f"<li>{rec}</li>" for rec in recomendaciones)}
            </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Eliminar advertencia y mostrar un espacio vacío
            st.write("")
    else:
        # Eliminar advertencia y mostrar un espacio vacío
        st.write("")

    # 5. Mapa Coroplético: Distribución geográfica
    st.markdown("<h2 style='text-align:center; color:#1a365d; margin-bottom:20px; margin-top:40px; font-weight:700; font-size:28px; font-family:Arial, sans-serif;'>Distribución Geográfica de Ventas</h2>", unsafe_allow_html=True)
    
    ventas_pais = df_filtrado.groupby('pais')['ventas'].sum().reset_index()
    
    # Agregar más métricas para enriquecer el mapa
    metricas_pais = df_filtrado.groupby('pais').agg({
        'ventas': 'sum',
        'cantidad': 'sum',
        'id_cliente': 'nunique'  # Clientes únicos
    }).reset_index()
    
    # Agregar satisfacción promedio si existe
    if 'satisfaccion' in df_filtrado.columns:
        sat_pais = df_filtrado.groupby('pais')['satisfaccion'].mean().reset_index()
        metricas_pais = metricas_pais.merge(sat_pais, on='pais', how='left')
    
    # Calcular ticket promedio
    metricas_pais['ticket_promedio'] = metricas_pais['ventas'] / metricas_pais['id_cliente']


    
    # Crear mapa coroplético interactivo mejorado
    fig_mapa = px.choropleth(
        metricas_pais,
        locations='pais',
        locationmode='country names',
        color='ventas',
        hover_name='pais',
        color_continuous_scale='Plasma',
        range_color=[metricas_pais['ventas'].min(), metricas_pais['ventas'].max()],
        labels={'ventas': 'Ventas Totales (USD)'},
        height=650,
        custom_data=['cantidad', 'id_cliente', 'ticket_promedio'] + 
                  (['satisfaccion'] if 'satisfaccion' in metricas_pais.columns else [])
    )
    
    # Personalizar hover template y agregar debug info para nombres de países
    hover_template = '<b>%{hovertext}</b><br><br>' + \
                    'Ventas: $%{z:,.2f}<br>' + \
                    'Cantidad: %{customdata[0]:,}<br>' + \
                    'Clientes: %{customdata[1]:,}<br>' + \
                    'Ticket Promedio: $%{customdata[2]:,.2f}'
    
    if 'satisfaccion' in metricas_pais.columns:
        hover_template += '<br>Satisfacción: %{customdata[3]:.2f}/5'
        
    hover_template += '<extra></extra>'
    
    # Mostrar países incluidos para debugging
    st.info(f"Países en el análisis: {', '.join(metricas_pais['pais'].tolist())}")
    
    fig_mapa.update_traces(
        hovertemplate=hover_template,
        marker_line_color='white',
        marker_line_width=0.5
    )
    
    fig_mapa.update_layout(
        title={
            'text': 'Distribución Geográfica de Ventas por País',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': TITLE_FONT
        },
        font=LABEL_FONT,
        coloraxis_colorbar=dict(
            title=dict(
                text="<b>Ventas (USD)</b>",
                font=LEGEND_FONT
            ),
            tickprefix="$",
            tickformat=",",
            ticks="outside",
            thickness=12,
            len=0.42,
            bgcolor='rgba(255,255,255,0.93)',
            bordercolor='rgba(200,210,220,0.7)',
            borderwidth=1.5,
            outlinewidth=2,
            outlinecolor='rgba(180,180,180,0.7)',
            tickfont=dict(size=13, color='#1a365d')
        ),
        margin=dict(l=0, r=110, t=80, b=0),
        width=950,
        autosize=False,
        dragmode='pan',
    )
    
    st.plotly_chart(fig_mapa, use_container_width=True)
    
    # Insight para el mapa coroplético de países
    pais_mas_ventas = metricas_pais.loc[metricas_pais['ventas'].idxmax()]
    pais_mayor_ticket = metricas_pais.loc[metricas_pais['ticket_promedio'].idxmax()]
    
    # Calcular totales y participación de mercado
    total_ventas = metricas_pais['ventas'].sum()
    total_clientes = metricas_pais['id_cliente'].sum()
    participacion_principal = (pais_mas_ventas['ventas'] / total_ventas) * 100
    
    # Obtener datos del segundo país más importante
    segundo_pais = metricas_pais.nlargest(2, 'ventas').iloc[1]
    participacion_segundo = (segundo_pais['ventas'] / total_ventas) * 100
    
    # Comparar el ticket promedio del país principal con el promedio general
    ticket_promedio_general = total_ventas / total_clientes
    diferencia_ticket = ((pais_mayor_ticket['ticket_promedio'] / ticket_promedio_general) - 1) * 100
    
    # Generar texto de comparación más informativo
    if pais_mas_ventas['pais'] == pais_mayor_ticket['pais']:
        comparacion_texto = f"<b>{pais_mas_ventas['pais']}</b> lidera tanto en volumen de ventas con <b>${pais_mas_ventas['ventas']:,.2f}</b> ({participacion_principal:.1f}% del total) " + \
                          f"como en ticket promedio con <b>${pais_mas_ventas['ticket_promedio']:,.2f}</b> por cliente, " + \
                          f"un {diferencia_ticket:.1f}% superior al promedio general de ${ticket_promedio_general:.2f}."
    else:
        comparacion_texto = f"El país con mayor volumen de ventas es <b>{pais_mas_ventas['pais']}</b> con <b>${pais_mas_ventas['ventas']:,.2f}</b> " + \
                          f"({participacion_principal:.1f}% del total). Sin embargo, <b>{pais_mayor_ticket['pais']}</b> destaca con el mayor ticket promedio " + \
                          f"de <b>${pais_mayor_ticket['ticket_promedio']:,.2f}</b> por cliente, un {diferencia_ticket:.1f}% superior al promedio general."
    
    # Calcular densidad de ventas (ventas por cantidad de clientes en cada país)
    metricas_pais['densidad_ventas'] = metricas_pais['ventas'] / metricas_pais['id_cliente']
    pais_mayor_densidad = metricas_pais.loc[metricas_pais['densidad_ventas'].idxmax()]
    
    # Generar recomendaciones específicas según los datos
    recomendaciones = []
    
    # Para el país con mayor volumen
    if participacion_principal > 50:
        recomendaciones.append(f"<b>Para {pais_mas_ventas['pais']}</b>: Fortalecer la posición dominante mediante programas de fidelización avanzados y expandir la gama de productos premium.")
    else:
        recomendaciones.append(f"<b>Para {pais_mas_ventas['pais']}</b>: Profundizar penetración de mercado con estrategias de cross-selling y up-selling para incrementar el ticket promedio.")
    
    # Para el país con mayor ticket promedio (si es diferente)
    if pais_mas_ventas['pais'] != pais_mayor_ticket['pais']:
        recomendaciones.append(f"<b>Para {pais_mayor_ticket['pais']}</b>: Capitalizar el alto valor por cliente desarrollando líneas exclusivas y servicios premium adaptados a este mercado.")
    
    # Para el segundo país más importante
    segundo_pais_nombre = 'España' if segundo_pais['pais'] == 'Spain' else segundo_pais['pais']
    recomendaciones.append(f"<b>Para {segundo_pais_nombre}</b>: Implementar campañas específicas para incrementar su participación actual del {participacion_segundo:.1f}%, aprovechando el potencial de crecimiento.")
    
    # Análisis de satisfacción si está disponible
    satisfaccion_info = ""
    if 'satisfaccion' in metricas_pais.columns:
        pais_mejor_satisfaccion = metricas_pais.loc[metricas_pais['satisfaccion'].idxmax()]
        pais_peor_satisfaccion = metricas_pais.loc[metricas_pais['satisfaccion'].idxmin()]
        
        diferencia_satisfaccion = pais_mejor_satisfaccion['satisfaccion'] - pais_peor_satisfaccion['satisfaccion']
        
        # Reemplazar Spain por España en el texto de satisfacción
        pais_mejor_nombre = 'España' if pais_mejor_satisfaccion['pais'] == 'Spain' else pais_mejor_satisfaccion['pais']
        pais_peor_nombre = 'España' if pais_peor_satisfaccion['pais'] == 'Spain' else pais_peor_satisfaccion['pais']
        
        satisfaccion_info = f"""<p>El nivel de satisfacción varía considerablemente entre países, con <b>{pais_mejor_nombre}</b> 
        liderando con <b>{pais_mejor_satisfaccion['satisfaccion']:.2f}/5</b> y <b>{pais_peor_nombre}</b> 
        presentando oportunidades de mejora con <b>{pais_peor_satisfaccion['satisfaccion']:.2f}/5</b> 
        (diferencia de {diferencia_satisfaccion:.2f} puntos).</p>"""
    
    # Reemplazar Spain por España en el segundo mercado más importante
    segundo_pais_texto = 'España' if segundo_pais['pais'] == 'Spain' else segundo_pais['pais']
    
    st.markdown(f"""
    <div class='insight-card'>
    <h3>Insight: Distribución Geográfica de Ventas</h3>
    <p>{comparacion_texto}</p>
    
    <p>El segundo mercado más importante es <b>{segundo_pais_texto}</b> con <b>${segundo_pais['ventas']:,.2f}</b> 
    en ventas totales ({participacion_segundo:.1f}% de participación) y un ticket promedio de <b>${segundo_pais['ticket_promedio']:,.2f}</b>.</p>
    
    {satisfaccion_info}
    
    <p><b>Recomendaciones estratégicas por país:</b></p>
    <ul>
        {" ".join(f"<li>{rec}</li>" for rec in recomendaciones)}
        <li><b>Mercados emergentes</b>: Evaluar la expansión hacia nuevos territorios basándose en similitudes culturales y económicas con los mercados exitosos actuales.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # 6. Mapa de Burbujas mejorado: Combinar con análisis
    ventas_ciudad = df_filtrado.groupby(['pais', 'ciudad']).agg({
        'ventas': 'sum',
        'cantidad': 'sum'
    }).reset_index()
    
    # Agregar satisfacción solo si existe la columna
    if 'satisfaccion' in df_filtrado.columns:
        ventas_ciudad_sat = df_filtrado.groupby(['pais', 'ciudad'])['satisfaccion'].mean().reset_index()
        ventas_ciudad = ventas_ciudad.merge(ventas_ciudad_sat, on=['pais', 'ciudad'], how='left')
    
    # Combinar mapa de burbujas con un mapa coroplético en un gráfico de múltiples capas
    fig_geo_completo = go.Figure()
    
    # Capa 1: Mapa coroplético de países como base
    for trace in fig_mapa.data:
        fig_geo_completo.add_trace(trace)
    
    # Capa 2: Burbujas para ciudades
    if not ventas_ciudad.empty:
        # Ajustar tamaño de burbujas para mejor visualización
        size_min = 8
        size_max = 40
        
        # Calcular tamaños normalizados para las burbujas
        if len(ventas_ciudad) > 1:
            min_cantidad = ventas_ciudad['cantidad'].min()
            max_cantidad = ventas_ciudad['cantidad'].max()
            rango = max_cantidad - min_cantidad
            if rango > 0:
                normalizer = lambda x: (x - min_cantidad) / rango * (size_max - size_min) + size_min
                bubble_sizes = [normalizer(val) for val in ventas_ciudad['cantidad']]
            else:
                bubble_sizes = [size_max] * len(ventas_ciudad)
        else:
            bubble_sizes = [size_max]
        
        fig_geo_completo.add_trace(go.Scattergeo(
            locationmode='country names',
            locations=ventas_ciudad['pais'],
            text=ventas_ciudad['ciudad'],
            marker=dict(
                size=bubble_sizes,
                color=ventas_ciudad['ventas'],
                colorscale='Viridis',
                colorbar=dict(
                    title=dict(
                        text="<b>Ventas<br>por Ciudad</b>",
                        font=dict(size=15, color='#1a365d')
                    ),
                    tickprefix="$",
                    x=1.26,
                    len=0.38,
                    thickness=14,
                    bgcolor='rgba(255,255,255,0.96)',
                    bordercolor='rgba(200,210,220,0.7)',
                    borderwidth=1.5,
                    outlinewidth=2,
                    outlinecolor='rgba(180,180,180,0.7)',
                    tickfont=dict(size=13, color='#1a365d')
                ),
                opacity=0.8,
                line=dict(width=1, color='white'),
                symbol='circle'
            ),
            mode='markers',
            hovertemplate='<b>%{text}</b><br>' +
                          'País: %{location}<br>' +
                          'Ventas: $%{marker.color:,.2f}<br>' +
                          'Cantidad: %{marker.size:,.0f}' +
                          '<extra></extra>',
            name='Ciudades'
        ))
    
    # Ajustes finales para el mapa combinado
    fig_geo_completo.update_layout(
        title={
            'text': 'Análisis Geoespacial de Ventas: Países y Ciudades',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': TITLE_FONT
        },
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            landcolor='rgba(240, 240, 240, 0.8)',
            oceancolor='rgba(230, 240, 250, 0.8)',
            coastlinecolor='rgba(200, 200, 200, 0.8)',
            countrycolor='rgba(200, 200, 200, 0.8)',
            showocean=True,
            showcountries=True,
            bgcolor='rgba(240, 249, 255, 0.95)',
            lonaxis=dict(range=[-150, 70]),
            lataxis=dict(range=[-55, 85]),
            projection_scale=1.0,
        ),
        height=650,
        width=950,
        autosize=False,
        dragmode='pan',
        margin=dict(l=0, r=110, t=80, b=0)
    )
    
    st.plotly_chart(fig_geo_completo, use_container_width=True)
    
    # Insight para el mapa combinado de países y ciudades
   
    if not ventas_ciudad.empty:
        ciudad_mas_ventas = ventas_ciudad.loc[ventas_ciudad['ventas'].idxmax()]
        
        # Calcular concentración de ventas para las ciudades disponibles (hasta 3)
        num_ciudades = min(3, len(ventas_ciudad))
        top_ciudades = ventas_ciudad.nlargest(num_ciudades, 'ventas')
        total_ventas_ciudades = ventas_ciudad['ventas'].sum()
        concentracion_top = (top_ciudades['ventas'].sum() / total_ventas_ciudades) * 100
        
        # Generar HTML para las ciudades disponibles
        ciudades_html = ""
        for i in range(num_ciudades):
            ciudad_info = top_ciudades.iloc[i]
            ciudad_text = f"{ciudad_info['ciudad'].title()} ({ciudad_info['pais']}): ${ciudad_info['ventas']:,.2f}"
            ciudades_html += f"<li><b>{ciudad_text}</b></li>"
        
        # Determinar mensaje según la cantidad de ciudades
        if num_ciudades > 1:
            mensaje = f"Estas {num_ciudades} ciudades representan el <b>{concentracion_top:.1f}%</b> del total de ventas"
            if concentracion_top > 50:
                recomendacion = "Diversificar la presencia en más ciudades para reducir la dependencia geográfica."
            else:
                recomendacion = "Mantener la estrategia actual de distribución mientras se fortalecen los mercados clave."
        else:
            mensaje = "Esta ciudad representa el 100% de las ventas analizadas con los filtros actuales."
            recomendacion = "Considerar expandir a más ubicaciones para diversificar el mercado."
        
        st.markdown(f"""
        <div class='insight-card'>
        <h3>Insight: Análisis Geoespacial Detallado</h3>
        <p>La ciudad con mayor volumen de ventas es <b>{ciudad_mas_ventas['ciudad'].title()}</b> en <b>{ciudad_mas_ventas['pais']}</b> 
        con <b>${ciudad_mas_ventas['ventas']:,.2f}</b>.</p>
        
        <p><b>Top {num_ciudades} ciudades por ventas:</b></p>
        <ol style="margin-top: 0; padding-left: 20px;">
            {ciudades_html}
        </ol>
        
        <p>{mensaje}.</p>
        <p><b>Recomendación:</b> {recomendacion}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No hay datos suficientes de ciudades para generar insights geoespaciales detallados.")

    # 7. Segmentación de mercado mejorada: Visualización interactiva
    st.markdown("<h2 style='text-align:center; color:#1a365d; margin-bottom:20px; margin-top:40px; font-weight:700; font-size:28px; font-family:Arial, sans-serif;'>Segmentación de Mercado</h2>", unsafe_allow_html=True)
    
    # Añadimos el código para una sección básica de segmentación de mercado
    if 'rango_edad' in df_filtrado.columns and 'genero_cliente' in df_filtrado.columns:
        # Preparar datos para el gráfico de segmentación
        segmentacion = df_filtrado.groupby(['rango_edad', 'genero_cliente'])['ventas'].sum().reset_index()
        
        if not segmentacion.empty:
            # Calcular porcentajes para cada segmento
            total_ventas = segmentacion['ventas'].sum()
            segmentacion['porcentaje'] = (segmentacion['ventas'] / total_ventas * 100).round(1)
            
            # Ordenar los datos para un mejor aspecto visual
            orden_edad = ['<30', '30-45', '>45'] # Mantener orden lógico de grupos etarios
            
            # Crear un gráfico de barras agrupadas más profesional
            fig_segmentacion = px.bar(
                segmentacion,
                x='rango_edad',
                y='ventas',
                color='genero_cliente',
                color_discrete_map={  # Paleta de colores personalizada más profesional
                    'femenino': '#4a86e8',
                    'masculino': '#ff7043',
                    'f': '#4a86e8',
                    'm': '#ff7043',
                    'female': '#4a86e8',
                    'male': '#ff7043',
                    # Valores adicionales para posibles variaciones en los datos
                    'mujer': '#4a86e8', 
                    'hombre': '#ff7043'
                },
                category_orders={"rango_edad": orden_edad},
                labels={
                    'ventas': 'Ventas Totales (USD)',
                    'rango_edad': 'Segmento de Edad',
                    'genero_cliente': 'Género',
                    'porcentaje': 'Participación'
                },
                text='porcentaje',  # Mostrar porcentajes en las barras
                height=550,
                custom_data=['porcentaje', 'genero_cliente']  # Incluye género para el hover
            )
            
            # Personalizar el diseño con un estilo más profesional
            # CORRECCIÓN: yanchor cambiado de 'center' a 'middle' para evitar ValueError en Plotly
            fig_segmentacion.update_layout(
                title={
                    'text': 'Segmentación de Ventas por Edad y Género',
                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': TITLE_FONT
                },
                barmode='group',
                bargap=0.3,  # Espacio entre grupos
                bargroupgap=0.1,  # Espacio entre barras del mismo grupo
                xaxis_title={
                    'text': '<b>Segmento de Edad</b>',
                    'font': AXIS_TITLE_FONT
                },
                yaxis_title={
                    'text': '<b>Ventas Totales (USD)</b>',
                    'font': AXIS_TITLE_FONT
                },
                legend_title={
                    'text': '<b>Género</b>',
                    'font': LEGEND_FONT
                },
                font=LABEL_FONT,
                plot_bgcolor='rgba(240,249,255,0.95)',
                hoverlabel=dict(
                    bgcolor="white", 
                    font_size=14, 
                    font_family="Arial",
                    bordercolor='rgba(0,0,0,0.1)'
                ),
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.25,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(200,210,220,0.5)',
                    borderwidth=1
                ),
                margin=dict(l=60, r=320, t=80, b=120),  # Margen inferior aumentado para evitar solapamiento
                annotations=[
                    dict(
                        text="Fuente: Datos de ventas TechNova Retail",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=1,
                        y=-0.2,
                        font=dict(size=10, color="#6c757d"),
                        align="right"
                    )
                ]
            )
            
            # Mejorar el formato de las barras
            fig_segmentacion.update_traces(
                texttemplate='%{customdata[0]}%',  # Mostrar porcentaje
                textposition='outside',
                textfont=dict(
                    size=13,
                    color='#1a365d',
                    family='Arial',
                    weight='bold'
                )
            )
            
            # Añadir línea con promedio general
            promedio_ventas = segmentacion['ventas'].mean()
            fig_segmentacion.add_shape(
                type="line",
                x0=-0.5,
                y0=promedio_ventas,
                x1=len(orden_edad) - 0.5,
                y1=promedio_ventas,
                line=dict(
                    color="#2c5282",
                    width=2,
                    dash="dash",
                ),
                opacity=0.7
            )
            
            # Etiqueta para la línea de promedio
            fig_segmentacion.add_annotation(
                x=len(orden_edad) - 0.5,
                y=promedio_ventas,
                text=f"Ventas promedio: ${promedio_ventas:,.0f}",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#2c5282",
                ax=70,
                ay=0,
                font=dict(
                    size=12,
                    color="#2c5282",
                    family="Arial",
                    weight="bold"
                ),
                bgcolor="white",
                opacity=0.9,
                bordercolor="#4a86e8",
                borderwidth=1.5,
                borderpad=4
            )
            
            # Mostrar el gráfico
            st.plotly_chart(fig_segmentacion, use_container_width=True)
            
            # Identificar el segmento más valioso y hacer cálculos adicionales
            segmento_mas_valioso = segmentacion.loc[segmentacion['ventas'].idxmax()]
            segmento_opuesto = segmentacion[(segmentacion['rango_edad'] == segmento_mas_valioso['rango_edad']) & 
                                         (segmentacion['genero_cliente'] != segmento_mas_valioso['genero_cliente'])]
            
            if not segmento_opuesto.empty:
                diferencia_valor = segmento_mas_valioso['ventas'] - segmento_opuesto['ventas'].values[0]
                diferencia_porcentaje = (diferencia_valor / segmento_opuesto['ventas'].values[0]) * 100
                
                # Cálculo de ticket promedio por segmento si es posible
                if 'id_cliente' in df_filtrado.columns:
                    ticket_por_segmento = df_filtrado.groupby(['rango_edad', 'genero_cliente']).agg({
                        'ventas': 'sum',
                        'id_cliente': 'nunique'
                    })
                    ticket_por_segmento['ticket_promedio'] = ticket_por_segmento['ventas'] / ticket_por_segmento['id_cliente']
                    
                    ticket_segmento_valioso = ticket_por_segmento.loc[(segmento_mas_valioso['rango_edad'], segmento_mas_valioso['genero_cliente']), 'ticket_promedio']
                    ticket_info = f"<p>El ticket promedio de este segmento es <b>${ticket_segmento_valioso:.2f}</b>, lo que indica un alto poder adquisitivo.</p>"
                else:
                    ticket_info = ""
                
                # Obtener edades exactas para una mejor interpretación
                if segmento_mas_valioso['rango_edad'] == '<30':
                    rango_edad_texto = "menores de 30 años"
                elif segmento_mas_valioso['rango_edad'] == '30-45':
                    rango_edad_texto = "entre 30 y 45 años"
                else:  # >45
                    rango_edad_texto = "mayores de 45 años"
                
                # Personalizar género para el texto
                genero_texto = "masculino" if segmento_mas_valioso['genero_cliente'].lower() in ['masculino', 'm', 'male', 'hombre'] else "femenino"
                genero_opuesto = "femenino" if genero_texto == "masculino" else "masculino"
                
                # Análisis de categorías preferidas por este segmento
                categorias_segmento = df_filtrado[
                    (df_filtrado['rango_edad'] == segmento_mas_valioso['rango_edad']) & 
                    (df_filtrado['genero_cliente'] == segmento_mas_valioso['genero_cliente'])
                ].groupby('categoria')['ventas'].sum().sort_values(ascending=False)
                
                if not categorias_segmento.empty:
                    top_categorias = categorias_segmento.head(2).index.tolist()
                    categorias_texto = f"<p>Las categorías preferidas por este segmento son <b>{top_categorias[0].title()}</b>"
                    if len(top_categorias) > 1:
                        categorias_texto += f" y <b>{top_categorias[1].title()}</b>"
                    categorias_texto += ".</p>"
                else:
                    categorias_texto = ""
                
                # Crear insight HTML mejorado con formato estandarizado y más información
                insight_html = f"""
                <div class='insight-card'>
                <h3>Insight: Segmentación de Mercado</h3>
                <p>
                    El segmento más valioso son los clientes <b>{genero_texto}</b> <b>{rango_edad_texto}</b>, con ventas totales de 
                    <b>${segmento_mas_valioso['ventas']:,.2f}</b>, representando el <b>{segmento_mas_valioso['porcentaje']}%</b> del total de ventas.
                </p>
                
                <p>
                    Este segmento supera a su contraparte de <b>{genero_opuesto}</b> en la misma franja etaria por <b>${diferencia_valor:,.2f}</b> 
                    (<b>{diferencia_porcentaje:.1f}%</b> más), lo que sugiere una preferencia de género marcada en este grupo de edad.
                </p>
                
                {categorias_texto}
                {ticket_info}
                
                <p><b>Recomendaciones estratégicas:</b></p>
                <ul style="margin-top: 5px; padding-left: 20px;">
                    <li>Priorizar las estrategias de marketing y desarrollo de productos hacia el segmento <b>{genero_texto}</b> <b>{rango_edad_texto}</b>.</li>
                    <li>Desarrollar campañas específicas para aumentar la penetración en el segmento <b>{genero_opuesto}</b> <b>{rango_edad_texto}</b>, que muestra potencial de crecimiento.</li>
                    <li>Realizar investigación de mercado para entender mejor las preferencias de compra específicas del segmento demográfico dominante.</li>
                </ul>
                </div>
                """
            else:
                insight_html = """
                <div class='insight-card'>
                <h3>Insight: Segmentación de Mercado</h3>
                <p>No hay suficientes datos para comparar segmentos por género dentro del mismo rango de edad.</p>
                </div>
                """
            
            st.markdown(insight_html, unsafe_allow_html=True)
        else:
            st.info("No hay datos suficientes para crear la segmentación de mercado.")
    else:
        st.info("No hay datos suficientes para la segmentación de mercado por edad y género.")

# Función para crear tarjetas de métricas bonitas
def metric_card(title, value, delta, icon, color):
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 15px;
        padding: 20px 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 5px solid {color};
        margin-bottom: 15px;
        transition: transform 0.3s ease;
        font-family: Arial, sans-serif;
    ">
        <div style="font-size: 40px; margin-bottom: 10px;">{icon}</div>
        <h3 style="margin:0; color: #1a365d; font-size: 15px; font-weight: 700; font-family: Arial, sans-serif;">{title}</h3>
        <p style="font-size: 28px; font-weight: 700; color: {color}; margin: 10px 0 5px 0; font-family: Arial, sans-serif;">{value}</p>
        <span style="font-size: 13px; color: #595959; font-style: italic; font-family: Arial, sans-serif;">{delta}</span>
    </div>
    """, unsafe_allow_html=True)
