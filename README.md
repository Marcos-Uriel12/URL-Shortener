# URL Shortener

API REST para acortar URLs construida con FastAPI, SQLAlchemy y MySQL.

## Descripción

Permite crear URLs cortas a partir de URLs largas, redirigir a la URL original y consultar estadísticas de clics. Usa Alembic para migraciones de base de datos.

## Instalación y ejecución

**Requisitos:** Python 3.10+, MySQL

```bash
# CLonar el repo
git clone https://github.com/Marcos-Uriel12/URL Shortener

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (ver sección siguiente)
cp .env.example .env

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`.  
Documentación interactiva en `http://localhost:8000/docs`.

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

| Variable       | Descripción                          | Ejemplo                                          |
|----------------|--------------------------------------|--------------------------------------------------|
| `DATABASE_URL` | Cadena de conexión a MySQL           | `mysql+pymysql://user:pass@localhost:3306/db`    |
| `SECRET_KEY`   | Clave secreta para la aplicación     | `una-clave-secreta-muy-larga-random`             |

## Endpoints

| Método   | Ruta                    | Descripción                                      |
|----------|-------------------------|--------------------------------------------------|
| `GET`    | `/urls`                 | Lista todas las URLs (paginado: `page`, `limit`) |
| `POST`   | `/shorten`              | Crea una URL corta a partir de una URL larga     |
| `GET`    | `/{short_code}`         | Redirige a la URL original (302) e incrementa clics |
| `GET`    | `/stats/{short_code}`   | Retorna estadísticas de una URL corta            |
| `DELETE` | `/urls/{short_code}`    | Elimina una URL corta                            |

### Ejemplos

**POST /shorten**
```json
// Request
{ "original_url": "https://ejemplo.com/articulo-muy-largo" }

// Response 201
{
  "id": 1,
  "original_url": "https://ejemplo.com/articulo-muy-largo",
  "short_code": "aB3xYz",
  "clicks": 0,
  "created_at": "2026-04-20T10:00:00"
}
```

**GET /urls?page=1&limit=10**
```json
{
  "urls": [...],
  "total": 25,
  "page": 1,
  "total_pages": 3,
  "limit": 10
}
```

## Correr con Docker

**Requisitos:** Docker y Docker Compose instalados.

```bash
docker compose up --build
docker compose exec api alembic upgrade head
```

Levanta la API en `http://localhost:8001` y una base de datos MySQL en el puerto `3308`.  
Las variables de entorno ya están configuradas en el `docker-compose.yml`.

> Para detener: `docker compose down`  
> Para eliminar también los datos: `docker compose down -v`

## Correr tests

Los tests usan SQLite en memoria, no requieren MySQL.

```bash
# Instalar dependencias de desarrollo (si no están instaladas)
pip install pytest httpx

# Correr todos los tests
pytest tests/

# Con output detallado
pytest tests/ -v
```
## Roadmap.sh
Url: https://roadmap.sh/projects/url-shortening-service
