from locust import HttpUser, TaskSet, task
import random
from faker import Faker  # Para generar datos aleatorios

fake = Faker()


def get_csrf_token(response):
    """Extrae el token CSRF de una respuesta HTML si es necesario."""
    # Esto es un ejemplo, ajusta según cómo tu aplicación gestione los tokens
    token = response.cookies.get('csrf_token')  # O busca en el HTML si aplica
    return token


class SocialActions(TaskSet):
    def on_start(self):
        """Asegúrate de iniciar sesión antes de realizar cualquier acción."""
        self.ensure_logged_out()
        self.login()

    @task(2)
    def follow_user(self):
        """Simula la acción de seguir a un usuario."""
        user_id = random.choice([1, 2, 3, 4])
        response = self.client.post(f"/follow/{user_id}")
        if response.status_code != 200:
            print(f"Error al seguir al usuario {user_id}: {response.status_code}")

    @task(1)
    def unfollow_user(self):
        """Simula la acción de dejar de seguir a un usuario."""
        user_id = random.choice([1, 2, 3, 4])
        response = self.client.post(f"/unfollow/{user_id}")
        if response.status_code != 200:
            print(f"Error al dejar de seguir al usuario {user_id}: {response.status_code}")

    @task(2)
    def get_messages(self):
        """Simula la obtención de mensajes con un amigo."""
        user_id = random.choice([1, 2, 3, 4])
        response = self.client.get(f"/get_messages?friend_id={user_id}")
        if response.status_code != 200:
            print(f"Error al obtener mensajes del usuario {user_id}: {response.status_code}")

    @task(1)
    def send_message(self):
        """Simula el envío de un mensaje."""
        user_id = random.choice([1, 2, 3, 4])
        message = fake.sentence()
        data = {"followed_id": user_id, "text": message}
        response = self.client.post("/send_message", json=data)
        if response.status_code != 204:
            print(f"Error al enviar mensaje al usuario {user_id}: {response.status_code}")

    @task(2)
    def get_comments(self):
        """Simula la obtención de comentarios para un dataset."""
        dataset_id = random.choice([101, 102])
        response = self.client.get(f"/get_comments?dataset_id={dataset_id}")
        if response.status_code != 200:
            print(f"Error al obtener comentarios del dataset {dataset_id}: {response.status_code}")

    @task(1)
    def send_comment(self):
        """Simula el envío de un comentario."""
        user_id = random.choice([1, 2, 3, 4])
        dataset_id = random.choice([101, 102])
        message = fake.sentence()
        data = {"followed_id": user_id, "dataset_id": dataset_id, "text": message}
        response = self.client.post("/send_comment", json=data)
        if response.status_code != 204:
            print(f"Error al enviar comentario al dataset {dataset_id}: {response.status_code}")

    def ensure_logged_out(self):
        """Asegura que la sesión esté cerrada antes de intentar iniciar sesión."""
        response = self.client.get("/logout")
        if response.status_code != 200:
            print(f"No se pudo cerrar sesión correctamente: {response.status_code}")

    def login(self):
        """Inicia sesión en la aplicación."""
        response = self.client.get("/login")
        csrf_token = get_csrf_token(response)

        response = self.client.post("/login", data={
            "email": "user@example.com",
            "password": "test1234",
            "csrf_token": csrf_token
        })
        if response.status_code != 200:
            print(f"Error al iniciar sesión: {response.status_code}")


class SocialUser(HttpUser):
    tasks = [SocialActions]
    min_wait = 5000
    max_wait = 9000
    host = "http://localhost:5000"  # Cambia esto según tu configuración
