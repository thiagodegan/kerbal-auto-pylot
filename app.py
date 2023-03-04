from flask import Flask, render_template
import krpc
import threading
import time
from integracao import Telemetria

# cria uma classe pra rodar em thread paralela

"""
class MyThread(threading.Thread):
    def __init__(self, callbackAlt):
        super(MyThread, self).__init__()
        self.callbackAlt = callbackAlt

    def run(self):
        print('Thread Executando')
        for i in range(10):
            time.sleep(10)
            self.callbackAlt(i)


def retornoAlt(chamada):
    print(f'Executando chamada da th: {chamada}')


th = MyThread(retornoAlt)
th.daemon = True
th.start()

"""


def altitudeMarCallback(altitude):
    print(f'Altitude Mar: {altitude}')


def altitudeSoloCallback(altitude):
    print(f'Altitude Solo: {altitude}')


def apoastroCallback(apoastro):
    print(f'Apoastro: {apoastro}')


def periatroCallback(periastro):
    print(f'Periastro: {periastro}')


def angulacaoCallback(angulo):
    print(f'Angulo: {angulo}')


tel = Telemetria(AltitudeMarCallback=altitudeMarCallback,
                 AltitudeSoloCallback=altitudeSoloCallback,
                 ApoastroCallback=apoastroCallback,
                 PeriastroCallback=periatroCallback,
                 AngulacaoCallback=angulacaoCallback)
tel.daemon = True
tel.start()

app = Flask(__name__)

app.config["DEBUG"] = True


@app.route('/')
def index():
    return render_template('index.html', conectado=False)
