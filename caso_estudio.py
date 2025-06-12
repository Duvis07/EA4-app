import streamlit as st

# Constantes para estilos estandarizados
TITLE_FONT = "font-family: Arial, sans-serif; font-weight: 800; color: #1a365d;"
HEADING_FONT = "font-family: Arial, sans-serif; font-weight: 700; color: #1a365d;"
BODY_FONT = "font-family: Arial, sans-serif; font-weight: 400; color: #2d3748;"
ACCENT_COLOR = "#4a86e8"

# Constantes para textos repetidos
DESCRIPCION = "Descripción:"
VENTAJAS = "Ventajas:"
DESVENTAJAS = "Desventajas:"
CASOSUSO = "Casos de uso ideales:"
VER_DETALLES = "Ver detalles"

def mostrar_caso_estudio():
    st.markdown(f"<h1 style='{TITLE_FONT} font-size: 36px;'>Taller práctico: Analizando los datos en mapas</h1>", unsafe_allow_html=True)
    
    # Introducción
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 32px;'>Introducción</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
    El análisis geoespacial es fundamental para entender patrones de ventas, comportamientos de clientes y optimizar 
    estrategias comerciales basadas en ubicación. En este taller práctico, trabajamos con datos de ventas 
    minoristas de una cadena multinacional para identificar patrones significativos a través de visualizaciones 
    en mapas y otras técnicas analíticas.
    </p>
    """, unsafe_allow_html=True)
    
    # Objetivos
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 32px;'>Objetivos</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
        <li>Analizar información espacial proveniente de datos reales de ventas minoristas.</li>
        <li>Crear mapas interactivos que representen patrones significativos de ventas por ubicación geográfica.</li>
        <li>Identificar tendencias regionales y comportamiento de clientes en diferentes países y ciudades.</li>
        <li>Evaluar correlaciones entre ubicación, satisfacción del cliente y volumen de ventas.</li>
        <li>Optimizar estrategias de ventas basadas en análisis geográfico de datos.</li>
    </ul>
    """, unsafe_allow_html=True)
    
    # Conjunto de datos
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 32px;'>Conjunto de Datos</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
    El dataset "Ventas_Minoristas.xlsx" contiene información detallada sobre transacciones de una cadena minorista multinacional, incluyendo:
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
        <li><b>Productos vendidos</b>: Nombres y categorías</li>
        <li><b>Precios y cantidades</b>: Precio unitario en USD y cantidad de unidades vendidas</li>
        <li><b>Fechas de venta</b>: Registros temporales de cada transacción</li>
        <li><b>Ubicación geográfica</b>: País y ciudad donde se realizó la venta</li>
        <li><b>Método de pago</b>: Forma en que los clientes realizaron sus compras</li>
        <li><b>Demografía del cliente</b>: Edad y género</li>
        <li><b>Satisfacción del cliente</b>: Calificación de satisfacción en escala de 1-5</li>
    </ul>
    """, unsafe_allow_html=True)
    
    # Investigación de herramientas
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 32px;'>Investigación de herramientas de geovisualización</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
    Para este análisis, investigamos cinco herramientas de visualización geoespacial, evaluando sus características, ventajas y limitaciones 
    para determinar cuál se adaptaba mejor a nuestros objetivos de análisis de ventas minoristas.
    </p>
    """, unsafe_allow_html=True)
    
    # Python (Plotly)
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 24px;'>1. Python con Plotly</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES, expanded=True):
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESCRIPCION}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
        Plotly es una librería de Python que ofrece capacidades avanzadas de visualización geoespacial interactiva. 
        Permite crear mapas coropléticos, mapas de burbujas y otras visualizaciones geográficas interactivas con 
        relativa facilidad y alto nivel de personalización.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{VENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Interactividad</b>: Creación de visualizaciones interactivas con funciones como zoom, hover y selección.</li>
            <li><b>Variedad de tipos de mapas</b>: Coropléticos, burbujas, dispersión geográfica, mapas de calor.</li>
            <li><b>Personalización</b>: Alto nivel de control sobre todos los aspectos visuales.</li>
            <li><b>Integración con análisis de datos</b>: Trabaja perfectamente con pandas y otras librerías de análisis.</li>
            <li><b>Exportación web</b>: Posibilidad de exportar visualizaciones para uso en aplicaciones web.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESVENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Curva de aprendizaje</b>: Requiere conocimientos de programación en Python.</li>
            <li><b>Configuración inicial</b>: Puede ser complejo configurar correctamente las dependencias.</li>
            <li><b>Rendimiento</b>: Puede ralentizarse con conjuntos de datos muy grandes.</li>
            <li><b>Manejo de errores</b>: A veces los mensajes de error no son intuitivos.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{CASOSUSO}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Análisis exploratorio avanzado</b> de datos geoespaciales con múltiples dimensiones.</li>
            <li><b>Dashboards interactivos</b> que requieren filtrado en tiempo real y exploración profunda.</li>
            <li><b>Informes técnicos</b> que necesitan visualizaciones geoespaciales detalladas y personalizables.</li>
            <li><b>Análisis comparativo</b> entre regiones con múltiples variables superpuestas.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    # Power BI
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 24px;'>2. Power BI</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES):
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESCRIPCION}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
        Power BI es una herramienta de Business Intelligence de Microsoft que ofrece capacidades integradas de 
        visualización geoespacial. Permite crear mapas basados en ubicaciones geográficas con una interfaz intuitiva 
        de arrastrar y soltar, facilitando el análisis de datos espaciales para usuarios empresariales.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{VENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Facilidad de uso</b>: Interfaz visual intuitiva que no requiere programación.</li>
            <li><b>Integración empresarial</b>: Conexión directa con fuentes de datos corporativas.</li>
            <li><b>Actualizaciones automáticas</b>: Capacidad para configurar actualizaciones programadas de datos.</li>
            <li><b>Compartir y colaboración</b>: Fácil distribución de informes y dashboards dentro de organizaciones.</li>
            <li><b>Complementos geoespaciales</b>: Visualizaciones específicas para mapas como ArcGIS.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESVENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Personalización limitada</b>: Menos flexibilidad que soluciones basadas en código.</li>
            <li><b>Licenciamiento</b>: Costos asociados para funcionalidades avanzadas y compartir.</li>
            <li><b>Limitaciones de rendimiento</b>: Puede ralentizarse con conjuntos de datos muy grandes.</li>
            <li><b>Opciones de mapas geoespaciales más básicas</b> que herramientas especializadas.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{CASOSUSO}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Dashboards ejecutivos</b> donde la facilidad de interpretación es prioritaria.</li>
            <li><b>Informes corporativos recurrentes</b> que necesitan actualizaciones programadas.</li>
            <li><b>Análisis geoespacial básico a intermedio</b> sin necesidad de programación.</li>
            <li><b>Entornos empresariales</b> donde la integración con el ecosistema Microsoft es importante.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    # Tableau
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 24px;'>3. Tableau</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES):
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESCRIPCION}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
        Tableau es una plataforma líder de visualización de datos con capacidades geoespaciales avanzadas. Ofrece 
        herramientas específicas para mapeo que permiten crear visualizaciones geográficas sofisticadas con una 
        interfaz intuitiva, combinando facilidad de uso y alto nivel de personalización.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{VENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Capacidades geoespaciales nativas</b>: Funcionalidades de mapeo robustas integradas.</li>
            <li><b>Geocodificación automática</b>: Conversión de ubicaciones a coordenadas geográficas.</li>
            <li><b>Visualizaciones atractivas</b>: Mapas visualmente impactantes con poco esfuerzo.</li>
            <li><b>Interactividad avanzada</b>: Filtros, drill-downs y tooltips sofisticados.</li>
            <li><b>Facilidad de uso</b>: Interfaz intuitiva que equilibra poder y accesibilidad.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESVENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height:1.6;'>
            <li><b>Costo</b>: Licenciamiento significativo para uso empresarial completo.</li>
            <li><b>Curva de aprendizaje moderada</b>: Para funcionalidades avanzadas.</li>
            <li><b>Personalización limitada</b>: Comparado con soluciones programáticas como Python.</li>
            <li><b>Recursos computacionales</b>: Puede requerir hardware potente para conjuntos de datos grandes.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{CASOSUSO}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Análisis geoespacial avanzado</b> sin necesidad extensa de programación.</li>
            <li><b>Visualizaciones interactivas</b> para presentaciones ejecutivas y públicas.</li>
            <li><b>Dashboards comerciales</b> donde la estética y facilidad de comprensión son críticas.</li>
            <li><b>Análisis de territorios de ventas</b> con varios niveles de granularidad geográfica.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    # QGIS
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 24px;'>4. QGIS</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES):
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESCRIPCION}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
        QGIS es un sistema de información geográfica (SIG) de código abierto que proporciona herramientas avanzadas 
        para el análisis y la visualización de datos espaciales. Está diseñado específicamente para trabajar con 
        datos geográficos, ofreciendo capacidades sofisticadas de manejo de capas, proyecciones y análisis espacial.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{VENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Especializado en geografía</b>: Herramientas específicas para análisis espacial avanzado.</li>
            <li><b>Código abierto y gratuito</b>: Sin costos de licenciamiento.</li>
            <li><b>Extensible</b>: Numerosos complementos disponibles para funcionalidades específicas.</li>
            <li><b>Formatos variados</b>: Compatibilidad con múltiples formatos de datos espaciales.</li>
            <li><b>Análisis espacial avanzado</b>: Operaciones como buffer, intersección, y análisis de proximidad.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESVENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Curva de aprendizaje pronunciada</b>: Requiere conocimientos específicos de SIG.</li>
            <li><b>Menos orientado a business intelligence</b>: Enfocado en análisis geográfico más que en BI.</li>
            <li><b>Interfaz menos intuitiva</b>: Comparado con herramientas orientadas a negocios.</li>
            <li><b>Integración más complicada</b> con flujos de trabajo empresariales no espaciales.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{CASOSUSO}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Análisis geoespacial profundo</b> que requiere operaciones espaciales avanzadas.</li>
            <li><b>Creación de mapas cartográficos precisos</b> para reportes especializados.</li>
            <li><b>Proyectos que requieren múltiples capas</b> de información geográfica.</li>
            <li><b>Análisis de proximidad y territorios</b> para planificación de ubicaciones comerciales.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    # Looker Studio (anteriormente Data Studio)
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 24px;'>5. Looker Studio</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES):
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESCRIPCION}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
        Looker Studio (anteriormente Google Data Studio) es una herramienta gratuita de visualización de datos en la nube 
        que incluye capacidades para crear mapas y visualizaciones geoespaciales. Ofrece una plataforma accesible para 
        crear dashboards interactivos con componentes geográficos, especialmente integrada con el ecosistema de Google.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{VENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Gratuito</b>: Accesible sin costo para funcionalidades básicas y avanzadas.</li>
            <li><b>Basado en la nube</b>: No requiere instalación local ni mantenimiento.</li>
            <li><b>Colaborativo</b>: Facilidad para compartir y trabajar en equipo en tiempo real.</li>
            <li><b>Integración con Google</b>: Conexión nativa con fuentes de datos de Google.</li>
            <li><b>Mapas de Google</b>: Utiliza la familiar interfaz de Google Maps.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{DESVENTAJAS}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Opciones de visualización geoespacial limitadas</b>: Menos tipos de mapas que herramientas especializadas.</li>
            <li><b>Personalización restringida</b>: Menos opciones para personalizar visualizaciones avanzadas.</li>
            <li><b>Dependencia de conexión a internet</b>: Requiere acceso web constante.</li>
            <li><b>Limitaciones de rendimiento</b>: Puede ralentizarse con conjuntos de datos muy grandes.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>{CASOSUSO}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
            <li><b>Informes geoespaciales rápidos</b> que requieren colaboración en equipo.</li>
            <li><b>Dashboards compartidos públicamente</b> sin necesidad de licencias para los consumidores.</li>
            <li><b>Visualización geoespacial básica</b> integrada con datos de Google Analytics o Sheets.</li>
            <li><b>Proyectos con presupuesto limitado</b> que requieren capacidades de mapeo.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    # Justificación de la selección
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 32px;'>Justificación de la selección de herramientas</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
    Para el análisis de ventas minoristas con componente geoespacial, seleccionamos <b>Python con Plotly</b> como nuestra herramienta principal, 
    complementada con elementos de análisis estadístico utilizando pandas, matplotlib y seaborn. Esta combinación nos permite realizar 
    un análisis integral de los patrones de ventas, incorporando visualizaciones geoespaciales interactivas con un alto nivel de personalización.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>Criterios de selección:</h3>", unsafe_allow_html=True)
    
    # Usar una lista más simple sin sangría para evitar problemas de formato
    st.markdown(f"""
    <ol style='{BODY_FONT} font-size: 18px; line-height: 1.6; padding-left: 30px;'>
    <li><b>Complejidad de los datos:</b> El dataset contiene múltiples dimensiones (productos, ubicaciones, demografía, tiempo), lo que requiere una herramienta flexible como Python que puede manejar análisis multidimensional y preparación avanzada de datos.</li>
    <li><b>Tipo de visualización requerida:</b> Necesitábamos crear mapas coropléticos por país y mapas de burbujas para ciudades, junto con visualizaciones estadísticas como boxplots y heatmaps que se integren en un análisis cohesivo. Plotly ofrece todas estas capacidades en un ecosistema unificado.</li>
    <li><b>Interactividad:</b> Los mapas y gráficos interactivos permiten una exploración más profunda de los datos de ventas, algo que Plotly proporciona de manera nativa y que es crucial para descubrir patrones no evidentes inicialmente.</li>
    <li><b>Integración con análisis estadístico:</b> La combinación de capacidades geoespaciales con herramientas de análisis estadístico es esencial para correlacionar ubicación con variables como satisfacción y volumen de ventas.</li>
    <li><b>Escalabilidad:</b> Python permite automatizar el análisis para futuras actualizaciones de datos, haciendo el proceso sostenible.</li>
    </ol>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='{HEADING_FONT} font-size: 20px;'>Comparación con alternativas:</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
    Aunque herramientas como Tableau o Power BI ofrecen interfaces más amigables, Python con Plotly proporciona mayor 
    flexibilidad y personalización para crear exactamente las visualizaciones que necesitamos para este análisis 
    específico de ventas minoristas con enfoque geoespacial. El código desarrollado también permite reproducibilidad 
    y adaptación a futuros conjuntos de datos similares.
    </p>
    """, unsafe_allow_html=True)
    
    # Conclusiones
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 32px;'>Conclusiones</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background-color: #f8fafc; padding: 25px; border-radius: 10px; border-left: 5px solid {ACCENT_COLOR}; margin-bottom: 20px;'>
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>El análisis geoespacial de los datos de ventas minoristas de TechNova Retail nos ha permitido identificar patrones 
    y tendencias significativas que pueden guiar las decisiones estratégicas de la empresa:</p>
    
    <h3 style='{HEADING_FONT} font-size: 22px;'>1. Patrones geográficos determinantes</h3>
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>La visualización de datos en mapas ha revelado una clara disparidad en el comportamiento de ventas entre diferentes 
    regiones geográficas. Los mapas coropléticos por país y los mapas de burbujas por ciudad nos han permitido identificar 
    no solo dónde se concentra el mayor volumen de ventas, sino también dónde se encuentran las oportunidades de crecimiento 
    con mayor potencial. Esta información es fundamental para decisiones de expansión, distribución de recursos y estrategias 
    de marketing regionalizadas.</p>
    
    <h3 style='{HEADING_FONT} font-size: 22px;'>2. Correlación entre ubicación y comportamiento del cliente</h3>
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>El análisis geoespacial ha evidenciado una fuerte correlación entre la ubicación geográfica y factores como la 
    satisfacción del cliente, el ticket promedio y las preferencias de categorías de productos. Estas correlaciones permiten 
    desarrollar estrategias personalizadas por región, optimizando el surtido de productos, los precios y las campañas 
    promocionales según las características específicas de cada mercado. La combinación de visualizaciones geoespaciales 
    con análisis demográficos ha sido especialmente valiosa para segmentar mercados de manera efectiva.</p>
    
    <p style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>La herramienta seleccionada, Python con Plotly, ha demostrado ser la opción más adecuada para este análisis al 
    permitir la creación de visualizaciones interactivas, personalizables y con múltiples capas de información que facilitan 
    la identificación de patrones complejos y la comunicación efectiva de los hallazgos. La capacidad para combinar 
    diferentes tipos de visualizaciones y análisis estadísticos en un flujo de trabajo unificado resultó ser determinante 
    para la profundidad del análisis obtenido.</p>
    </div>
    """, unsafe_allow_html=True)

    # Referencias bibliográficas
    st.markdown(f"<h2 style='{HEADING_FONT} font-size: 28px; margin-top:32px;'>Referencias bibliográficas</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <ul style='{BODY_FONT} font-size: 18px; line-height: 1.6;'>
        <li><b>Plotly Technologies Inc. (2023).</b> Plotly: The front end for ML and data science models. <a href='https://plotly.com/python/' target='_blank'>https://plotly.com/python/</a></li>
        <li><b>McKinney, W. (2010).</b> Data Structures for Statistical Computing in Python. <i>Proceedings of the 9th Python in Science Conference</i>, 51-56.</li>
        <li><b>Jordahl, K. (2022).</b> GeoPandas: Python tools for geographic data. <a href='https://geopandas.org/' target='_blank'>https://geopandas.org/</a></li>
        <li><b>Rey, S. J., & Arribas-Bel, D. (2022).</b> Geographic Data Science with Python. <i>CRC Press</i>.</li>
        <li><b>Robinson, A. C., et al. (2017).</b> Geospatial Big Data and Cartography: Research Challenges and Opportunities for Making Maps That Matter. <i>International Journal of Cartography</i>, 3(sup1), 32-60.</li>
    </ul>
    """, unsafe_allow_html=True)