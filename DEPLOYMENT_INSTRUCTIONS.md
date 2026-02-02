# 📊 Dashboard de Finanzas - Enero 2026

Dashboard interactivo para análisis de pagos y gastos administrativos de enero 2026.

## 🚀 Despliegue en Streamlit Cloud

### Pasos para compartir en Streamlit Cloud:

1. **Crea una cuenta en Streamlit Cloud**: https://share.streamlit.io

2. **Conecta tu repositorio Git**:
   - Clona este repositorio o crea uno nuevo en GitHub
   - Sube los archivos necesarios:
     - `dashboard_finanzas.py`
     - `requirements.txt`
     - `CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx`
     - `.streamlit/config.toml` (opcional)

3. **Despliega la aplicación**:
   - Ve a https://share.streamlit.io
   - Click en "New app"
   - Selecciona tu repositorio
   - Selecciona el archivo principal: `dashboard_finanzas.py`

4. **Si el archivo Excel no se encuentra**:
   - El dashboard mostrará un uploader
   - Sube el archivo `CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx` desde la interfaz

## 📁 Estructura de archivos

```
CIERRE-PAGOS-ENERO-2026/
├── dashboard_finanzas.py          # Dashboard principal
├── dashboard.py                   # Dashboard de pagos
├── requirements.txt               # Dependencias Python
├── .streamlit/config.toml        # Configuración de Streamlit
├── CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx
├── PAGOS ENERO 2026.xlsx
└── README.md
```

## 📦 Dependencias

Las dependencias se instalan automáticamente desde `requirements.txt`:
- streamlit
- pandas
- plotly
- numpy
- openpyxl

## ✨ Características

- 📊 Indicadores financieros principales
- 📈 Análisis por cartera, asesor y campaña
- 📅 Evolución diaria y acumulada
- 📊 Análisis por semana (Lunes a Domingo)
- 💾 Descarga de datos en Excel
- 📤 Carga de archivos en Streamlit Cloud

## 🔧 Ejecución local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard
streamlit run dashboard_finanzas.py
```

## 📝 Notas

- El dashboard está optimizado para Enero 2026
- Las semanas comienzan en lunes
- Los montos se muestran en soles (S/)
- Todos los gráficos incluyen etiquetas con valores
