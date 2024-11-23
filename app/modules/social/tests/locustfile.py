from locust import HttpUser, task, between
import random


class SocialUser(HttpUser):
    wait_time = between(1, 5)
    user_ids = [1, 2, 3, 4]  # IDs conocidos de usuarios para pruebas

    def on_start(self):
        # Inicia sesión al comienzo de cada sesión de usuario simulada
        with self.client.post("/login", data={
            "email": "user@example.com",
            "password": "test1234"
        }, catch_response=True) as response:
            if response.status_code == 200:
                print("Inicio de sesión exitoso.")
            else:
                print(f"Error al iniciar sesión: {response.status_code}")
                response.failure(f"Inicio de sesión fallido: {response.status_code}")

    @task(2)
    def follow_user(self):
        # Simula la acción de seguir a un usuario
        user_id = random.choice(self.user_ids)
        with self.client.post(f"/follow/{user_id}", catch_response=True) as response:
            if response.status_code == 200:
                print(f"Se siguió exitosamente al usuario {user_id}.")
            else:
                print(f"Error al seguir al usuario {user_id}: {response.status_code}")
                response.failure(f"Error al seguir al usuario {user_id}: {response.status_code}")

    @task(1)
    def unfollow_user(self):
        # Simula la acción de dejar de seguir a un usuario
        user_id = random.choice(self.user_ids)
        with self.client.post(f"/unfollow/{user_id}", catch_response=True) as response:
            if response.status_code == 200:
                print(f"Se dejó de seguir exitosamente al usuario {user_id}.")
            else:
                print(f"Error al dejar de seguir al usuario {user_id}: {response.status_code}")
                response.failure(f"Error al dejar de seguir al usuario {user_id}: {response.status_code}")

    def on_stop(self):
        # Cierra sesión al finalizar cada sesión de usuario simulada
        with self.client.get("/logout", catch_response=True) as response:
            if response.status_code == 200:
                print("Cierre de sesión exitoso.")
            else:
                print(f"Error al cerrar sesión: {response.status_code}")
                response.failure(f"Error al cerrar sesión: {response.status_code}")
