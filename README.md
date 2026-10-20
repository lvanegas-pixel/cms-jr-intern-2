## 1. Entorno

```bash
# 1. Crea y activa el entorno virtual
python -m venv venv
source venv/bin/activate        # macOS/Linux
# .\venv\Scripts\activate       # Windows

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Copia el archivo de entorno (el .env real NUNCA se commitea)
cp .env.example .env

# 4. Crea el proyecto Django (si aún no existe)
django-admin startproject config .

# 5. Primeras migraciones + superusuario (para el admin)
python manage.py migrate
python manage.py createsuperuser

# 6. Arranca
python manage.py runserver
```

Abre http://127.0.0.1:8000/ y http://127.0.0.1:8000/admin/ — si ves ambas, +10 pts 🎉

## 2. Correr los tests

```bash
pytest
```

## 3. Login

Hay un POST específico de Login tal que: 
POST {{base_url}}/api/login/
body: {
    "username": "username",
	"password": "password"
}

example of result: token	64c1bb9b646b7a1ffca85b0f318eecb137974daf
