import krpc
import threading
import time


class Telemetria(threading.Thread):
    def __init__(self, ApoastroCallback=None, PeriastroCallback=None, AltitudeMarCallback=None, AltitudeSoloCallback=None, AngulacaoCallback=None):
        super(Telemetria, self).__init__()
        self.apoastroCall = ApoastroCallback
        self.periastroCall = PeriastroCallback
        self.altitudeMarCall = AltitudeMarCallback
        self.altitudeSoloCall = AltitudeSoloCallback
        self.angulacaoCall = AngulacaoCallback
        self.conn = None
        self.KSPConectado = False
        self.CurrentScenne = None
        self.vessel = None
        self.altitudeMarStr = None
        self.altitudeSoloStr = None
        self.altitudeMar = 0
        self.altitudeSolo = 0
        self.apoastroStr = None
        self.apoastro = 0
        self.periastroStr = None
        self.periastro = 0
        self.angulacaoStr = None
        self.angulacao = 0

    def checkCon(self):
        """Verifica se precisa conectar com o KSP"""
        try:
            if self.conn == None:
                self.conn = krpc.connect(name="KSP - Auto-Pylot")
                self.KSPConectado = True
                print('KRPC conectado...')
        except ConnectionRefusedError as conRefused:
            self.conn = None
            self.KSPConectado = False
            print(
                'Erro checkConn: Conexão recusada! Verifique se o KSP está ativo com o KRPC.')
        except Exception as e:
            self.conn = None
            self.KSPConectado = False
            print(f'Erro checkCon: {e}')
            raise e

    def getCurrentScenne(self):
        """Atualiza a Cena atual"""
        try:
            self.CurrentScenne = None
            if self.KSPConectado:
                self.CurrentScenne = self.conn.krpc.current_game_scene
                if self.CurrentScenne.name == 'flight':
                    self.vessel = self.conn.space_center.active_vessel
                else:
                    self.vessel = None
                    self.apoastroStr = None
                    self.periastroStr = None
                    self.angulacaoStr = None
                    self.altitudeMarStr = None
                    self.altitudeSoloStr = None
                    self.angulacaoStr = None

        except Exception as e:
            print(f'Erro ao capturar a cena atual: {e}')
            raise e

    def configApoastroStream(self):
        """Configura o Stream para capturar o Apoastro"""
        try:
            if self.CurrentScenne != None and self.CurrentScenne.name == 'flight':
                if self.apoastroStr == None:
                    self.apoastroStr = self.conn.add_stream(
                        getattr, self.vessel.orbit, 'apoapsis_altitude')
        except Exception as e:
            print(f'Erro configApoastroStrem: {e}')

    def configPeriastroStream(self):
        """Configura o Stream para capturar o Periastro"""
        try:
            if self.CurrentScenne != None and self.CurrentScenne.name == 'flight':
                if self.periastroStr == None:
                    self.periastroStr = self.conn.add_stream(
                        getattr, self.vessel.orbit, 'periapsis_altitude')
        except Exception as e:
            print(f'Erro configPeriastroStream: {e}')

    def configAltitudeMarStream(self):
        """Configura o Stream para captuar a altitude em relacao ao mar"""
        try:
            if self.CurrentScenne != None and self.CurrentScenne.name == 'flight':
                if self.altitudeMarStr == None:
                    self.altitudeMarStr = self.conn.add_stream(
                        getattr, self.vessel.flight(), 'mean_altitude')
            else:
                self.altitudeMarStr = None
        except Exception as e:
            print(f'Erro configAltitudeMarStream: {e}')
            raise e

    def configAltitudeSoloStream(self):
        """Configura o Stream para capturar a altitude em relação ao solo"""
        try:
            if self.CurrentScenne != None and self.CurrentScenne.name == 'flight':
                if self.altitudeSoloStr == None:
                    self.altitudeSoloStr = self.conn.add_stream(
                        getattr, self.vessel.flight(), 'surface_altitude')
            else:
                self.altitudeSoloStr = None
        except Exception as e:
            print(f'Erro configAltitudeSoloStream: {e}')
            raise e

    def configAngulacaoStream(self):
        """Configura o Stream para capturar o angulo da nava"""
        try:
            if self.CurrentScenne != None and self.CurrentScenne.name == 'flight':
                if self.angulacaoStr == None:
                    self.angulacaoStr = self.conn.add_stream(
                        getattr, self.vessel.flight(), 'pitch')
            else:
                self.angulacaoStr = None
        except Exception as e:
            print(f'Erro ao obter o angulo da nave: {e}')

    def getAltitudeMar(self):
        """Busca a altitude rel mar, atualiza dados local efetua callback se configurado """
        try:
            if self.altitudeMarStr != None:
                self.altitudeMar = self.altitudeMarStr()
                if self.altitudeMarCall != None:
                    self.altitudeMarCall(self.altitudeMar)
        except Exception as e:
            print(f'Erro ao ler altitude mar: {e}')

    def getAltitudeSolo(self):
        """Busca a altitude rel solo, atualiza dados local e efetua callback se configurado"""
        try:
            if self.altitudeSoloStr != None:
                self.altitudeSolo = self.altitudeSoloStr()
                if self.altitudeSoloCall != None:
                    self.altitudeSoloCall(self.altitudeSolo)
        except Exception as e:
            print(f'Erro ao ler altitude solo: {e}')

    def getApoastro(self):
        """Busca a altitude do apoastro"""
        try:
            if self.apoastroStr != None:
                self.apoastro = self.apoastroStr()
                if self.apoastroCall != None:
                    self.apoastroCall(self.apoastro)
        except Exception as e:
            print(f'Erro ao obter apoastro: {e}')

    def getPeriastro(self):
        """Busca a altitude do periastro"""
        try:
            if self.periastroStr != None:
                self.periastro = self.periastroStr()
                if self.periastroCall != None:
                    self.periastroCall(self.periastro)
        except Exception as e:
            print(f'Erro ao obter periastro: {e}')

    def getAngulacao(self):
        """Busca a angulacao"""
        try:
            if self.angulacaoStr != None:
                self.angulacao = self.angulacaoStr()
                if self.angulacaoCall != None:
                    self.angulacaoCall(self.angulacao)
        except Exception as e:
            print(f'Erro ao obter angulação da nave: {e}')

    def run(self):
        while(True):
            try:
                time.sleep(0.5)
                # Verica a conexao com o KSP
                self.checkCon()
                self.getCurrentScenne()
                self.configApoastroStream()
                self.configPeriastroStream()
                self.configAltitudeMarStream()
                self.configAltitudeSoloStream()
                self.configAngulacaoStream()
                self.getAltitudeMar()
                self.getAltitudeSolo()
                self.getApoastro()
                self.getPeriastro()
                self.getAngulacao()
            except ConnectionResetError:
                self.conn = None
                self.KSPConectado = False
                print('Desconectado do KSP...')
            except Exception as e:
                if (self.conn != None):
                    self.conn.close()
                self.conn = None
                self.KSPConectado = False
                print(e)
