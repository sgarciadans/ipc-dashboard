# Dashboard IPC INDEC 🇦🇷

Dashboard interactivo del Índice de Precios al Consumidor de Argentina, con actualización automática diaria desde la API oficial del INDEC.

## Setup en 5 minutos

### 1. Crear el repositorio en GitHub
- Entrá a [github.com/new](https://github.com/new)
- Nombre: `ipc-dashboard` (o el que quieras)
- Visibilidad: **Public** (necesario para GitHub Pages gratis)
- Click en **Create repository**

### 2. Subir los archivos

**Opción A — Desde la web de GitHub (más fácil):**
1. En el repo recién creado, click en **"uploading an existing file"**
2. Arrastrá todos los archivos y carpetas de esta carpeta
3. Click en **Commit changes**

**Opción B — Con Git:**
```bash
cd ipc-dashboard
git init
git add .
git commit -m "feat: dashboard IPC INDEC"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/ipc-dashboard.git
git push -u origin main
```

### 3. Activar GitHub Pages
1. En tu repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / `/ (root)`
4. Click **Save**

### 4. Correr el workflow por primera vez (para poblar los datos)
1. En tu repo → **Actions**
2. Click en **"Actualizar datos IPC"**
3. Click en **"Run workflow"** → **"Run workflow"**
4. Esperá ~1 minuto

### 5. ¡Listo! 🎉
Tu dashboard va a estar disponible en:
```
https://TU_USUARIO.github.io/ipc-dashboard/
```

---

## ¿Cómo funciona?

```
GitHub Actions (todos los días a las 10:00 AM Argentina)
    ↓
scripts/fetch_indec.py
    ↓ fetches
apis.datos.gob.ar (API pública INDEC)
    ↓ guarda
data/ipc.json
    ↓ commit automático
index.html lee el JSON → dashboard actualizado
```

## Estructura

```
├── index.html              # Dashboard (abrí este en el browser)
├── data/
│   └── ipc.json           # Datos pre-procesados (auto-actualizado)
├── scripts/
│   └── fetch_indec.py     # Script que fetchea la API de INDEC
└── .github/
    └── workflows/
        └── update.yml     # GitHub Actions — corre diario
```

## Fuente de datos

- **INDEC** vía [API de Series de Tiempo — datos.gob.ar](https://apis.datos.gob.ar/series/api/)
- Base: diciembre 2016 = 100
- Frecuencia: mensual
- Cobertura: desde julio 2017
