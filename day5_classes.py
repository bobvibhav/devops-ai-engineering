class Server:
    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.status = "stopped"

    def start(self):
        self.status = "running"
        print(f"{self.name} is now running in {self.region}")
        
server1 = Server("web-server-1", "eu-west-1")
Server.start(server1)
server1.start()
print(server1.name)
print(server1.status)
