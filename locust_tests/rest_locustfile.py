from locust import HttpUser, task, between
import random

class GlossaryRESTUser(HttpUser):
    host = "https://vkr.dzhevelik.com"
    wait_time = between(1, 3)
    
    def on_start(self):
        self.terms = []
    
    @task(10)
    def get_all_terms(self):
        with self.client.get("/api/terms", catch_response=True) as response:
            if response.status_code == 200:
                self.terms = response.json()
                response.success()
            else:
                response.failure(f"Got status {response.status_code}")
    
    @task(5)
    def get_single_term(self):
        if self.terms:
            term = random.choice(self.terms)
            keyword = term.get("keyword", "")
            with self.client.get(f"/api/terms/{keyword}", catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Got status {response.status_code}")
    
    @task(2)
    def create_term(self):
        test_id = random.randint(1000, 9999)
        payload = {
            "keyword": f"LoadTest{test_id}",
            "definition": f"Термин для нагрузочного тестирования {test_id}",
            "category": "Test",
            "source": "Locust"
        }
        with self.client.post("/api/terms", json=payload, catch_response=True) as response:
            if response.status_code in [200, 201]:
                response.success()
            elif response.status_code == 400:
                response.success()
            else:
                response.failure(f"Got status {response.status_code}")
    
    @task(1)
    def get_graph(self):
        with self.client.get("/api/graph", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status {response.status_code}")
                