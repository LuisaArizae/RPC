from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import socket #permite conectar dos programas en red para intercambiar datos en este caso ips

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
# Create server
hostIP=str(socket.gethostbyname(socket.gethostname()))
with SimpleXMLRPCServer((hostIP, 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods (in this case, just 'mul').
    class Index:
        def __init__(self)->None:
            self.registeredList={} #clients ips and names

        #Register a client Lo usan los clientes
        def register(self, ip, name):
            self.registeredList[name]=ip
            #Send clients IP to all clients
            self.sendRegisteredClientsList() # funcion para mandar a todos la lista con nombres
            return self.registeredList

        #Send registered clients list to all clients
        def sendRegisteredClientsList(self):
            print("Clients List:")
            print(self.registeredList)
            cpRegisteredList=self.registeredList
            for key in self.registeredList:
                IPClient = self.registeredList.get(key)
                sc = xmlrpc.client.ServerProxy('http://'+IPClient+':8000')
                sc.updateClientsList(cpRegisteredList)
                
    server.register_instance(Index())

    # Run the server's main loop
    print("Server Index actived in: "+hostIP)
    server.serve_forever()