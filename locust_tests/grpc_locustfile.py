import grpc
from locust import User, task, between
from locust.exception import LocustError
import time
import random
import sys
import os

from protos import glossary_pb2, glossary_pb2_grpc


class GrpcClient:
    def __init__(self, host):
        self.host = host
        credentials = grpc.ssl_channel_credentials()
        self.channel = grpc.secure_channel('grpc.dzhevelik.com:443', credentials)
        self.stub = glossary_pb2_grpc.GlossaryServiceStub(self.channel)
    
    def get_all_terms(self):
        start_time = time.time()
        try:
            response = self.stub.GetAllTerms(glossary_pb2.Empty())
            total_time = int((time.time() - start_time) * 1000)
            return True, total_time, len(response.terms)
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            return False, total_time, str(e)
    
    def get_term(self, keyword):
        start_time = time.time()
        try:
            request = glossary_pb2.GetTermRequest(keyword=keyword)
            response = self.stub.GetTerm(request)
            total_time = int((time.time() - start_time) * 1000)
            return True, total_time, response.keyword
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            return False, total_time, str(e)
    
    def create_term(self, keyword, definition):
        start_time = time.time()
        try:
            request = glossary_pb2.CreateTermRequest(
                keyword=keyword,
                definition=definition,
                category="Test",
                source="Locust"
            )
            response = self.stub.CreateTerm(request)
            total_time = int((time.time() - start_time) * 1000)
            return True, total_time, response.keyword
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            return False, total_time, str(e)
    
    def get_graph(self):
        start_time = time.time()
        try:
            response = self.stub.GetGraph(glossary_pb2.Empty())
            total_time = int((time.time() - start_time) * 1000)
            return True, total_time, len(response.nodes)
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            return False, total_time, str(e)

class GlossaryGRPCUser(User):
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = GrpcClient("grpc.dzhevelik.com:443")
        self.terms = []
    
    @task(10)
    def get_all_terms(self):
        success, response_time, result = self.client.get_all_terms()
        if success:
            self.environment.events.request.fire(
                request_type="grpc",
                name="GetAllTerms",
                response_time=response_time,
                response_length=result,
                exception=None,
                context={}
            )
        else:
            self.environment.events.request.fire(
                request_type="grpc",
                name="GetAllTerms",
                response_time=response_time,
                response_length=0,
                exception=LocustError(result),
                context={}
            )
    
    @task(5)
    def get_single_term(self):
        keywords = ["Блокчейн", "Ethereum Virtual Machine", "Layer 2", "Proof of Stake", "Смарт-контракт"]
        keyword = random.choice(keywords)
        success, response_time, result = self.client.get_term(keyword)
        
        if success:
            self.environment.events.request.fire(
                request_type="grpc",
                name="GetTerm",
                response_time=response_time,
                response_length=len(str(result)),
                exception=None,
                context={}
            )
        else:
            self.environment.events.request.fire(
                request_type="grpc",
                name="GetTerm",
                response_time=response_time,
                response_length=0,
                exception=LocustError(result),
                context={}
            )
    
    @task(2)
    def create_term(self):
        test_id = random.randint(1000, 9999)
        keyword = f"LoadTest{test_id}"
        definition = f"Термин для нагрузочного тестирования {test_id}"
        
        success, response_time, result = self.client.create_term(keyword, definition)
        
        if success or "ALREADY_EXISTS" in str(result):
            self.environment.events.request.fire(
                request_type="grpc",
                name="CreateTerm",
                response_time=response_time,
                response_length=len(str(result)),
                exception=None,
                context={}
            )
        else:
            self.environment.events.request.fire(
                request_type="grpc",
                name="CreateTerm",
                response_time=response_time,
                response_length=0,
                exception=LocustError(result),
                context={}
            )
    
    @task(1)
    def get_graph(self):
        success, response_time, result = self.client.get_graph()
        
        if success:
            self.environment.events.request.fire(
                request_type="grpc",
                name="GetGraph",
                response_time=response_time,
                response_length=result,
                exception=None,
                context={}
            )
        else:
            self.environment.events.request.fire(
                request_type="grpc",
                name="GetGraph",
                response_time=response_time,
                response_length=0,
                exception=LocustError(result),
                context={}
            )
