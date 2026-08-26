# Contribución al proyecto

## Guía de contribución

Este documento describe cómo contribuir al proyecto Create-Python-App.

### Estructura del proyecto

El proyecto está organizado en las siguientes secciones:

- `cpa-templates/`: Plantillas para generar aplicaciones
- `fastapi-starter/`: Plantilla base para aplicaciones FastAPI
- `mlops-sklearn-starter/`: Plantilla base para MLOps con soporte de scikit-learn
- `cli-starter/`: Plantilla para el CLI
- `uv-workspace-starter/`: Plantilla para configuración de entorno

### Requisitos previos

- Python 3.10+
- Node.js 18+ (para compilar extensiones)
- `uv` instalado (versión 0.4.0 o superior)
- `curl` y `git` instalados

### Cómo crear una nueva aplicación

Para crear una nueva aplicación, utiliza el comando:

```bash
uvx create-awesome-python-app mi-app \
  --template fastapi-starter \
  --addons github-setup fastapi-docker \
  --yes
```

Esto generará un proyecto con la plantilla FastAPI y las extensiones recomendadas.

### Contribuciones

#### Tipos de contribuciones

1. **Corrección de bugs** - Arreglar errores en el código existente
2. **Nueva función** - Añadir nuevas características solicitadas por los usuarios
3. **Mejora de documentación** - Actualizar guías, READMEs y archivos de configuración
4. **Extensión** - Crear una nueva extensión para el sistema de plantillas

#### Flujo de trabajo

1. Crea una rama nueva desde `main`:
   ```bash
   git checkout -b mi-nueva-contribucion
   ```

2. Haz tus cambios y asegúrate de que el código compile correctamente:
   ```bash
   uv sync
   uv run ruff check .
   ```

3. Sube tu cambio al repositorio:
   ```bash
   git push origin mi-nueva-contribucion
   ```

4. Abre una solicitud de pull request (PR) contra `main`.

### Reglas de estilo

- Usa **Jinja2** para variables en los archivos `.template`
- Los archivos sin sufijo se copian tal cual
- Las extensiones deben usar el patrón `.append` o `.append.template`
- El archivo `pyproject.toml` debe declarar todas las dependencias necesarias

### Calidad del código

- **Tipado**: Documenta el tipado de Python en `docs/TYPING.md`
- **Tests**: Cada nuevo cambio debe incluir pruebas unitarias
- **Linting**: Ejecuta `ruff` y `ruff format` antes de hacer commit

### Recursos

- [Guía completa de plantillas](docs/ARCHITECTURE.md)
- [Calidad del código](docs/QUALITY.md)
- [Lista de tareas](docs/TASKS.md)

### Contacto

Para preguntas sobre contribución, contacta a los mantenedores del proyecto.
