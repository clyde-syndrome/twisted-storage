from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

#set port to listen on
PORT = 8123


class GlobalStore():
    '''Class for saving sessions with storages'''
    store = {}        

    def get_storage(self,client_id):
        '''get or create new storage'''
        if client_id not in self.store.keys():
            self.store[client_id] = Storage(client_id)
        return self.store[client_id]


class Storage():
    '''Key-value storage'''

    def __init__(self,client_id):
        self.client_id = client_id
        self.stack = {}

    def get_key(self,key):
        '''gets value by key'''
        return self.stack[key]

    def set_value(self,key,value):
        '''sets value'''
        self.stack[key] = value

    def del_key(self,key):
        '''deletes some key frrom storage'''
        del self.stack[key]

    def get_all(self):
        '''gets all key and values from storage'''
        data = ''
        for i,key in enumerate(self.stack.keys()):
            data += key+':'+self.stack[key]
            if (i+1) != len(self.stack.keys()):
                data += ','
        return data

class ClientProtocol(LineReceiver):
    '''Protocol for serving clients'''
    def __init__(self, factory):
        self.factory = factory
        self.auth = False
        

    def connectionMade(self):
        '''Sends text when connection is established'''
        self.sendLine("You are connected")

    def connectionLost(self,reason):
        '''Closes connection'''
        self.transport.loseConnection()

    def lineReceived(self, line):
        '''Commands dispatcher'''
        if self.auth:
            data = line.strip()
            cmds = data.split(";")
            for c in cmds:
                cmd = c.split(",")
                if cmd[0] == 'set':
                    self.command_set(cmd[1],cmd[2])
                elif cmd[0] == 'get':
                    self.command_get(cmd[1])
                elif cmd[0] == 'del':
                    self.command_del(cmd[1])
                elif cmd[0] == 'all':
                    self.command_all()
                elif cmd[0] == 'exit':
                    self.transport.loseConnection()
                else:
                    self.command_undefined(cmd[0])
        else:
            client_id_data = line.split(',')
            if client_id_data[0] == 'auth':
                self.storage = global_store.get_storage(client_id_data[1])
                self.auth = True


    def command_set(self, key, val):
        '''set command'''
        self.storage.set_value(key,val)
    def command_get(self,key):
        '''get command'''
        val = self.storage.get_key(key)
        self.sendLine(val)
    def command_del(self,key):
        '''delete command'''
        self.storage.del_key(key)
    def command_all(self):
        '''get all data command'''
        val = self.storage.get_all()
        self.sendLine(val)
    def command_undefined(self,cmd):
        '''undefined command'''
        pass


class ClientFactory(Factory):
    '''Factory for serving connections'''
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        '''Builds protocol for each client'''
        return ClientProtocol(self)

#global storage instantiation
global_store = GlobalStore()
#create factory
factory = ClientFactory()

#run reactor
from twisted.internet import reactor
reactor.listenTCP(PORT, factory)
reactor.run()

