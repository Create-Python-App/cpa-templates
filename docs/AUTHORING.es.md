# Creación y mantenimiento de plantillas y extensiones

Guía para colaboradores que quieran añadir o actualizar plantillas y extensiones en `cpa-templates`. Esta guía sigue la misma estructura que [cna-templates AUTHORING.md](https://github.com/Create-Node-App/cna-templates/blob/main/docs/AUTHORING.md) y se mantiene en paridad con ella.

## Estructura del directorio de plantillas

```text
my-template/
├── cpa.config.json       # Prompts interactivos opcionales
├── pyproject.toml        # Manifiesto del proyecto (uv)
├── app/                  # Código de la aplicación
├── tests/
└── README.md
````

También puedes utilizar un subdirectorio `template/`. CPA copiará los archivos desde `template/` cuando exista:

```text
my-template/
├── cpa.config.json
└── template/
    ├── pyproject.toml
    └── app/
```

## pyproject.toml como manifiesto del proyecto

A diferencia de las plantillas de CNA que exportan `package/index.js`, las plantillas de CPA incluyen un archivo `pyproject.toml` en la raíz de la plantilla (o dentro de `template/`).

La CLI ejecuta `uv sync` después de generar el proyecto.

Las extensiones pueden incluir un `pyproject.toml` parcial con únicamente las claves que añaden (por ejemplo, un controlador de base de datos).

CPA combina estas configuraciones mediante overlays en lugar de sobrescribirlas. Consulta la sección de combinación de `pyproject` para más información.

## cpa.config.json

Define los prompts interactivos de la CLI. Las respuestas se convierten en variables de scaffold/Jinja. En CI o en modo no interactivo se utilizan los valores predeterminados.

```json
{
  "name": "my-template",
  "customOptions": [
    {
      "key": "apiPrefix",
      "type": "string",
      "message": "Prefijo de URL de la API",
      "default": "/api/v1"
    },
    {
      "key": "enableCors",
      "type": "boolean",
      "message": "Activar middleware CORS",
      "default": true
    }
  ]
}
```

| Campo     | Descripción                                                                                                                                            |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `key`     | Identificador de la opción (se convierte en una variable Jinja y coincide con directorios `[key]/` cuando el renombrado con corchetes está habilitado) |
| `type`    | Tipo del prompt (`string`, `boolean`, etc.)                                                                                                            |
| `message` | Pregunta mostrada en la CLI                                                                                                                            |
| `default` | Valor utilizado en modo no interactivo (`CI=true`)                                                                                                     |

Mantén `cpa.config.json` junto a la plantilla para que funcione correctamente tanto con resolución mediante slug como con URLs locales `file://`.

No coloques `customOptions` dentro de `templates.json`. Este archivo solo se lee desde `cpa.config.json`.

Referencia del esquema: `create-python-app docs/cpa-config-schema.md`.
## Variables Jinja2

Todos los archivos con extensión `.template` se procesan utilizando Jinja2.

El nombre del archivo generado elimina el sufijo `.template`.

Las variables que no estén definidas provocan un error durante la generación.(`StrictUndefined`).

| Variable | Origen | Ejemplo |
| --- | --- | --- |
| `{{ projectName }}` | Entrada del usuario o `--set projectName=...` | `my-api` |
| `{{ apiPrefix }}` | Opción personalizada de `cpa.config.json` | `/api/v1` |
| `{{ enableCors }}` | Opción personalizada de `cpa.config.json` | `true` |
| Cualquier `customOptions[].key` | Igual que la clave de la opción | — |

Ejemplo de `fastapi-starter`:

```python
# app/core/config.py.template

api_prefix: str = "{{ apiPrefix }}"
enable_cors: bool = {{ "True" if enableCors | lower in ["1", "true", "yes", "on"] else "False" }}
````

Utiliza filtros y condicionales de Jinja para valores booleanos y valores derivados.

Prefiere definir valores predeterminados explícitos dentro de las plantillas en lugar de depender de variables opcionales.

## Convenciones de archivos (`create-python-app-core`)

| Sufijo                                  | Comportamiento                                                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `.template`                             | Procesamiento con Jinja2 (`{{ var }}`), elimina el sufijo. Las variables no definidas generan error (`StrictUndefined`). |
| `.append`                               | Añade contenido al archivo correspondiente que ya existe en el proyecto.                                                 |
| `.append.template` / `.template.append` | Renderiza con Jinja y después añade el contenido.                                                                        |

Los archivos estáticos (sin sufijos especiales) se copian directamente.

En caso de conflicto de rutas, las capas posteriores sobrescriben los archivos anteriores, excepto `pyproject.toml`, que se combina mediante merge.

## Convenciones de nombres (compatibilidad con `cna-templates`)

### Archivos Compose / Docker

| Preferir                                                      | Evitar                                                       |
| ------------------------------------------------------------- | ------------------------------------------------------------ |
| `compose.yml` / `compose.prod.yml`                            | `docker-compose.yml`                                         |
| `docker/<engine>/compose.yml` para servicios de base de datos | Overlays en la raíz usando únicamente `docker-compose.*.yml` |
| `.dockerignore` junto al `Dockerfile`                         | Omitir reglas de exclusión                                   |

Compose se ejecuta utilizando:

```bash
docker compose -f compose.yml …
```

(usa la convención de nombres de archivos de Compose V2).

## Taxonomía de carpetas de extensiones (compatibilidad con CNA)

El nombre de la carpeta debe representar el nivel real de acoplamiento.

El slug del catálogo puede ser más amigable que el nombre de la carpeta, pero nunca debe indicar compatibilidad universal cuando el overlay depende de un stack específico.

| Tipo                 | Patrón de carpeta      | Slug del catálogo                                                            | Campo `type`                                    |
| -------------------- | ---------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------- |
| Universal            | `all-{capability}`     | Normalmente amigable (`github-setup`, `development-container`, `postgres`)   | Lista amplia de tipos de plantillas compatibles |
| Específica del stack | `{stack}-{capability}` | Normalmente coincide con la carpeta (`fastapi-docker`, `fastapi-sqlalchemy`) | Solo ese tipo de plantilla                      |

Ejemplos:

| Carpeta                         | Slug                    | Significado                                                                        |
| ------------------------------- | ----------------------- | ---------------------------------------------------------------------------------- |
| `extensions/all-github-setup`   | `github-setup`          | Automatización CI/repositorio portable                                             |
| `extensions/all-devcontainer`   | `development-container` | Dev Container de VS Code para cualquier plantilla CPA                              |
| `extensions/all-postgres`       | `postgres`              | PostgreSQL mediante Compose únicamente para infraestructura (sin modificar `app/`) |
| `extensions/fastapi-docker`     | `fastapi-docker`        | Dockerfile/Compose con aplicación `uvicorn app.main:app`                           |
| `extensions/django-docker`      | `django-docker`         | Dockerfile/Compose para Django/Gunicorn                                            |
| `extensions/celery-docker`      | `celery-docker`         | Dockerfile/Compose para workers de Celery                                          |
| `extensions/fastapi-sqlalchemy` | `fastapi-sqlalchemy`    | FastAPI con base de datos y Alembic                                                |

Nunca utilices una carpeta o slug genérico como `python-*` para overlays que escriban rutas específicas de FastAPI dentro de `app/` o que utilicen comandos exclusivos de FastAPI.

CI valida esta regla en:

```text
scripts/ci/validate-registry.py
```

Las carpetas de extensiones deben cumplir uno de estos formatos:

* `all-*`
* `{stack}-*` coincidiendo con un único tipo

`python-*` será rechazado.

Cada plantilla del catálogo debe incluir los archivos de calidad indicados más adelante (validado en el nivel de madurez correspondiente después de completar los PR de actualización de plantillas).
## `incompatibleWith` (colisiones de rutas)

Utiliza `incompatibleWith` de forma simétrica cuando dos extensiones puedan sobrescribir las mismas rutas generadas.

Por ejemplo, dos overlays de Docker que incluyen un `Dockerfile` o `compose.yml` para el mismo tipo de plantilla deberían declararse como incompatibles.

Actualmente, las extensiones Docker específicas de cada stack están aisladas por tipo. Cuando un tipo tenga varias estrategias de empaquetado, declara la incompatibilidad mutua siguiendo el mismo patrón que utiliza `cna-templates` para conflictos como Redux saga/thunk.

---

# Requisitos de calidad de las plantillas (todas las plantillas del catálogo)

Cada plantilla registrada en `templates.json` debe incluir como mínimo:

| Área | Requerido |
| --- | --- |
| Arquitectura | Organización de características/módulos apropiada para el stack (no un único módulo plano de tipo "hello world") |
| `docs/` | `README.md`, `PROJECT_STRUCTURE.md`, `CONFIGURATION.md`, `TESTING_GUIDE.md`, `DEPLOYMENT.md`, además de documentación específica del stack (por ejemplo `API.md` para APIs HTTP) |
| Documentación raíz | Un `README.md` sólido (o `.template`), `AGENTS.md`, `CONTRIBUTING.md`, `.env.example` |
| Herramientas | `pyproject.toml` con Ruff + pytest (y herramientas propias del stack); Python tipado documentado |
| Tests | Pruebas reales dentro de `tests/` que cubran rutas principales y de salud |

`fastapi-starter` es la implementación de referencia.

Las nuevas plantillas deben alcanzar este nivel de calidad; no se debe reducir el estándar.

No añadas una segunda plantilla base de FastAPI para tipado estricto.

Las herramientas de tipado y la documentación `docs/TYPING.md` deben vivir dentro de `fastapi-starter`.

Si en el futuro necesitas una configuración de tipado más estricta como opción adicional, crea una extensión ligera como `fastapi-strict-typing` en lugar de crear otra plantilla inicial competidora.

Referencias externas de calidad:
- `cna-templates react-vite-starter`
- `cna-templates nestjs-starter`

---

# Estructura de extensiones

Las extensiones añaden archivos sobre una plantilla compatible.

No definen `cpa.config.json` ni utilizan prompts interactivos.

## Preferir `template/` para evitar sobrescribir el README del banco

El cargador de CPA utiliza preferentemente un subdirectorio `template/` cuando existe (`get_template_dir_path`).

Coloca los archivos que pertenecen al proyecto generado dentro de `template/`.

Mantén el `README.md` de la extensión en la raíz para el catálogo.

Esto sigue el comportamiento de Create-Node-App: el README del catálogo no debe reemplazar el README generado del proyecto.

Ejemplo:

```text
extensions/fastapi-docker/
├── README.md                         # Solo para el catálogo (NO se copia)
└── template/
    ├── Dockerfile
    ├── .dockerignore
    ├── compose.yml
    ├── compose.prod.yml
    └── docs/
        ├── DOCKER_GUIDE.md           # Guía larga para el proyecto generado
        └── README.md.append          # Añadido a docs/README.md
````

## Ejemplo — PostgreSQL universal

```text
extensions/all-postgres/
├── README.md                         # Solo para el catálogo
└── template/
    ├── pyproject.toml                # Parcial — se combina con el manifiesto del proyecto
    ├── .env.example.append           # Añadido al .env.example de la plantilla
    ├── docker/postgres/compose.yml
    ├── docker/postgres/.env.example
    └── docs/
        ├── POSTGRES_GUIDE.md
        └── README.md.append
```

---

# Convención de documentación (compatibilidad con CNA)

Cada extensión que documente características del proyecto generado debe incluir:

| Ruta (dentro de `template/` cuando se utiliza ese patrón) | Función                                                                                                           |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `docs/<TOPIC>_GUIDE.md`                                   | Guía completa: descripción general, qué añade, uso, configuración, verificación, solución de problemas y recursos |
| `docs/README.md.append`                                   | Un elemento que enlaza la guía dentro del índice `docs/README.md` del proyecto                                    |

Patrón más común: un `pyproject.toml` parcial con dependencias para combinar:

```toml
[project]
dependencies = [
  "psycopg[binary]>=3.2",
]
```

Todo lo que se encuentre dentro de la raíz copiada (`template/` o la raíz de la extensión) se copia al proyecto respetando todas las convenciones de sufijos anteriores.
# Python con tipado estático como estándar

Las plantillas nuevas y actualizadas deben considerar Python tipado como el estándar de calidad predeterminado:

- Anota las APIs públicas y utiliza modelos de Pydantic en los límites de la aplicación.
- Documenta `mypy` y/o `pyright` en `README.md`, `docs/TYPING.md` o CI.
- Siempre que sea práctico, incluye las herramientas de tipado dentro de los grupos de dependencias de `pyproject.toml`.
- Las extensiones no deben eliminar el tipado existente (evita overlays sin tipado que entren en conflicto con comprobaciones estrictas).

---

## Conexión automática de extensiones (auto-wiring)

Las extensiones que aportan comportamiento en tiempo de ejecución (middleware, rutas, instrumentación) utilizan el mecanismo `.append` / `.append.template` para conectarse al proyecto generado de forma automática. No se requieren ediciones manuales en los archivos del template base.

Existen dos patrones según el stack.

### FastAPI — registro de providers

El template base `fastapi-starter` incluye `app/core/providers.py` con un registro ligero:

```python
# app/core/providers.py (generado)
AppProvider = Callable[[FastAPI], None]
_providers: list[AppProvider] = []

def register(fn: AppProvider) -> AppProvider: ...
def setup_app(app: FastAPI) -> None: ...
```

`app/main.py` llama a `setup_app(app)` una vez, después de configurar el middleware base.

Las extensiones registran su función de configuración añadiendo `template/app/core/providers.py.append.template`. Se usa el decorador `@register` con un import diferido para evitar ruff E402 (import fuera del bloque inicial):

```python
# extensions/fastapi-cors/template/app/core/providers.py.append.template

@register
def _cors(app: FastAPI) -> None:  # registrado al final — CORS envuelve todo el middleware (LIFO)
    from app.core.cors import setup_cors
    setup_cors(app)
```

**Orden:** los providers se llaman en el orden en que se añaden (orden de addons en el scaffold). Dado que `add_middleware` en FastAPI es LIFO, el middleware añadido en último lugar se convierte en la capa más externa. `fastapi-cors` debe ser siempre la última extensión en la lista de addons cuando el orden importa.

### FastAPI — registro de rutas de funcionalidades

Las extensiones de funcionalidades (auth, chat, …) añaden `template/app/api/router.py.append`:

```python
# extensions/fastapi-auth-jwt/template/app/api/router.py.append
from app.features.auth.router import router as auth_router
router.include_router(auth_router)
```

`router` ya está definido en `app/api/router.py` antes de que se ejecute el contenido añadido.

### Django — append en settings y URLs

Django carga `settings.py` como un módulo Python, por lo que la concatenación de listas y la mutación de dicts son válidas en el ámbito del módulo. Las extensiones añaden contenido a `config/settings.py` y `config/urls.py`:

```python
# extensions/django-spectacular/template/config/settings.py.append
INSTALLED_APPS += ["drf_spectacular"]
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
```

```python
# extensions/django-spectacular/template/config/urls.py.append
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns += [
    path(f"{api_prefix}/schema/", SpectacularAPIView.as_view(), name="schema"),
    ...
]
```

`urlpatterns` y `api_prefix` ya están definidos en el `urls.py` base.

### Adiciones al checklist para extensiones con auto-wiring

- [ ] El archivo de append apunta a una ruta que existe en el template base
- [ ] El archivo de append contiene solo el cable mínimo de configuración, sin duplicar lógica del módulo helper (un decorador `@register` para providers FastAPI, `router.include_router()` para routers FastAPI, o una sentencia `+=` / mutación de dict para settings/URLs de Django)
- [ ] Para extensiones de middleware FastAPI que llamen a `app.add_middleware()`, verificar que la extensión sea la última en la lista de addons en los perfiles CI (última registrada = capa más externa, por la regla LIFO de FastAPI)

---

# Combinación de `pyproject.toml`

Cuando las capas de generación incluyen un archivo `pyproject.toml`, CPA combina su contenido con el archivo de destino en lugar de sobrescribirlo.

| Clave | Comportamiento |
| --- | --- |
| `[project].dependencies` | Unión por nombre del paquete; la capa posterior gana en caso de conflicto de versión |
| `[project].optional-dependencies.*` | Misma unión por grupo |
| `[dependency-groups].*` | Misma unión por grupo (`uv`) |
| Tablas anidadas (`[tool.ruff]`, etc.) | Merge profundo; los valores simples de capas posteriores tienen prioridad |
| Otros arrays | La capa posterior reemplaza el valor anterior |

Ejemplo:

Plantilla base:

```toml
[project]
name = "my-api"
dependencies = ["fastapi>=0.115"]
````

Extensión:

```toml
[project]
dependencies = ["psycopg[binary]>=3.2"]

[dependency-groups]
dev = ["ruff>=0.8"]
```

Resultado:

* Mantiene el nombre del proyecto.
* Une ambas dependencias.
* Añade el grupo `dev`.

Referencia completa:

```text
create-python-app docs/PYPROJECT_MERGE.md
```

---

# Registro en `templates.json`

## Entrada de plantilla

```json
{
  "name": "FastAPI Starter",
  "slug": "fastapi-starter",
  "description": "API FastAPI preparada para producción con uv, ruff y pytest",
  "url": "https://github.com/Create-Python-App/cpa-templates?subdir=templates/fastapi-starter",
  "type": "fastapi-backend",
  "category": "backend-applications",
  "labels": ["FastAPI", "API", "Python", "uv"]
}
```

## Entrada de extensión

```json
{
  "name": "GitHub Setup",
  "slug": "github-setup",
  "description": "CI de GitHub Actions, plantillas de issues y Dependabot",
  "url": "https://github.com/Create-Python-App/cpa-templates?subdir=extensions/all-github-setup",
  "type": ["fastapi-backend", "django-backend", "cli-app", "celery-worker", "uv-workspace"],
  "category": "ci",
  "labels": ["GitHub", "CI", "DevOps"]
}
```

---

# Compatibilidad de tipos

Una plantilla tiene un único valor `type` como cadena.

Una extensión puede tener un valor `type` como cadena o como lista de cadenas.

Una extensión es compatible cuando `template.type` aparece dentro de:

```text
[extension.type].flat()
```

---

# `incompatibleWith`

Declara extensiones mutuamente incompatibles dentro de `templates.json`.

CPA valida estas combinaciones seleccionadas durante la generación del proyecto.

Ejemplo:

```json
{
  "name": "Example A",
  "slug": "example-a",
  "incompatibleWith": ["example-b"],
  "...": "..."
}
```

Cuando dos extensiones tienen conflictos lógicos (por ejemplo, dos opciones de middleware o dos runtimes de contenedores), añade `incompatibleWith` en ambas entradas.

Utiliza esto para conflictos reales de funcionalidad.

Para restricciones más suaves entre dependencias utiliza versiones (`semver`) o reglas de compatibilidad.

Esquema:

```text
templates.schema.json → extensions[].incompatibleWith
```

---

# Orden de generación

1. Resolver las URLs de plantillas y extensiones desde `templates.json` (o desde una URL `file://` / GitHub).
2. Clonar o abrir los directorios fuente (guardados en caché dentro de `~/.cache/cpa` para repositorios remotos).
3. Para cada capa, copiar desde `template/` cuando exista; de lo contrario, copiar desde la raíz de la capa.
4. Procesar archivos `.template`, `.append` y sufijos relacionados.
5. Combinar los archivos `pyproject.toml` de todas las capas.
6. Ejecutar `uv sync` cuando exista `pyproject.toml` (excepto con `--no-install`).
7. Inicializar Git (excepto si `CPA_SKIP_GIT=1`).

Consulta `ARCHITECTURE.md` para conocer la descripción completa del sistema.

---

## Pruebas locales

Apunta la CLI a un checkout local:

```bash
export CPA_TEMPLATES_URL="file:///path/to/cpa-templates"

CI=true uvx create-awesome-python-app my-app \
  --template fastapi-starter \
  --addons github-setup fastapi-docker \
  --no-interactive

cd my-app
```

Verifica el resultado generado:

```bash
uv sync
uv run ruff check .
uv run pytest
```

También ejecuta cualquier comprobación específica de extensiones documentada en el README de cada extensión.
---

# Lista de comprobación para nuevas plantillas

* `cpa.config.json` junto a la plantilla (si necesita prompts).
* `pyproject.toml` con metadatos válidos para un proyecto `uv`.
* Arquitectura de características/módulos (no un ejemplo plano de "hello world").
* Python tipado documentado (y herramientas configuradas cuando corresponda): `mypy` / `pyright`.
* Los archivos `.template` utilizan únicamente variables Jinja definidas.
* Entrada añadida a `templates.json` con el `type` y categoría correctos.
* `README`, `CONTRIBUTING`, `AGENTS` y documentación completa en `docs/` (según los requisitos de calidad).
* Prueba local de generación completada correctamente.

---

# Lista de comprobación para nuevas extensiones

* La carpeta sigue la taxonomía `all-*` o `{stack}-*` (sin usar `python-*` para código específico de un stack).
* Los tipos compatibles coinciden con las plantillas objetivo; solo usa compatibilidad amplia cuando sea realmente portable.
* Los archivos generados están dentro de `template/`; el `README.md` del catálogo permanece fuera y no sobrescribe el README del proyecto.
* Incluye `docs/<TOPIC>_GUIDE.md` y `docs/README.md.append` cuando añade documentación al proyecto generado.
* Usa un `pyproject.toml` parcial únicamente cuando añada dependencias.
* Los archivos `.append` apuntan a rutas existentes en la plantilla base.
* Los archivos Compose siguen las convenciones `compose.yml` / `docker/<engine>/`.
* Define `incompatibleWith` para extensiones mutuamente incompatibles.
* El README del catálogo explica cuándo usar la extensión, qué copia y cómo verificarla.
* La entrada de `templates.json` existe y la URL `subdir` coincide con el nombre de la carpeta.

---

# Futuras plantillas

Las plantillas planificadas que todavía no están registradas se encuentran en:

```text
FUTURE_TEMPLATES.md
```

---

# Catálogo AI/ML

Para conocer la taxonomía de AI/ML, las categorías y las reglas entre plantillas y extensiones consulta:

```text
AI_ML_AUTHORING.md
```