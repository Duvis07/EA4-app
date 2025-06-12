import streamlit as st

# Constantes para textos repetidos
DESCRIPCION = "Descripción:"
VENTAJAS = "Ventajas:"
DESVENTAJAS = "Desventajas:"
CASOSUSO = "Casos de uso ideales:"
VER_DETALLES = "Ver detalles"

def mostrar_caso_estudio():
    st.markdown("<h1 style='font-size: 36px; color: #1a365d;'>Taller práctico: Analizando los datos en mapas</h1>", unsafe_allow_html=True)
    
    # Introducción
    st.markdown("<h2 style='font-size: 32px; color: #1a365d;'>Introducción</h2>", unsafe_allow_html=True)
    st.write("""
    El análisis geoespacial es fundamental para entender patrones de ventas, comportamientos de clientes y optimizar 
    estrategias comerciales basadas en ubicación. En este taller práctico, trabajamos con datos de ventas 
    minoristas de una cadena multinacional para identificar patrones significativos a través de visualizaciones 
    en mapas y otras técnicas analíticas.
    """)
    
    # Objetivos
    st.markdown("<h2 style='font-size: 32px; color: #1a365d;'>Objetivos</h2>", unsafe_allow_html=True)
    st.markdown("""
    - Analizar información espacial proveniente de datos reales de ventas minoristas.
    - Crear mapas interactivos que representen patrones significativos de ventas por ubicación geográfica.
    - Identificar tendencias regionales y comportamiento de clientes en diferentes países y ciudades.
    - Evaluar correlaciones entre ubicación, satisfacción del cliente y volumen de ventas.
    - Optimizar estrategias de ventas basadas en análisis geográfico de datos.
    """)
    
    # Conjunto de datos
    st.markdown("<h2 style='font-size: 32px; color: #1a365d;'>Conjunto de Datos</h2>", unsafe_allow_html=True)
    st.write("""
    El dataset "Ventas_Minoristas.xlsx" contiene información detallada sobre transacciones de una cadena minorista multinacional, incluyendo:
    """)
    
    st.markdown("""
    - **Productos vendidos**: Nombres y categorías
    - **Precios y cantidades**: Precio unitario en USD y cantidad de unidades vendidas
    - **Fechas de venta**: Registros temporales de cada transacción
    - **Ubicación geográfica**: País y ciudad donde se realizó la venta
    - **Método de pago**: Forma en que los clientes realizaron sus compras
    - **Demografía del cliente**: Edad y género
    - **Satisfacción del cliente**: Calificación de satisfacción en escala de 1-5
    """)
    
    # Investigación de herramientas
    st.markdown("<h2 style='font-size: 32px; color: #1a365d;'>Investigación de herramientas de geovisualización</h2>", unsafe_allow_html=True)
    st.write("""
    Para este análisis, investigamos cinco herramientas de visualización geoespacial, evaluando sus características, ventajas y limitaciones 
    para determinar cuál se adaptaba mejor a nuestros objetivos de análisis de ventas minoristas.
    """)
    
    # Python (Plotly)
    st.markdown("<h2 style='font-size: 24px; color: #1a365d;'>1. Python con Plotly</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES, expanded=True):
        st.subheader(DESCRIPCION)
        st.write("""
        Plotly es una librería de Python que ofrece capacidades avanzadas de visualización geoespacial interactiva. 
        Permite crear mapas coropléticos, mapas de burbujas y otras visualizaciones geográficas interactivas con 
        relativa facilidad y alto nivel de personalización.
        """)
        
        st.subheader(VENTAJAS)
        st.markdown("""
        - **Interactividad**: Creación de visualizaciones interactivas con funciones como zoom, hover y selección.
        - **Variedad de tipos de mapas**: Coropléticos, burbujas, dispersión geográfica, mapas de calor.
        - **Personalización**: Alto nivel de control sobre todos los aspectos visuales.
        - **Integración con análisis de datos**: Trabaja perfectamente con pandas y otras librerías de análisis.
        - **Exportación web**: Posibilidad de exportar visualizaciones para uso en aplicaciones web.
        """)
        
        st.subheader(DESVENTAJAS)
        st.markdown("""
        - **Curva de aprendizaje**: Requiere conocimientos de programación en Python.
        - **Configuración inicial**: Puede ser complejo configurar correctamente las dependencias.
        - **Rendimiento**: Puede ralentizarse con conjuntos de datos muy grandes.
        - **Manejo de errores**: A veces los mensajes de error no son intuitivos.
        """)
        
        st.subheader(CASOSUSO)
        st.markdown("""
        - **Análisis exploratorio avanzado** de datos geoespaciales con múltiples dimensiones.
        - **Dashboards interactivos** que requieren filtrado en tiempo real y exploración profunda.
        - **Informes técnicos** que necesitan visualizaciones geoespaciales detalladas y personalizables.
        - **Análisis comparativo** entre regiones con múltiples variables superpuestas.
        """)
    
    # Power BI
    st.markdown("<h2 style='font-size: 24px; color: #1a365d;'>2. Power BI</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES):
        st.subheader(DESCRIPCION)
        st.write("""
        Power BI es una herramienta de Business Intelligence de Microsoft que ofrece capacidades integradas de 
        visualización geoespacial. Permite crear mapas basados en ubicaciones geográficas con una interfaz intuitiva 
        de arrastrar y soltar, facilitando el análisis de datos espaciales para usuarios empresariales.
        """)
        
        st.subheader(VENTAJAS)
        st.markdown("""
        - **Facilidad de uso**: Interfaz visual intuitiva que no requiere programación.
        - **Integración empresarial**: Conexión directa con fuentes de datos corporativas.
        - **Actualizaciones automáticas**: Capacidad para configurar actualizaciones programadas de datos.
        - **Compartir y colaboración**: Fácil distribución de informes y dashboards dentro de organizaciones.
        - **Complementos geoespaciales**: Visualizaciones específicas para mapas como ArcGIS.
        """)
        
        st.subheader(DESVENTAJAS)
        st.markdown("""
        - **Personalización limitada**: Menos flexibilidad que soluciones basadas en código.
        - **Licenciamiento**: Costos asociados para funcionalidades avanzadas y compartir.
        - **Limitaciones de rendimiento**: Puede ralentizarse con conjuntos de datos muy grandes.
        - **Opciones de mapas geoespaciales más básicas** que herramientas especializadas.
        """)
        
        st.subheader(CASOSUSO)
        st.markdown("""
        - **Dashboards ejecutivos** donde la facilidad de interpretación es prioritaria.
        - **Informes corporativos recurrentes** que necesitan actualizaciones programadas.
        - **Análisis geoespacial básico a intermedio** sin necesidad de programación.
        - **Entornos empresariales** donde la integración con el ecosistema Microsoft es importante.
        """)
    
    # Tableau
    st.markdown("<h2 style='font-size: 24px; color: #1a365d;'>3. Tableau</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES):
        st.subheader(DESCRIPCION)
        st.write("""
        Tableau es una plataforma líder de visualización de datos con capacidades geoespaciales avanzadas. Ofrece 
        herramientas específicas para mapeo que permiten crear visualizaciones geográficas sofisticadas con una 
        interfaz intuitiva, combinando facilidad de uso y alto nivel de personalización.
        """)
        
        st.subheader(VENTAJAS)
        st.markdown("""
        - **Capacidades geoespaciales nativas**: Funcionalidades de mapeo robustas integradas.
        - **Geocodificación automática**: Conversión de ubicaciones a coordenadas geográficas.
        - **Visualizaciones atractivas**: Mapas visualmente impactantes con poco esfuerzo.
        - **Interactividad avanzada**: Filtros, drill-downs y tooltips sofisticados.
        - **Facilidad de uso**: Interfaz intuitiva que equilibra poder y accesibilidad.
        """)
        
        st.subheader(DESVENTAJAS)
        st.markdown("""
        - **Costo**: Licenciamiento significativo para uso empresarial completo.
        - **Curva de aprendizaje moderada**: Para funcionalidades avanzadas.
        - **Personalización limitada**: Comparado con soluciones programáticas como Python.
        - **Recursos computacionales**: Puede requerir hardware potente para conjuntos de datos grandes.
        """)
        
        st.subheader(CASOSUSO)
        st.markdown("""
        - **Análisis geoespacial avanzado** sin necesidad extensa de programación.
        - **Visualizaciones interactivas** para presentaciones ejecutivas y públicas.
        - **Dashboards comerciales** donde la estética y facilidad de comprensión son críticas.
        - **Análisis de territorios de ventas** con varios niveles de granularidad geográfica.
        """)
    
    # QGIS
    st.markdown("<h2 style='font-size: 24px; color: #1a365d;'>4. QGIS</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES):
        st.subheader(DESCRIPCION)
        st.write("""
        QGIS es un sistema de información geográfica (SIG) de código abierto que proporciona herramientas avanzadas 
        para el análisis y la visualización de datos espaciales. Está diseñado específicamente para trabajar con 
        datos geográficos, ofreciendo capacidades sofisticadas de manejo de capas, proyecciones y análisis espacial.
        """)
        
        st.subheader(VENTAJAS)
        st.markdown("""
        - **Especializado en geografía**: Herramientas específicas para análisis espacial avanzado.
        - **Código abierto y gratuito**: Sin costos de licenciamiento.
        - **Extensible**: Numerosos complementos disponibles para funcionalidades específicas.
        - **Formatos variados**: Compatibilidad con múltiples formatos de datos espaciales.
        - **Análisis espacial avanzado**: Operaciones como buffer, intersección, y análisis de proximidad.
        """)
        
        st.subheader(DESVENTAJAS)
        st.markdown("""
        - **Curva de aprendizaje pronunciada**: Requiere conocimientos específicos de SIG.
        - **Menos orientado a business intelligence**: Enfocado en análisis geográfico más que en BI.
        - **Interfaz menos intuitiva**: Comparado con herramientas orientadas a negocios.
        - **Integración más complicada** con flujos de trabajo empresariales no espaciales.
        """)
        
        st.subheader(CASOSUSO)
        st.markdown("""
        - **Análisis geoespacial profundo** que requiere operaciones espaciales avanzadas.
        - **Creación de mapas cartográficos precisos** para reportes especializados.
        - **Proyectos que requieren múltiples capas** de información geográfica.
        - **Análisis de proximidad y territorios** para planificación de ubicaciones comerciales.
        """)
    
    # Looker Studio (anteriormente Data Studio)
    st.markdown("<h2 style='font-size: 24px; color: #1a365d;'>5. Looker Studio</h2>", unsafe_allow_html=True)
    with st.expander(VER_DETALLES):
        st.subheader(DESCRIPCION)
        st.write("""
        Looker Studio (anteriormente Google Data Studio) es una herramienta gratuita de visualización de datos en la nube 
        que incluye capacidades para crear mapas y visualizaciones geoespaciales. Ofrece una plataforma accesible para 
        crear dashboards interactivos con componentes geográficos, especialmente integrada con el ecosistema de Google.
        """)
        
        st.subheader(VENTAJAS)
        st.markdown("""
        - **Gratuito**: Accesible sin costo para funcionalidades básicas y avanzadas.
        - **Basado en la nube**: No requiere instalación local ni mantenimiento.
        - **Colaborativo**: Facilidad para compartir y trabajar en equipo en tiempo real.
        - **Integración con Google**: Conexión nativa con fuentes de datos de Google.
        - **Mapas de Google**: Utiliza la familiar interfaz de Google Maps.
        """)
        
        st.subheader(DESVENTAJAS)
        st.markdown("""
        - **Opciones de visualización geoespacial limitadas**: Menos tipos de mapas que herramientas especializadas.
        - **Personalización restringida**: Menos opciones para personalizar visualizaciones avanzadas.
        - **Dependencia de conexión a internet**: Requiere acceso web constante.
        - **Limitaciones de rendimiento**: Puede ralentizarse con conjuntos de datos muy grandes.
        """)
        
        st.subheader(CASOSUSO)
        st.markdown("""
        - **Informes geoespaciales rápidos** que requieren colaboración en equipo.
        - **Dashboards compartidos públicamente** sin necesidad de licencias para los consumidores.
        - **Visualización geoespacial básica** integrada con datos de Google Analytics o Sheets.
        - **Proyectos con presupuesto limitado** que requieren capacidades de mapeo.
        """)
    
    # Justificación de la selección
    st.markdown("<h2 style='font-size: 32px; color: #1a365d;'>Justificación de la selección de herramientas</h2>", unsafe_allow_html=True)
    st.write("""
    Para el análisis de ventas minoristas con componente geoespacial, seleccionamos **Python con Plotly** como nuestra herramienta principal, 
    complementada con elementos de análisis estadístico utilizando pandas, matplotlib y seaborn. Esta combinación nos permite realizar 
    un análisis integral de los patrones de ventas, incorporando visualizaciones geoespaciales interactivas con un alto nivel de personalización.
    """)
    
    st.subheader("Criterios de selección:")
    st.markdown("""
    1. **Complejidad de los datos:** El dataset contiene múltiples dimensiones (productos, ubicaciones, demografía, tiempo), lo que requiere 
       una herramienta flexible como Python que puede manejar análisis multidimensional y preparación avanzada de datos.
       
    2. **Tipo de visualización requerida:** Necesitábamos crear mapas coropléticos por país y mapas de burbujas para ciudades, 
       junto con visualizaciones estadísticas como boxplots y heatmaps que se integren en un análisis cohesivo. Plotly ofrece 
       todas estas capacidades en un ecosistema unificado.
       
    3. **Interactividad:** Los mapas y gráficos interactivos permiten una exploración más profunda de los datos de ventas, 
       algo que Plotly proporciona de manera nativa y que es crucial para descubrir patrones no evidentes inicialmente.
       
    4. **Integración con análisis estadístico:** La combinación de capacidades geoespaciales con herramientas de análisis 
       estadístico es esencial para correlacionar ubicación con variables como satisfacción y volumen de ventas.
       
    5. **Escalabilidad:** Python permite automatizar el análisis para futuras actualizaciones de datos, haciendo el proceso sostenible.
    """)
    
    st.subheader("Comparación con alternativas:")
    st.write("""
    Aunque herramientas como Tableau o Power BI ofrecen interfaces más amigables, Python con Plotly proporciona mayor 
    flexibilidad y personalización para crear exactamente las visualizaciones que necesitamos para este análisis 
    específico de ventas minoristas con enfoque geoespacial. El código desarrollado también permite reproducibilidad 
    y adaptación a futuros conjuntos de datos similares.
    """)
    
    # Conclusiones
    st.markdown("<h2 style='font-size: 32px; color: #1a365d;'>Conclusiones</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-card'>
    <p>El análisis geoespacial de los datos de ventas minoristas de TechNova Retail nos ha permitido identificar patrones 
    y tendencias significativas que pueden guiar las decisiones estratégicas de la empresa:</p>
    
    <h3>1. Patrones geográficos determinantes</h3>
    <p>La visualización de datos en mapas ha revelado una clara disparidad en el comportamiento de ventas entre diferentes 
    regiones geográficas. Los mapas coropléticos por país y los mapas de burbujas por ciudad nos han permitido identificar 
    no solo dónde se concentra el mayor volumen de ventas, sino también dónde se encuentran las oportunidades de crecimiento 
    con mayor potencial. Esta información es fundamental para decisiones de expansión, distribución de recursos y estrategias 
    de marketing regionalizadas.</p>
    
    <h3>2. Correlación entre ubicación y comportamiento del cliente</h3>
    <p>El análisis geoespacial ha evidenciado una fuerte correlación entre la ubicación geográfica y factores como la 
    satisfacción del cliente, el ticket promedio y las preferencias de categorías de productos. Estas correlaciones permiten 
    desarrollar estrategias personalizadas por región, optimizando el surtido de productos, los precios y las campañas 
    promocionales según las características específicas de cada mercado. La combinación de visualizaciones geoespaciales 
    con análisis demográficos ha sido especialmente valiosa para segmentar mercados de manera efectiva.</p>
    
    <p>La herramienta seleccionada, Python con Plotly, ha demostrado ser la opción más adecuada para este análisis al 
    permitir la creación de visualizaciones interactivas, personalizables y con múltiples capas de información que facilitan 
    la identificación de patrones complejos y la comunicación efectiva de los hallazgos. La capacidad para combinar 
    diferentes tipos de visualizaciones y análisis estadísticos en un flujo de trabajo unificado resultó ser determinante 
    para la profundidad del análisis obtenido.</p>
    </div>
    """, unsafe_allow_html=True)

    # Referencias bibliográficas
    st.markdown("""
    <h2 style='font-size: 28px; color: #1a365d; margin-top:32px;'>Referencias bibliográficas</h2>
    <ul style='font-size:18px;'>
        <li><b>Plotly Technologies Inc. (2023).</b> Plotly: The front end for ML and data science models. <a href='https://plotly.com/python/' target='_blank'>https://plotly.com/python/</a></li>
        <li><b>McKinney, W. (2010).</b> Data Structures for Statistical Computing in Python. <i>Proceedings of the 9th Python in Science Conference</i>, 51-56.</li>
        <li><b>Jordahl, K. (2022).</b> GeoPandas: Python tools for geographic data. <a href='https://geopandas.org/' target='_blank'>https://geopandas.org/</a></li>
        <li><b>Rey, S. J., & Arribas-Bel, D. (2022).</b> Geographic Data Science with Python. <i>CRC Press</i>.</li>
        <li><b>Robinson, A. C., et al. (2017).</b> Geospatial Big Data and Cartography: Research Challenges and Opportunities for Making Maps That Matter. <i>International Journal of Cartography</i>, 3(sup1), 32-60.</li>
    </ul>
    """, unsafe_allow_html=True)