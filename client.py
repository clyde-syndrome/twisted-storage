import os
import uuid
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from Tkinter import *
from twisted.internet import tksupport

#edit this parameters for your connection
HOST = 'localhost'
PORT = 8123

class Client(LineReceiver):
    '''Client protocol class'''

    def connectionMade(self):
        '''Called when the connection is established'''
        self.sendLine('auth,'+token)

    def lineReceived(self, line):
        '''Called when any data retrieved from the server'''
        app.response(line)

    def connectionLost(self, reason):
        '''Called when connection loses'''
        self.transport.loseConnection()
    


class MyClientFactory(ClientFactory):
    '''Client Factory class'''

    def clientConnectionFailed(self, connector, reason):

        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()

    def buildProtocol(self, addr):
        '''Builds protocol for connection'''
        self.connection = Client()
        return self.connection

    def send(self,text):
        '''Send data to the server'''
        self.connection.sendLine(text)

    def stop(self):
        '''Stopes the program execution'''
        self.connection.connectionLost('quit')




class App():
    '''Tkinter GUI class'''
    
    def __init__(self, master, client):
        self.client = client
        self.frame = Frame(master)
        self.frame.grid(row=2,column=3)
        
        
        self.button = Button(self.frame, text="DO COMMAND", command=self.send_command)
        self.button.grid(row=1,column=1)
        self.quitbutton = Button(self.frame, text="QUIT", fg='red',command=self.quit)
        self.quitbutton.grid(row=1,column=2)
        
        self.sendtext = Entry(self.frame,width=60)
        self.sendtext.grid(row=1,column=0)
        
        gettext = Text(self.frame,height=10,width=80,wrap=WORD)
        self.gettext = gettext
        gettext.grid(row=0,columnspan=3)
        gettext.insert(END,'Welcome to my key-value store\n')
        gettext.insert(END,'Use commands below:\n')
        gettext.insert(END,'get - get value from storage by key. example "get,q"\n')
        gettext.insert(END,'set - set key and value. example "set,q,1"\n')
        gettext.insert(END,'del - delete key from storage. example "del,q"\n')
        gettext.insert(END,'all - get all key and their values from storage. exapmle "all"\n')
        gettext.insert(END,'exit - shutdown client and close connection\n')
        gettext.insert(END,'multiple commands need to be separated by semicolon\n')

        gettext.configure(state='disabled')

    def quit(self):
        '''exit from application'''
        client.stop()
        
    def send_command(self):
        '''send command to server'''
        text = self.sendtext.get()
        self.sendtext.delete(0,END)
        self.client.send(text)

    def response(self,data):
        '''handle response from server'''
        self.gettext.configure(state='normal')
        self.gettext.insert(END,'%s\n'%data)
        self.gettext.configure(state='disabled')

        

def generate_token():
    '''generate token for session'''
    return "".join(str(uuid.uuid4()).split('-'))


#generate and handle token
current_dir = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(current_dir,'config.cfg')
if not os.path.exists(config):
    cf = open(config,'w')
    cf.write(generate_token())
    cf.close()

cf = open(config,'r')
token = cf.read()
cf.close()

#instantiate factory
client = MyClientFactory()
#create app gui
root = Tk()
root.title('Client')
root.resizable(width=FALSE, height=FALSE)
app = App(root,client)
tksupport.install(root)
#run reactor
reactor.connectTCP(HOST,PORT,client)
reactor.run()