import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Dashboard de Pagos Enero 2026", layout="wide", initial_sidebar_state="expanded")

# Título principal
st.title("📊 Dashboard de Pagos - Enero 2026")

# Cargar datos
@st.cache_data
def cargar_datos():
    excel_file = "PAGOS ENERO 2026.xlsx"
    
    # Leer la hoja
    df_cierre = pd.read_excel(excel_file, sheet_name="Hoja1")
    df_totales = df_cierre  # Usar los mismos datos para ambas vistas
    
    # Convertir columnas de fechas a strings para evitar problemas de serialización con Arrow
    for col in df_cierre.columns:
        if pd.api.types.is_datetime64_any_dtype(df_cierre[col]):
            df_cierre[col] = df_cierre[col].dt.strftime('%Y-%m-%d')
    
    for col in df_totales.columns:
        if pd.api.types.is_datetime64_any_dtype(df_totales[col]):
            df_totales[col] = df_totales[col].dt.strftime('%Y-%m-%d')
    
    return df_cierre, df_totales

try:
    df_cierre, df_totales = cargar_datos()
    
    # Crear tabs
    tab1, tab2 = st.tabs(["📋 Cierre de Pagos", "📊 Pagos Total"])
    
    # TAB 1: CIERRE DE PAGOS
    with tab1:
        st.header("Cierre de Pagos")
        
        st.subheader("📊 Resumen de Datos - Cierre de Pagos")
        
        # Crear columnas para las métricas
        col1, col2, col3, col4 = st.columns(4)
        
        # Calcular totales
        total_pago_planilla = pd.to_numeric(df_cierre['PAGO PLANILLA'], errors='coerce').sum()
        total_pago_gastos = pd.to_numeric(df_cierre['PAGO GASTOS'], errors='coerce').sum()
        total_cartera = df_cierre['CARTERA'].nunique()
        total_asesores = df_cierre['ASESOR'].nunique()
        
        # Mostrar métricas
        col1.metric("💰 Total Pago Planilla", f"S/ {total_pago_planilla:,.2f}")
        col2.metric("💳 Total Pago Gastos", f"S/ {total_pago_gastos:,.2f}")
        col3.metric("📦 Total Carteras", f"{total_cartera}")
        col4.metric("👥 Total Asesores", f"{total_asesores}")
        
        # Gráficos
        st.subheader("📈 Visualizaciones")
        
        # Crear dos columnas para los gráficos
        gf1, gf2 = st.columns(2)
        
        # Gráfico 1: Top 10 - Pago Planilla por Asesor
        with gf1:
            df_por_asesor = df_cierre.groupby('ASESOR')['PAGO PLANILLA'].sum().reset_index()
            df_por_asesor = df_por_asesor.sort_values('PAGO PLANILLA', ascending=False).head(10)
            
            fig = px.bar(df_por_asesor, x='ASESOR', y='PAGO PLANILLA', 
                        title="Top 10 - Pago Planilla por Asesor",
                        labels={'PAGO PLANILLA': 'Monto (S/)', 'ASESOR': 'Asesor'},
                        color='PAGO PLANILLA', color_continuous_scale="Blues")
            fig.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico 2: Comparación Pago Planilla vs Pago Gastos
        with gf2:
            totales_comparacion = {
                "Tipo de Pago": ["Pago Planilla", "Pago Gastos"],
                "Monto": [total_pago_planilla, total_pago_gastos]
            }
            df_comparacion = pd.DataFrame(totales_comparacion)
            
            fig = px.pie(df_comparacion, values="Monto", names="Tipo de Pago",
                        title="Proporción: Pago Planilla vs Pago Gastos",
                        color_discrete_sequence=["#1f77b4", "#ff7f0e"])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico 3: Pago Gastos por Asesor
        gf3, gf4 = st.columns(2)
        
        with gf3:
            df_gastos_asesor = df_cierre.groupby('ASESOR')['PAGO GASTOS'].sum().reset_index()
            df_gastos_asesor = df_gastos_asesor.sort_values('PAGO GASTOS', ascending=False).head(10)
            
            fig = px.bar(df_gastos_asesor, x='ASESOR', y='PAGO GASTOS', 
                        title="Top 10 - Pago Gastos por Asesor",
                        labels={'PAGO GASTOS': 'Monto (S/)', 'ASESOR': 'Asesor'},
                        color='PAGO GASTOS', color_continuous_scale="Oranges")
            fig.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico 4: Cartera por Asesor
        with gf4:
            df_cartera = df_cierre.groupby('ASESOR')['CARTERA'].nunique().reset_index()
            df_cartera.columns = ['ASESOR', 'Cantidad_Cartera']
            df_cartera = df_cartera.sort_values('Cantidad_Cartera', ascending=False).head(10)
            
            fig = px.bar(df_cartera, x='ASESOR', y='Cantidad_Cartera', 
                        title="Top 10 - Carteras por Asesor",
                        labels={'Cantidad_Cartera': 'Cantidad', 'ASESOR': 'Asesor'},
                        color='Cantidad_Cartera', color_continuous_scale="Greens")
            fig.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico 5: Línea de Tiempo de Pagos
        st.subheader("📅 Línea de Tiempo de Pagos")
        
        # Crear DataFrame con datos de fecha y monto
        df_timeline = df_cierre[['FECHA_DE_PAGO', 'PAGO PLANILLA', 'PAGO GASTOS']].copy()
        df_timeline.columns = ['Fecha', 'Pago Planilla', 'Pago Gastos']
        df_timeline['Fecha'] = pd.to_datetime(df_timeline['Fecha'], errors='coerce')
        
        # Agrupar por fecha y sumar
        df_timeline_agg = df_timeline.groupby('Fecha').agg({
            'Pago Planilla': 'sum',
            'Pago Gastos': 'sum'
        }).reset_index()
        df_timeline_agg = df_timeline_agg.sort_values('Fecha')
        
        # Crear gráfico de línea
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=df_timeline_agg['Fecha'], 
            y=df_timeline_agg['Pago Planilla'],
            mode='lines+markers',
            name='Pago Planilla',
            line=dict(color='#1f77b4', width=3)
        ))
        fig_timeline.add_trace(go.Scatter(
            x=df_timeline_agg['Fecha'], 
            y=df_timeline_agg['Pago Gastos'],
            mode='lines+markers',
            name='Pago Gastos',
            line=dict(color='#ff7f0e', width=3)
        ))
        fig_timeline.update_layout(
            title='Evolución de Pagos por Fecha',
            xaxis_title='Fecha',
            yaxis_title='Monto (S/)',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Gráfico 6: Cantidad de pagos por día
        df_timeline['Cantidad'] = 1
        df_cantidad = df_timeline.groupby('Fecha')['Cantidad'].sum().reset_index()
        df_cantidad = df_cantidad.sort_values('Fecha')
        
        fig_cantidad = px.bar(df_cantidad, x='Fecha', y='Cantidad',
                             title='Cantidad de Pagos por Fecha',
                             labels={'Cantidad': 'Número de Pagos', 'Fecha': 'Fecha'},
                             color='Cantidad', color_continuous_scale="Viridis")
        fig_cantidad.update_layout(height=350)
        st.plotly_chart(fig_cantidad, use_container_width=True)
        
        # Mostrar tabla de datos detallados
        st.subheader("📋 Datos Detallados")
        st.dataframe(df_cierre, width='stretch', height=400)
    
    # TAB 2: PAGOS TOTAL
    with tab2:
        st.header("Pagos Total - Solo P y Pago P y G")
        
        st.subheader("📊 Resumen de Datos")
        
        # Crear columnas para las métricas
        col1, col2, col3 = st.columns(3)
        
        # Calcular totales
        total_suma = pd.to_numeric(df_totales['Suma Total'], errors='coerce').sum()
        total_pago_planilla_gastos = pd.to_numeric(df_totales['Pago Planilla y Gastos'], errors='coerce').sum()
        total_registros = len(df_totales)
        
        # Mostrar métricas
        col1.metric("💰 Total Suma General", f"S/ {total_suma:,.2f}")
        col2.metric("💳 Total Pago P y G", f"S/ {total_pago_planilla_gastos:,.2f}")
        col3.metric("📋 Total Registros", f"{total_registros}")
        
        # Crear visualizaciones
        st.subheader("📈 Visualizaciones")
        
        # Gráfico 1: Top 10 - Suma Total por Campaña
        gf1, gf2 = st.columns(2)
        
        with gf1:
            df_campana = df_totales.groupby('CAMPAÑA')['Suma Total'].sum().reset_index()
            df_campana = df_campana.sort_values('Suma Total', ascending=False)
            
            fig = px.bar(df_campana, x='CAMPAÑA', y='Suma Total', 
                        title="Suma Total por Campaña",
                        labels={'Suma Total': 'Monto (S/)', 'CAMPAÑA': 'Campaña'},
                        color='Suma Total', color_continuous_scale="Blues")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico 2: Comparación Suma Total vs Pago Planilla y Gastos
        with gf2:
            totales = {
                "Tipo": ["Suma Total", "Pago P y G"],
                "Monto": [total_suma, total_pago_planilla_gastos]
            }
            df_tots = pd.DataFrame(totales)
            
            fig = px.pie(df_tots, values="Monto", names="Tipo",
                        title="Proporción: Suma Total vs Pago P y G",
                        color_discrete_sequence=["#1f77b4", "#ff7f0e"])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico 3: Top 10 - Pago Planilla y Gastos por Razón Social
        st.subheader("🏢 Análisis por Razón Social")
        df_razon = df_totales.groupby('RAZON SOCIAL').agg({
            'Suma Total': 'sum',
            'Pago Planilla y Gastos': 'sum'
        }).reset_index()
        df_razon = df_razon.sort_values('Suma Total', ascending=False).head(10)
        
        fig = px.bar(df_razon, x='RAZON SOCIAL', y=['Suma Total', 'Pago Planilla y Gastos'],
                    title="Top 10 - Comparación de Montos por Razón Social",
                    labels={'value': 'Monto (S/)', 'RAZON SOCIAL': 'Razón Social'},
                    barmode='group')
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico 4: Línea de Tiempo de Pagos por Fecha
        st.subheader("📅 Línea de Tiempo de Pagos")
        
        # Crear DataFrame con datos de fecha y monto
        df_timeline2 = df_totales[['Fecha de Pago', 'Suma Total', 'Pago Planilla y Gastos']].copy()
        df_timeline2['Fecha de Pago'] = pd.to_datetime(df_timeline2['Fecha de Pago'], errors='coerce')
        
        # Agrupar por fecha y sumar
        df_timeline_agg2 = df_timeline2.dropna(subset=['Fecha de Pago']).groupby('Fecha de Pago').agg({
            'Suma Total': 'sum',
            'Pago Planilla y Gastos': 'sum'
        }).reset_index()
        df_timeline_agg2 = df_timeline_agg2.sort_values('Fecha de Pago')
        
        if len(df_timeline_agg2) > 0:
            # Crear gráfico de línea
            fig_timeline2 = go.Figure()
            fig_timeline2.add_trace(go.Scatter(
                x=df_timeline_agg2['Fecha de Pago'], 
                y=df_timeline_agg2['Suma Total'],
                mode='lines+markers',
                name='Suma Total',
                line=dict(color='#1f77b4', width=3)
            ))
            fig_timeline2.add_trace(go.Scatter(
                x=df_timeline_agg2['Fecha de Pago'], 
                y=df_timeline_agg2['Pago Planilla y Gastos'],
                mode='lines+markers',
                name='Pago P y G',
                line=dict(color='#ff7f0e', width=3)
            ))
            fig_timeline2.update_layout(
                title='Evolución de Pagos por Fecha',
                xaxis_title='Fecha',
                yaxis_title='Monto (S/)',
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_timeline2, use_container_width=True)
        
        # Mostrar tabla de datos detallados
        st.subheader("📋 Datos Detallados")
        st.dataframe(df_totales, width='stretch', height=400)
        
        # Resumen estadístico
        st.subheader("📊 Resumen Estadístico")
        st.dataframe(df_totales[['Suma Total', 'Pago Planilla y Gastos']].describe(), width='stretch')

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.info("Asegúrate de que el archivo 'PAGOS NOVIEMBRE 2025.xlsx' esté en el mismo directorio que este script.")
