# Contribuyendo

¡Gracias por contribuir! Este repo impulsa [create-awesome-python-app](https://github.com/Create-Python-App/create-python-app).

Para una explicación completa de cómo funcionan las plantillas, extensiones y el sistema de archivos, lee [docs/AUTHORING.md](./docs/AUTHORING.md).

## Agregar una extensión

1. Crea `extensions/<tu-slug>/`
2. Agrega archivos para copiar en el proyecto generado (usa `template/` si solo quieres un subconjunto copiado)
3. Regístrala en `templates.json` bajo `"extensions"`:

```json
{
  "name": "Mi Extensión",
  "slug": "mi-extension",
  "description": "Agrega X a tu proyecto",
  "url": "https://github.com/Create-Python-App/cpa-templates/tree/main/extensions/mi-extension",
  "type": ["fastapi-backend"],
  "category": "tooling",
  "labels": ["FastAPI", "Tooling"]
}
```

## Agregar una plantilla

1. Crea `templates/<tu-slug>/` con un `pyproject.toml` (y opcional `template/` subdirectorio)
2. Agrega `cpa.config.json` para opciones interactivas cuando sea necesario
3. Regístrala en `templates.json` bajo `"templates"` (mismos campos que extensiones)

## Mensajes de commit

Usa [commit convencionales](https://www.conventionalcommits.org/es): `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.

## Checklist de PR

- [ ] El nombre del directorio coincide con el `slug` en `templates.json`
- [ ] `url` apunta a la ruta correcta en la rama `main`
- [ ] `slug` es globalmente único entre plantillas y extensiones
- [ ] Todos los campos requeridos presentes: `name`, `slug`, `description`, `url`, `type`, `category`, `labels`
- [ ] `type` de extensión es un array si apoya múltiples tipos de plantillas
- [ ] Probado localmente — mira [docs/TESTING.md](./docs/TESTING.md)

## ¿Preguntas?

Abre un [issue](https://github.com/Create-Python-App/cpa-templates/issues) o inicia una [discussion](https://github.com/Create-Python-App/cpa-templates/discussions).

## Nota sobre Contribuciones

El **canonical** es la versión en inglés (`CONTRIBUTING.md`). Se mantiene un **resumen breve en español** aquí abajo para crear un acceso rápido al proceso de contribución para hispanohablantes.

## Resumen Rápido para Hispanohablantes

**Para iniciar una contribución:**

1. **Clona el repo** desde `https://github.com/Create-Python-App/cpa-templates`
2. **Lee `docs/AUTHORING.md`** para entender cómo funcionan las plantillas y extensiones
3. **Crea una extensión**
   - Crea una carpeta nueva: `extensions/<tu-slug>/`
   - Agrega archivos a copiar en el proyecto (o dentro de `template/` si solo quieres un subconjunto)
   - Regístrala en `templates.json` bajo `"extensions"` siguiendo el formato de ejemplo
4. **Crea una plantilla**
   - Crea una carpeta nueva: `templates/<tu-slug>/`
   - Incluye un archivo `pyproject.toml` (y opcionalmente un directorio `template/`)
   - Agrega `cpa.config.json` si necesitas opciones interactivas
   - Regístrala en `templates.json` bajo `"templates"`
5. **Sigue las reglas**:
   - Usa commits convencionales (por ejemplo, `feat:`, `fix:`, `docs:`)
   - Verifica la checklist de PR en la versión en inglés
6. **Prueba localmente**
   - Consulta [docs/TESTING.md](./docs/TESTING.md) para guías de pruebas locales

**Para más ayuda:** Abre un issue o discussion en el repo.