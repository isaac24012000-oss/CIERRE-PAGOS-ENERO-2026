# Dashboard de Finanzas - Enero 2026

Dashboard interactivo para análisis financiero de gastos administrativos desarrollado con Streamlit y Plotly.

## 📊 Características

- **Indicadores Principales**: Visualización de Monto Total, Valor Venta e IGV
- **Análisis por Cartera**: Descomposición de montos por cartera
- **Top Asesores**: Ranking de los mejores asesores por monto
- **Análisis Temporal**: Evolución diaria y acumulado durante enero
- **Análisis por Campaña**: Comparación de montos por campaña
- **Estado de Planillas**: Distribución por estado administrativo
- **Exportación de Datos**: Descarga de datos detallados en Excel
- **Interfaz Interactiva**: Gráficos dinámicos y responsivos

## 🚀 Requisitos

- Python 3.8+
- pip

## 📦 Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd dashboard-finanzas
```

2. **Crear un entorno virtual** (recomendado)
```bash
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 📄 Preparación de datos

Este dashboard requiere un archivo Excel con la siguiente estructura:

**Archivo**: `CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx`
**Hoja**: `Hoja1`

**Columnas requeridas**:
- ASESOR
- CAMPANA
- CARTERA
- RAZON_SOCIAL
- FECHA_DE_PAGO
- VALOR VENTA
- IGV
- MONTO
- ESTADO_PLANILLA
- NUMERO_FACTURA

Coloca el archivo Excel en la misma carpeta que `dashboard_finanzas.py`

## 💻 Uso Local

Ejecuta el dashboard con Streamlit:

```bash
streamlit run dashboard_finanzas.py
```

El dashboard se abrirá en tu navegador (por defecto en `http://localhost:8501`)

## 🌐 Desplegar en Streamlit Cloud

1. **Push a GitHub**
   ```bash
   git init
   git add .
   git commit -m "Inicial: Dashboard de finanzas"
   git push origin main
   ```

2. **Conectar con Streamlit Cloud**
   - Ir a https://streamlit.io/cloud
   - Seleccionar "New app"
   - Conectar tu repositorio de GitHub
   - Seleccionar rama principal y archivo `dashboard_finanzas.py`

3. **Configurar secretos** (si es necesario)
   - Los datos se cargan desde el archivo local Excel
   - Para Streamlit Cloud, considera usar un servicio de almacenamiento en la nube (Google Drive, AWS S3, etc.)

## 📁 Estructura del Proyecto

```
.
├── dashboard_finanzas.py                          # Script principal del dashboard
├── requirements.txt                               # Dependencias del proyecto
├── README.md                                      # Este archivo
├── .gitignore                                     # Archivos a ignorar en Git
├── CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx  # Datos (no incluir en repo)
└── CIERRE-PAGOS-ENERO/                        # Carpeta adicional
    ├── LICENSE
    └── README.md
```

## 🎨 Tecnologías Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework web para aplicaciones de datos
- **[Pandas](https://pandas.pydata.org/)**: Análisis y manipulación de datos
- **[Plotly](https://plotly.com/)**: Visualización interactiva
- **[NumPy](https://numpy.org/)**: Computación numérica
- **[OpenPyXL](https://openpyxl.readthedocs.io/)**: Lectura/escritura de Excel

## 📊 Secciones del Dashboard

### Indicadores Principales
- Monto total por cartera
- Composición Valor Venta vs IGV
- Descomposición por cartera

### Análisis por Asesor
- Top 15 asesores por monto

### Evolución Temporal
- Monto diario durante enero
- Progresión acumulada del mes

### Análisis por Campaña
- Comparación de montos por campaña

### Estado de Planilla
- Distribución de montos por estado administrativo

### Datos Detallados
- Tabla completa con opción de descarga a Excel

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Notas

- El dashboard usa caché para optimizar el rendimiento al cargar datos
- Los datos se filtran automáticamente para excluir filas de totales (sin ASESOR)
- Todos los gráficos son interactivos y responsivos
- Los números se formatean automáticamente en soles peruanos (S/)

## ❓ Solución de Problemas

**Error: "No module named 'streamlit'"**
```bash
pip install -r requirements.txt
```

**Error: "Archivo Excel no encontrado"**
- Asegúrate de que `CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx` está en el mismo directorio

**El dashboard carga lentamente**
- Streamlit usa caché inteligente. La primera carga es lenta, las posteriores son rápidas

## 📧 Contacto

Para preguntas o sugerencias, contacta al autor del proyecto.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
