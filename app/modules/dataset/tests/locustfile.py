from locust import HttpUser, TaskSet, task
from core.locust.common import get_csrf_token
from core.environment.host import get_host_for_locust_testing
import random
from faker import Faker

fake = Faker()

def get_csrf_token(response):
    """Extrae el token CSRF de una respuesta HTML si es necesario."""
    token = response.cookies.get('csrf_token') 
    return token

class DatasetBehavior(TaskSet):
    def on_start(self):
        self.login()

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

    @task(1)
    def dataset(self):
        response = self.client.get("/dataset/upload")
        get_csrf_token(response)


class RatingBehavior(TaskSet):
    @task(1)
    def rate_dataset(self):
        """
        Calificar un dataset
        """
        dataset_id = random.randint(1, 6)  
        user_id = 1  
        
        rating_data = {
            "user_id": user_id,
            "dataset_id": dataset_id,
            "quality": random.uniform(1, 5),  
            "size": random.uniform(1, 5),     
            "usability": random.uniform(1, 5)  
        }
        
        response = self.client.post(
            "/rate",  
            data=json.dumps(rating_data),
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Calificación para dataset {dataset_id} realizada, respuesta: {response.status_code}")
        get_csrf_token(response)  

class DatasetUser(HttpUser):
    tasks = [DatasetBehavior, RatingBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
