# Time Game Challenge API

API RESTful desarrollada con **FastAPI** que permite a los usuarios jugar un juego de precisión donde deben detener un cronómetro lo más cerca posible de los **10 segundos**. La sessión expira si no se completa en 30 minutos.

Incluye:

- Registro y autenticación con JWT
- Iniciar/detener sesiones de juego
- Leaderboard global
- Analytics personales
- Testing con `pytest`
- Docker multistage + `make` para facilitar la ejecución

---

## Setup (Modo local)

### Crear y configurar entorno virtual

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Crear archivo `.env`

```dotenv
# .env

# Database
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3

# JWT
JWT_SECRET_KEY=clave_super_secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
APP_TITLE=Time It Right Game API
APP_VERSION=0.1.0
```

### Ejecutar en modo local

```bash
uvicorn app.main:app --reload
```

Accedé a la documentación Swagger en:  
 http://localhost:8000/docs

---

## Docker (recomendado)

###  Build y run

```bash
make build
make up
```

###  Detener contenedor

```bash
make down
```

---

## Autenticación

### `POST /auth/register`

```json
{
  "username": "marco123",
  "email": "marco@example.com",
  "password": "123456"
}
```

### `POST /auth/login`

```json
{
  "email": "marco@example.com",
  "password": "123456"
}
```

Devuelve:

```json
{
  "access_token": "ey...",
  "token_type": "bearer"
}
```

---

## Endpoints

### `/games/start`  
Inicia una nueva sesión (requiere token).

###  `/games/{session_id}/stop`  
Detiene la sesión y calcula duración y desviación.

### `/leaderboard?page=1&size=10`  
Top 10 jugadores con menor desviación promedio.

### `/analytics/user/{user_id}`  
Estadísticas personales: partidas, desviación promedio y mejor.

---

## Testing

### Correr tests

```bash
make test
```

O directamente:

```bash
PYTHONPATH=./ pytest -s
```

---

## Stack

- FastAPI
- SQLAlchemy 2.0 Async
- Pydantic v2
- SQLite + aiosqlite
- Uvicorn
- jose (JWT)
- passlib + bcrypt
- pytest + httpx
- docker + multistage
- dotenv

---

## Deploy

Tu app está en producción:

[Ver API en producción](https://time-game-challenge-production.up.railway.app/docs)


## Autor

Marco Romero  
 marcoromero.dev@gmail.com  
 [LinkedIn](https://www.linkedin.com/in/marco-romero-at)