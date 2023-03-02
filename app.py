from flask import Flask, render_template
import krpc


conn = None
vessel = None


def conectarKsp():
    """Conecta no KSP"""
    try:
        return krpc.connect(name='Kerbal Auto-Pylot')
    except ConnectionRefusedError:
        print('Conexão recusada, verifique se o KRPC está ativo...')


def getVessel(conn):
    """Retorna a nave"""
    if (conn != None):
        return conn.space_center.active_vessel
    else:
        print('A conexão não foi estabelicida!')
    return None


conn = conectarKsp()
vessel = getVessel(conn=conn)

app = Flask(__name__)

app.config["DEBUG"] = True


@app.route('/')
def index():
    if vessel == None:
        return render_template('index.html', conectado=False)
    else:
        return render_template('index.html', conectado=True, nave=getVessel, conn=conn)
