import grpc

import service_pb2
import service_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')  # Адрес сервера
    stub = service_pb2_grpc.MyServiceStub(channel)

    request = service_pb2.Request(id = 1, par_1 = 5, par_2 = 4)
    response = stub.MyMethod(request)
    print(response.result)

if __name__ == '__main__':
    run()
