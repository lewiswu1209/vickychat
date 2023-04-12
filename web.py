
from web import app
from config import host
from config import port

if __name__ == '__main__':
    app.run( host = host, port = port )
