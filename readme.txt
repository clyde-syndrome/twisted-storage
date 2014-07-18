To setup server running you need python 2.7 to be installed
Get the server code from git repo

You can use virtualenv 
Make virtual environment with command:
virtualenv env
Then activate it like so:
source env/bin/activate
When you install environment you should setup some packages with command:
pip install -r requirements.txt
In the server script edit the PORT constant to listen on
Then run the server script:
python server.py

If you dont want to use virtualenv then you need twisted to be installed:
pip install twisted

When server is running in the top of client script edit HOST and PORT parameters
Already you need twisted if you run client script on other computer then server script
Use virtualenv or just install twisted with pip command:
pip install twisted


The client implements several commands to work with key-value in-memory storage.
When you open client window threre will be text input and two buttons DO COMMAND and QUIT
Enter you command and press DO COMMAND button to execute it


get - get value from storage by key. example "get,q"
set - set key and value. example "set,q,1"
del - delete key from storage. example "del,q"
all - get all key and their values from storage. exapmle "all"
exit - shutdown client and close connection

Also client supports multiple commands.
To execute several commands you need to separate them with semicolon
example:
"set,q,1;set,w,2;set,e,3;all"

Client will retrive session after disconnect.


