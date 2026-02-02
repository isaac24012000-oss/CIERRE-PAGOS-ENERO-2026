import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import io
import os
from pathlib import Path

# Configuración de la página
st.set_page_config(page_title="Dashboard Finanzas - Enero 2026", layout="wide", initial_sidebar_state="expanded")

# Título principal
st.title("💰 Dashboard de Finanzas - Enero 2026")

# Función para encontrar el archivo Excel
def encontrar_archivo_excel():
    """Busca el archivo Excel en múltiples ubicaciones"""
    nombres_posibles = [
        "CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx",
        "./CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx",
    ]
    
    # Buscar en el directorio actual
    for nombre in nombres_posibles:
        if os.path.exists(nombre):
            return nombre
    
    # Buscar en el directorio del script
    script_dir = Path(__file__).parent
    for nombre in nombres_posibles:
        ruta = script_dir / nombre.strip("./")
        if ruta.exists():
            return str(ruta)
    
    # Buscar en directorios padres
    for padre in [script_dir.parent, script_dir.parent.parent]:
        for nombre in nombres_posibles:
            ruta = padre / nombre.strip("./")
            if ruta.exists():
                return str(ruta)
    
    return None

# Cargar datos
@st.cache_data
def cargar_datos():
    archivo = encontrar_archivo_excel()
    
    if archivo is None:
        return None, "No se encontró el archivo 'CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx'"
    
    try:
        # Leer la hoja
        df = pd.read_excel(archivo, sheet_name="Hoja1")
        
        # Excluir filas que no tengan ASESOR (son filas de totales)
        df = df.dropna(subset=['ASESOR'])
        
        # Convertir columnas de fechas a strings para evitar problemas de serialización
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%d')
        
        return df, None
    except Exception as e:
        return None, f"Error al leer el archivo: {str(e)}"

# Cargar datos
resultado_carga = cargar_datos()
if isinstance(resultado_carga, tuple):
    df, error_msg = resultado_carga
else:
    df = resultado_carga
    error_msg = None

try:
    if df is None or error_msg is not None:
        st.error(f"⚠️ {error_msg or 'Error desconocido al cargar los datos'}")
        
        # Opción para subir archivo en Streamlit Cloud
        st.info("📤 Si estás usando Streamlit Cloud, sube el archivo Excel aquí:")
        uploaded_file = st.file_uploader("Elige el archivo Excel", type="xlsx")
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file, sheet_name="Hoja1")
                df = df.dropna(subset=['ASESOR'])
                
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        df[col] = df[col].dt.strftime('%Y-%m-%d')
                
                st.success("✅ Archivo cargado correctamente")
            except Exception as e:
                st.error(f"Error al procesar el archivo: {str(e)}")
                st.stop()
        else:
            st.stop()
    
    # ============ ANÁLISIS PRINCIPAL: VALOR VENTA, IGV, MONTO ============
    st.markdown("---")
    st.subheader("💵 Indicadores Financieros Principales")
    st.markdown("---")
    
    # Calcular KPIs
    total_valor_venta = pd.to_numeric(df['VALOR VENTA'], errors='coerce').sum()
    total_igv = pd.to_numeric(df['IGV'], errors='coerce').sum()
    total_monto = pd.to_numeric(df['MONTO'], errors='coerce').sum()
    
    # Gráficos principales en 3 columnas grandes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Monto por Cartera - PRINCIPAL
        df_cartera_monto = df.groupby('CARTERA')['MONTO'].sum().reset_index().sort_values('MONTO', ascending=True)
        
        fig = px.bar(df_cartera_monto, x='MONTO', y='CARTERA',
                     title=f"<b>MONTO TOTAL</b><br>S/ {total_monto:,.2f}",
                     labels={'MONTO': 'Monto (S/)', 'CARTERA': 'Cartera'},
                     color='MONTO', color_continuous_scale="Greens",
                     orientation='h')
        fig.update_layout(height=600, showlegend=False, template='plotly_white',
                         font=dict(size=12),
                         margin=dict(l=150))
        fig.update_traces(textposition='auto', texttemplate='S/ %{x:,.0f}', textfont=dict(size=12))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Composición del MONTO: Valor Venta vs IGV
        descomposicion = pd.DataFrame({
            'Componente': ['Valor Venta', 'IGV'],
            'Monto': [total_valor_venta, total_igv]
        })
        
        fig = px.pie(descomposicion, values='Monto', names='Componente',
                     title=f"<b>COMPOSICIÓN DEL MONTO</b><br>Valor Venta: S/ {total_valor_venta:,.2f}<br>IGV: S/ {total_igv:,.2f}",
                     color_discrete_map={'Valor Venta': '#1f77b4', 'IGV': '#ff7f0e'},
                     hole=0.3)
        fig.update_layout(height=600, showlegend=True, template='plotly_white', font=dict(size=12))
        fig.update_traces(textposition='auto', texttemplate='<b>%{label}</b><br>S/ %{value:,.0f}<br>(%{percent})', 
                         textfont=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Descomposición por Cartera: Valor Venta e IGV apilados
        df_cartera_comp = df.groupby('CARTERA').agg({
            'VALOR VENTA': 'sum',
            'IGV': 'sum'
        }).reset_index().sort_values('VALOR VENTA', ascending=True)
        
        fig = px.bar(df_cartera_comp, x=['VALOR VENTA', 'IGV'], y='CARTERA',
                     title="<b>DESCOMPOSICIÓN POR CARTERA</b><br>Valor Venta e IGV",
                     labels={'value': 'Monto (S/)', 'CARTERA': 'Cartera'},
                     barmode='stack',
                     color_discrete_map={
                        'VALOR VENTA': '#1f77b4',
                        'IGV': '#ff7f0e'
                    },
                     orientation='h')
        fig.update_layout(height=600, showlegend=True, template='plotly_white',
                         font=dict(size=12),
                         margin=dict(l=150))
        fig.update_traces(textposition='auto', texttemplate='S/ %{x:,.0f}', textfont=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)
    
    # ============ ANÁLISIS DETALLADO POR ASESOR ============
    st.markdown("---")
    st.subheader("👥 Análisis Detallado por Asesor")
    st.markdown("---")
    
    # Top Asesores por Monto
    df_asesor = df.groupby('ASESOR').agg({
        'VALOR VENTA': 'sum',
        'IGV': 'sum',
        'MONTO': 'sum'
    }).reset_index().sort_values('MONTO', ascending=False).head(15)
    
    fig = px.bar(df_asesor, y='ASESOR', x='MONTO',
                title="<b>Top 15 Asesores - Monto</b>",
                labels={'MONTO': 'Monto (S/)', 'ASESOR': 'Asesor'},
                color='MONTO', color_continuous_scale="Blues",
                orientation='h')
    fig.update_layout(height=600, showlegend=False, template='plotly_white', 
                     yaxis={'categoryorder': 'total ascending'},
                     font=dict(size=11),
                     margin=dict(l=150))
    fig.update_traces(textposition='auto', texttemplate='S/ %{x:,.0f}', textfont=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)
    
    # ============ LÍNEA DE TIEMPO FINANCIERA ============
    st.markdown("---")
    st.subheader("📅 Evolución Financiera por Fecha")
    st.markdown("---")
    
    # Preparar datos de línea de tiempo
    df_timeline = df[['FECHA_DE_PAGO', 'VALOR VENTA', 'IGV', 'MONTO']].copy()
    df_timeline['FECHA_DE_PAGO'] = pd.to_datetime(df_timeline['FECHA_DE_PAGO'], errors='coerce')
    
    # Agrupar por fecha
    df_timeline_agg = df_timeline.dropna(subset=['FECHA_DE_PAGO']).groupby('FECHA_DE_PAGO').agg({
        'VALOR VENTA': 'sum',
        'IGV': 'sum',
        'MONTO': 'sum'
    }).reset_index().sort_values('FECHA_DE_PAGO')
    
    if len(df_timeline_agg) > 0:
        col_timeline1, col_timeline2 = st.columns(2)
        
        with col_timeline1:
            # Crear gráfico de línea mejorado - Solo Monto Total
            fig_timeline = go.Figure()
            
            fig_timeline.add_trace(go.Scatter(
                x=df_timeline_agg['FECHA_DE_PAGO'], 
                y=df_timeline_agg['MONTO'],
                mode='lines+markers+text',
                name='Monto Diario',
                line=dict(color='#2ca02c', width=3),
                marker=dict(size=10),
                text=df_timeline_agg['MONTO'].apply(lambda x: f'S/ {x:,.0f}'),
                textposition='top center',
                textfont=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(44, 160, 44, 0.3)'
            ))
            
            fig_timeline.update_layout(
                title='<b>Monto Diario - Enero 2026</b>',
                xaxis_title='Fecha',
                yaxis_title='Monto (S/)',
                hovermode='x unified',
                height=550,
                template='plotly_white',
                showlegend=False,
                font=dict(size=11)
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        with col_timeline2:
            # Crear gráfico acumulado
            df_timeline_agg['MONTO_ACUMULADO'] = df_timeline_agg['MONTO'].cumsum()
            
            fig_acumulado = go.Figure()
            
            fig_acumulado.add_trace(go.Scatter(
                x=df_timeline_agg['FECHA_DE_PAGO'], 
                y=df_timeline_agg['MONTO_ACUMULADO'],
                mode='lines+markers+text',
                name='Acumulado',
                line=dict(color='#d62728', width=3),
                marker=dict(size=10),
                text=df_timeline_agg['MONTO_ACUMULADO'].apply(lambda x: f'S/ {x:,.0f}'),
                textposition='top center',
                textfont=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(214, 39, 40, 0.3)'
            ))
            
            fig_acumulado.update_layout(
                title='<b>Monto Acumulado - Progresión en Enero</b>',
                xaxis_title='Fecha',
                yaxis_title='Monto Acumulado (S/)',
                hovermode='x unified',
                height=550,
                template='plotly_white',
                showlegend=False,
                font=dict(size=11)
            )
            st.plotly_chart(fig_acumulado, use_container_width=True)
    
    # ============ ANÁLISIS POR SEMANA ============
    st.markdown("---")
    st.subheader("📅 Análisis por Semana (Lunes a Domingo)")
    st.markdown("---")
    
    # Preparar datos de semana
    df_week = df[['FECHA_DE_PAGO', 'VALOR VENTA', 'IGV', 'MONTO']].copy()
    df_week['FECHA_DE_PAGO'] = pd.to_datetime(df_week['FECHA_DE_PAGO'], errors='coerce')
    
    # Definir las semanas comenzando en lunes (incluyendo 29 dic del año pasado)
    semanas = {
        'Semana 1 (29 Dic - 4 Ene)': (pd.Timestamp('2025-12-29'), pd.Timestamp('2026-01-04')),
        'Semana 2 (5 - 11 Ene)': (pd.Timestamp('2026-01-05'), pd.Timestamp('2026-01-11')),
        'Semana 3 (12 - 18 Ene)': (pd.Timestamp('2026-01-12'), pd.Timestamp('2026-01-18')),
        'Semana 4 (19 - 25 Ene)': (pd.Timestamp('2026-01-19'), pd.Timestamp('2026-01-25')),
        'Semana 5 (26 - 31 Ene)': (pd.Timestamp('2026-01-26'), pd.Timestamp('2026-01-31'))
    }
    
    # Calcular montos por semana
    datos_semana = []
    for semana, (fecha_inicio, fecha_fin) in semanas.items():
        df_semana_temp = df_week[(df_week['FECHA_DE_PAGO'] >= fecha_inicio) & 
                                  (df_week['FECHA_DE_PAGO'] <= fecha_fin)]
        
        if len(df_semana_temp) > 0:
            total_valor_venta_semana = pd.to_numeric(df_semana_temp['VALOR VENTA'], errors='coerce').sum()
            total_igv_semana = pd.to_numeric(df_semana_temp['IGV'], errors='coerce').sum()
            total_monto_semana = pd.to_numeric(df_semana_temp['MONTO'], errors='coerce').sum()
            
            datos_semana.append({
                'Semana': semana,
                'VALOR VENTA': total_valor_venta_semana,
                'IGV': total_igv_semana,
                'MONTO': total_monto_semana
            })
    
    if datos_semana:
        df_semanas = pd.DataFrame(datos_semana)
        
        # Gráfico de barras agrupadas por semana
        col_sem1, col_sem2 = st.columns(2)
        
        with col_sem1:
            # Gráfico de barras: Monto por Semana
            fig_semana = px.bar(df_semanas, x='Semana', y='MONTO',
                               title='<b>Dinero Ingresado por Semana</b>',
                               labels={'MONTO': 'Monto (S/)', 'Semana': 'Semana'},
                               color='MONTO', color_continuous_scale='Viridis',
                               text='MONTO')
            fig_semana.update_layout(xaxis_tickangle=-45, height=600, template='plotly_white',
                                    font=dict(size=11),
                                    margin=dict(b=100))
            fig_semana.update_traces(texttemplate='S/ %{value:,.0f}', textposition='auto', textfont=dict(size=12))
            st.plotly_chart(fig_semana, use_container_width=True)
        
        with col_sem2:
            # Gráfico de comparación: Valor Venta vs IGV por semana
            fig_comp_semana = px.bar(df_semanas, x='Semana', y=['VALOR VENTA', 'IGV'],
                                    title='<b>Composición por Semana</b><br>Valor Venta e IGV',
                                    labels={'value': 'Monto (S/)', 'Semana': 'Semana'},
                                    barmode='group',
                                    color_discrete_map={
                                        'VALOR VENTA': '#1f77b4',
                                        'IGV': '#ff7f0e'
                                    })
            fig_comp_semana.update_layout(xaxis_tickangle=-45, height=600, template='plotly_white',
                                         font=dict(size=11),
                                         margin=dict(b=100))
            fig_comp_semana.update_traces(textposition='auto', texttemplate='S/ %{y:,.0f}', textfont=dict(size=11))
            st.plotly_chart(fig_comp_semana, use_container_width=True)
        
        # Tabla resumen de semanas
        st.markdown("---")
        st.subheader("📊 Resumen Semanal")
        
        df_semanas_display = df_semanas.copy()
        df_semanas_display['VALOR VENTA'] = df_semanas_display['VALOR VENTA'].apply(lambda x: f"S/ {x:,.2f}")
        df_semanas_display['IGV'] = df_semanas_display['IGV'].apply(lambda x: f"S/ {x:,.2f}")
        df_semanas_display['MONTO'] = df_semanas_display['MONTO'].apply(lambda x: f"S/ {x:,.2f}")
        
        st.dataframe(df_semanas_display, use_container_width=True, hide_index=True)
    
    # ============ ANÁLISIS POR CAMPAÑA ============
    st.markdown("---")
    st.subheader("🎯 Análisis por Campaña")
    st.markdown("---")
    
    df_campana = df.groupby('CAMPANA').agg({
        'VALOR VENTA': 'sum',
        'IGV': 'sum',
        'MONTO': 'sum'
    }).reset_index().sort_values('MONTO', ascending=False)
    
    fig = px.bar(df_campana, x='CAMPANA', y=['VALOR VENTA', 'IGV', 'MONTO'],
                title="<b>Análisis Financiero por Campaña</b>",
                labels={'value': 'Monto (S/)', 'CAMPANA': 'Campaña'},
                barmode='group',
                color_discrete_map={
                    'VALOR VENTA': '#1f77b4',
                    'IGV': '#ff7f0e',
                    'MONTO': '#2ca02c'
                })
    fig.update_layout(xaxis_tickangle=-45, height=700, template='plotly_white', 
                     font=dict(size=12),
                     margin=dict(t=100, b=100))
    fig.update_traces(textposition='auto', texttemplate='S/ %{y:,.0f}', textfont=dict(size=14, color='black'))
    st.plotly_chart(fig, use_container_width=True)
    
    # ============ ANÁLISIS POR ESTADO DE PLANILLA ============
    st.markdown("---")
    st.subheader("📋 Distribución por Estado de Planilla")
    st.markdown("---")
    
    # Monto por Estado de Planilla
    df_estado = df.groupby('ESTADO_PLANILLA').agg({
        'MONTO': 'sum'
    }).reset_index().sort_values('MONTO', ascending=False)
    
    fig = px.pie(df_estado, values='MONTO', names='ESTADO_PLANILLA',
                title='<b>Distribución de Monto por Estado de Planilla</b>',
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.3)
    fig.update_layout(height=600, template='plotly_white', font=dict(size=12))
    fig.update_traces(textposition='auto', texttemplate='<b>%{label}</b><br>S/ %{value:,.0f}<br>(%{percent})',
                     textfont=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)
    
    # ============ TABLA DE DATOS DETALLADOS ============
    st.markdown("---")
    st.subheader("📊 Datos Detallados")
    st.markdown("---")
    
    # Crear una copia para mostrar - Seleccionar solo columnas importantes
    df_display = df[['ASESOR', 'CAMPANA', 'CARTERA', 'RAZON_SOCIAL', 'FECHA_DE_PAGO', 
                     'VALOR VENTA', 'IGV', 'MONTO', 'ESTADO_PLANILLA', 'NUMERO_FACTURA']].copy()
    
    # Crear versión sin formato para exportar a Excel
    df_export = df_display.copy()
    for col in ['VALOR VENTA', 'IGV', 'MONTO']:
        if col in df_export.columns:
            df_export[col] = pd.to_numeric(df_export[col], errors='coerce')
    
    # Formatear columnas numéricas para mostrar
    for col in ['VALOR VENTA', 'IGV', 'MONTO']:
        if col in df_display.columns:
            df_display[col] = pd.to_numeric(df_display[col], errors='coerce').apply(lambda x: f"S/ {x:,.2f}" if pd.notna(x) else "")
    
    # Botón para descargar Excel
    col_export1, col_export2 = st.columns([3, 1])
    
    with col_export2:
        # Crear archivo Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_export.to_excel(writer, sheet_name='Datos', index=False)
        output.seek(0)
        
        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name="Datos_Finanzas_Enero_2026.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )
    
    st.dataframe(df_display, use_container_width=True, height=400)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.info("📤 Si estás usando Streamlit Cloud, carga el archivo Excel usando el uploader anterior.")

