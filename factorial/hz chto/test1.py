from concurrent import futures
import grpc

import service_pb2
import service_pb2_grpc

class MyService(service_pb2_grpc.MyServiceServicer):
    def MyMethod(self, request, context):
        # Обработка запроса и формирование ответа
        response = service_pb2.Response(result="Hello, " + request.message + request.id)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    service_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')  # Порт, на котором будет слушать сервер
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()



# 