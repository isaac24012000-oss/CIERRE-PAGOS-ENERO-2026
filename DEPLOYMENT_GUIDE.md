# Guía para Publicar en Streamlit Cloud

## Pasos para Publicar tu Dashboard

### 1️⃣ Preparar tu Repositorio GitHub

```bash
# Inicializar Git (si no lo has hecho)
git init

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit: Dashboard de Finanzas Enero 2026"

# Agregar origen remoto
git remote add origin https://github.com/tu-usuario/dashboard-finanzas.git

# Empujar a GitHub
git branch -M main
git push -u origin main
```

### 2️⃣ Crear Cuenta en Streamlit Cloud

1. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
2. Haz clic en "Sign up" o "Sign in" si ya tienes cuenta
3. Conecta tu cuenta de GitHub
4. Autoriza Streamlit para acceder a tus repositorios

### 3️⃣ Crear Nueva Aplicación

1. En tu dashboard de Streamlit Cloud, haz clic en "New app"
2. Selecciona:
   - **Repository**: `tu-usuario/dashboard-finanzas`
   - **Branch**: `main`
   - **Main file path**: `dashboard_finanzas.py`
3. Haz clic en "Deploy"

### 4️⃣ Configurar Datos en la Nube (Importante)

Como Streamlit Cloud es un entorno remoto, necesitas hacer accesible tu archivo Excel. Opciones:

#### Opción A: Google Drive (Recomendado)
```python
# Instalar: pip install gdown

import gdown
import pandas as pd

@st.cache_data
def cargar_datos():
    # Descargar de Google Drive
    url = "https://drive.google.com/uc?id=TU_FILE_ID"
    output = "CIERRE GASTOS ADMINISTRATIVOS ENERO 2026.xlsx"
    gdown.download(url, output, quiet=False)
    
    df = pd.read_excel(output, sheet_name="Hoja1")
    df = df.dropna(subset=['ASESOR'])
    
    return df
```

#### Opción B: GitHub (Archivos Pequeños)
1. Sube el archivo Excel a tu repositorio
2. Actualiza `.gitignore` para permitir archivos `.xlsx`
3. Streamlit lo cargará automáticamente

#### Opción C: Streamlit Secrets (Para URLs)
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Selecciona tu app
3. Haz clic en "Settings" → "Secrets"
4. Agrega tu URL de datos:
```toml
[data]
excel_url = "https://ejemplo.com/archivo.xlsx"
```

### 5️⃣ Monitorear el Despliegue

- Verás los logs en tiempo real
- Una vez que veas "App is running", ¡está lista!
- Tu app estará en: `https://dashboard-finanzas-XXXX.streamlit.app`

## 🔄 Actualizar la Aplicación

Cualquier cambio que hagas en GitHub se desplegará automáticamente:

```bash
# Hacer cambios localmente
# ...

# Commit y push
git add .
git commit -m "Update: Agregar nueva función"
git push origin main
```

Streamlit Cloud detará automáticamente los cambios y redesplegará la app.

## 🚨 Solución de Problemas

### App muestra "Loading..."
- Espera 1-2 minutos en el primer despliegue
- Comprueba los logs en Streamlit Cloud

### "ModuleNotFoundError"
- Verifica que `requirements.txt` esté en la raíz del repositorio
- Asegúrate de que la sintaxis es correcta

### Archivo Excel no se encuentra
- Implementa una de las opciones para datos en la nube (Opción A, B o C)

### Cambios no aparecen
- Streamlit Cloud redeploya automáticamente
- Si no, ve a Settings → Reboot app

## 💡 Tips de Optimización

1. **Usa caché**: El código ya lo tiene con `@st.cache_data`
2. **Limita datos**: Considera filtrar datos antiguos
3. **Comprime imágenes**: Streamlit no maneja bien imágenes muy pesadas
4. **Usa secrets**: Para datos sensibles, usa el manager de secretos de Streamlit

## 📊 Monitoreo y Estadísticas

En Streamlit Cloud puedes ver:
- Número de usuarios activos
- Uso de recursos
- Errores y logs
- Tiempo de respuesta

Todo esto en tu dashboard de Streamlit Cloud.

## 🎉 ¡Listo!

Tu dashboard está en la nube y accesible desde cualquier navegador. ¡Comparte el enlace!

---

Para más información: https://docs.streamlit.io/streamlit-cloud
