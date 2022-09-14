from re import A
import psycopg2
import PyQt5
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow

conn = psycopg2.connect(user="postgres", password="171201", database="Trab_bd", host="localhost", port="5432")

cur = conn.cursor()

'''Classe da tela de login'''
'''Ira redirecionar para as telas do piloto, admin e escuderias'''
class TelaLogin(QMainWindow):
    '''iniciando a tela'''
    def __init__(self):
        super(TelaLogin, self).__init__()
        loadUi("Tela1.ui",self)
        self.LoginButton.clicked.connect(self.checkUsuario)

    '''funcao para ir para a tela de login'''
    '''eh usada quando o usuario erra o login ou a senha'''
    def goToLogin(self):
        telalogin = TelaLogin()
        widget.addWidget(telalogin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    '''funcao para ir para a tela de overview do admin'''
    def goToAdmin(self):
        telaadmin = TelaAdmin()
        widget.addWidget(telaadmin)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    '''funcao para ir para a tela de overview do piloto'''
    def gotToPiloto(self):
        telapiloto = TelaPiloto(self.Senha.text())
        widget.addWidget(telapiloto)
        widget.setCurrentIndex(widget.currentIndex()+1)

    '''funcao para ir para a tela de overview da escuderia'''
    def gotToEscuderia(self):
        telaescuderia= TelaEscuderia(self.Senha.text())
        widget.addWidget(telaescuderia)
        widget.setCurrentIndex(widget.currentIndex()+1)

    '''funcao para a checar o tipo de usuario'''
    def checkUsuario(self):
        if(self.NomeUsuario.text() == 'admin' and self.Senha.text() == 'admin'):
            self.goToAdmin()
        elif("_d" in self.NomeUsuario.text()):
            '''checa o login'''
            self.checkLogin(self.NomeUsuario.text())
            '''checa a senha'''
            self.checkSenha(self.Senha.text())
            '''caso a senha ou o login estejam errados ele limpa os campos e exibe a mensagem: Usuario ou senha inválidos'''
            '''caso contrario ele ira para a tela de overview do piloto'''
            if(self.checkLoginIndex == 0 or self.checkSenhaIndex == 0):
                self.NomeUsuario.setText(" ")
                self.Senha.setText(" ")
                self.UsuarioSenha.setText("Usuario ou senha inválidos")
            elif(self.checkLoginIndex == 1 and self.checkSenhaIndex == 1):
                self.gotToPiloto()
        elif("_c" in self.NomeUsuario.text()):
            '''checa o login'''
            self.checkLogin(self.NomeUsuario.text())
            '''checa a senha'''
            self.checkSenha(self.Senha.text())
            '''caso a senha ou o login estejam errados ele limpa os campos e exibe a mensagem: Usuario ou senha inválidos'''
            '''caso contrario ele ira para a tela de overview da escuderia'''
            if(self.checkLoginIndex == 0 or self.checkSenhaIndex == 0):
                self.NomeUsuario.setText(" ")
                self.Senha.setText(" ")
                self.UsuarioSenha.setText("Usuario ou senha inválidos")
            elif(self.checkLoginIndex == 1 and self.checkSenhaIndex == 1):
                self.gotToEscuderia()
            
    '''funcao que checa o login'''
    def checkLogin(self,login):
        '''busca na tabela Users'''
        cur.execute(f"SELECT login FROM Users WHERE login = '{login}'")
        '''caso for encontrado um resultado o index de login eh 1 e caso contrario 0'''
        if(cur.fetchone() == None):
            self.checkLoginIndex = 0
        else:
            self.checkLoginIndex = 1

    '''funcao que checa a senha'''
    def checkSenha(self,senha):
        '''busca na tabela Users'''
        cur.execute(f"SELECT password FROM Users WHERE password = MD5('{senha}')")
        '''caso for encontrado um resultado o index de login eh 1 e caso contrario 0'''
        if(cur.fetchone() == None):
            self.checkSenhaIndex = 0
        else:
            self.checkSenhaIndex = 1

'''classe da tela do admin'''
class TelaAdmin(QMainWindow):
    '''inicia a tela'''
    def __init__(self):
        super(TelaAdmin, self).__init__()
        loadUi("Tela2.ui",self)
        '''Muda a label da tela para Adim'''
        self.AdminOverview.setText("Admin")
        '''Faz a pesquisa no banco de dados para ver o numero de pilotos'''
        cur.execute("SELECT COUNT(driverid) total_motoristas FROM driver;")
        self.pilotos = cur.fetchone()[0]
        '''Muda o numero de pilotos na tela de acordo com a busca'''
        self.NumeroPilotos.setText(str(self.pilotos))

        '''Faz a pesquisa no banco de dados para ver o numero de escuderias'''
        cur.execute("SELECT COUNT(constructorid) total_escuderias FROM constructors;")
        self.escuderias = cur.fetchone()[0]
        '''Muda o numero de escuderias na tela de acordo com a busca'''
        self.NumeroEscuderias.setText(str(str(self.escuderias)))

        '''Faz a pesquisa no banco de dados para ver o numero de corridas'''
        cur.execute("SELECT COUNT(raceid) total_corridas FROM races;")
        self.corridas = cur.fetchone()[0]
        '''Muda o numero de corridas na tela de acordo com a busca'''
        self.NumeroCorridas.setText(str(self.corridas))

        '''Faz a pesquisa no banco de dados para ver o numero de temporadas'''
        cur.execute("SELECT COUNT(year) total_temporadas FROM seasons;")
        self.temporadas = cur.fetchone()[0]
        '''Muda o numero de pilotos na tela de acordo com a busca'''
        self.NumeroTemporadas.setText(str(self.temporadas))
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.CadastroEscuderia.clicked.connect(self.goToCadEscuderia)
        
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.CadastroPiloto.clicked.connect(self.goToCadPiloto)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio1.clicked.connect(self.goToRelatorio1)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio2.clicked.connect(self.goToRelatorio2)

    '''funcao que encaminha o usuario para a tela de cadastro de escuderia'''
    def goToCadEscuderia(self):
        telacadastroescuderia = TelaCadastroEscuderia()
        widget.addWidget(telacadastroescuderia)
        widget.setCurrentIndex(widget.currentIndex()+1)

    '''funcao que encaminha o usuario para a tela de cadastro de piloto'''
    def goToCadPiloto(self):
        telacadastropiloto = TelaCadastroPiloto()
        widget.addWidget(telacadastropiloto)
        widget.setCurrentIndex(widget.currentIndex()+1)

    '''funcao que encaminha o usuario para a tela do relatorio 1'''
    def goToRelatorio1(self):
        telarelatorio1 = TelaRelatorio1()
        widget.addWidget(telarelatorio1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    '''funcao que encaminha o usuario para a tela do relatorio 2'''
    def goToRelatorio2(self):
        telarelatorio2 = TelaRelatorio2()
        widget.addWidget(telarelatorio2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


'''classe da tela do piloto'''
class TelaPiloto(QMainWindow):
    '''inicia a tela do piloto'''
    def __init__(self,nome):
        super(TelaPiloto, self).__init__()
        loadUi("Tela3.ui",self)
        self.nome = nome
        '''chama funcao que procura na tabela driver o nome e sobrenome do piloto logado'''
        self.getName(nome)
        '''muda a label para o nome do piloto logado'''
        self.PilotoOverview.setText(self.nomeCompleto)
        '''chama a funcao para pegar o Id do piloto logado'''
        self.getId(self.nome)
        '''chama a funcao para pegar o numero de vitorias do piloto logado'''
        self.getVitorias()
        '''muda a label de acordo com o numero de vitorias do piloto'''
        self.NumeroVitorias.setText(self.numVitorias)
        '''chama a funcao para pegar o primeiro e o ultimo ano em que o pilto correu'''
        self.getAnos()
        '''mada a label de acordo com os anos'''
        self.PrimeiroAno.setText(self.primeiro)
        self.UltimoAno.setText(self.ultimo)
        
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio5.clicked.connect(self.goToRelatorio5)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio6.clicked.connect(self.goToRelatorio6)

    '''funcao para pegar o nome e sobrenome do piloto'''
    def getName(self,nome):
        '''busca na tabela driver'''
        cur.execute(f"SELECT forename,surname FROM driver WHERE driverref = '{nome}';")
        result = cur.fetchmany(2)
        for row in result:
            forename = row[0]
            surname = row[1]
        self.nomeCompleto = forename + ' ' + surname

    '''funcao para pegar o id do piloto'''
    def getId(self,nome):
        '''busca na tabela Users'''
        cur.execute(f"SELECT IdOriginal FROM Users INNER JOIN driver d ON (d.driverId = IdOriginal) WHERE d.driverref = '{nome}'")
        self.id = str(cur.fetchone()[0])

    '''funcao para pegar o numero de vitorias do piloto'''
    def getVitorias(self):
        '''utiliza a funcao criada para ver a quantidade de vitorias do piloto'''
        cur.execute("SELECT quantidade_vitorias_piloto("+ self.id +");")
        self.numVitorias = str(cur.fetchone()[0])

    '''funcao para pegar o primeiro e o ultimo ano corrido pelo piloto'''
    def getAnos(self):
        '''utiliza a funcao criada'''
        cur.execute(f"SELECT primeiro_ano, ultimo_ano FROM primeiro_e_ultimo_ano_piloto({self.id});")
        result = cur.fetchmany(2)
        for row in result:
            primeiro = str(row[0])
            ultimo = str(row[1])
        self.primeiro = primeiro
        self.ultimo = ultimo

    '''funcao que encaminha o usuario para a tela do relatorio 5'''
    def goToRelatorio5(self):
        telarelatorio5 = TelaRelatorio5(self.id, self.nomeCompleto, self.nome)
        widget.addWidget(telarelatorio5)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    '''funcao que encaminha o usuario para a tela do relatorio 6'''
    def goToRelatorio6(self):
        telarelatorio6 = TelaRelatorio6(self.id, self.nomeCompleto, self.nome)
        widget.addWidget(telarelatorio6)
        widget.setCurrentIndex(widget.currentIndex() + 1)


'''classe para a tela da escuderia'''
class TelaEscuderia(QMainWindow):
    '''inicia a tela da escuderia'''
    def __init__(self,nome):
        super(TelaEscuderia, self).__init__()
        loadUi("Tela4.ui",self)
        self.nome = nome
        '''chama funcao para pegar o nome da escuderia'''
        self.getName(nome)
        '''muda a label de acordo com o nome da escuderia'''
        self.EscuderiaOverview.setText(self.nome)
        '''chama funcao para pegar o id da escuderia'''
        self.getId()
        '''chama a funcao que pega o numero de vitorias'''
        self.getVitorias()
        '''muda a label de acordo com o numero de vitorias'''
        self.NumeroVitorias.setText(self.numVitorias)
        '''chama funcao que pega o primeiro e ultimo ano que a escuderia apresenta dados'''
        self.getAnos()
        '''muda a label de acordo com o primeiro e ultimo ano da escuderia'''
        self.PrimeiroAno.setText(self.primeiro)
        self.UltimoAno.setText(self.ultimo)
        '''chama a funcao para pega a quantidade de pilotos diferentes ja registrados pela escuderia'''
        self.getQuantidadeDePilotos()
        '''muda a label de acordo com a quantidade de pilotos'''
        self.QuantidadePilotos.setText(self.quantidade)
        
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.ConsultaBotao.clicked.connect(self.goToConsultaEscuderia)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio3.clicked.connect(self.goToRelatorio3)
        
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio4.clicked.connect(self.goToRelatorio4)

    '''funcao para pegar o nome da escuderia'''
    def getName(self,nome):
        cur.execute(f"SELECT name FROM constructors WHERE LOWER(name) LIKE LOWER('{nome}')")
        self.nome = str(cur.fetchone()[0])
    
    '''funcao para pegar o id do piloto'''
    def getId(self):
        '''busca na tabela Users'''
        cur.execute(f"SELECT IdOriginal FROM Users INNER JOIN constructors c ON (c.constructorId = IdOriginal) WHERE LOWER(c.name) LIKE LOWER('{self.nome}') AND tipo = 'Escuderia';")
        self.id = str(cur.fetchone()[0])

    '''funcao para pega o numero de vitorias'''
    def getVitorias(self):
        cur.execute(f"SELECT quantidade_vitorias_escuderia({self.id})")
        self.numVitorias = str(cur.fetchone()[0])
    
    '''funcao para pegar o primeiro e ultimo ano que a escuderia apresenta dados'''
    def getAnos(self):
        cur.execute(f"SELECT primeiro_ano, ultimo_ano FROM primeiro_e_ultimo_ano_escuderia({self.id})")
        result = cur.fetchmany(2)
        for row in result:
            primeiro = str(row[0])
            ultimo = str(row[1])
        self.primeiro = primeiro
        self.ultimo = ultimo
    
    '''funcao para pegar a quantidade de pilotos diferentes registrados pela escuderia'''
    def getQuantidadeDePilotos(self):
        cur.execute(f"SELECT quantidade_pilotos_diferentes_escuderia({self.id})")
        self.quantidade = str(cur.fetchone()[0])

    '''funcao que te manda para a tela de consulta por forename'''
    def goToConsultaEscuderia(self):
        telaconsultaescuderia = TelaConsultaEscuderia(self.id,self.nome)
        widget.addWidget(telaconsultaescuderia) 
        widget.setCurrentIndex(widget.currentIndex()+1)

    '''funcao que encaminha o usuario para a tela do relatorio 3'''
    def goToRelatorio3(self):
        telarelatorio3 = TelaRelatorio3(self.id,self.nome)
        widget.addWidget(telarelatorio3)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    '''funcao que encaminha o usuario para a tela do relatorio 4'''
    def goToRelatorio4(self):
        telarelatorio4 = TelaRelatorio4(self.id,self.nome)
        widget.addWidget(telarelatorio4)
        widget.setCurrentIndex(widget.currentIndex() + 1)

'''classe da tela de cadastro da escuderia'''
class TelaCadastroEscuderia(QMainWindow):
    '''iniciando a tela'''
    def __init__(self):
        super(TelaCadastroEscuderia, self).__init__()
        loadUi("Tela5.ui",self)
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.CadastroBotao.clicked.connect(self.defineVar)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.AdminOverview.clicked.connect(self.goToAdminOverview)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.CadastroPiloto.clicked.connect(self.goToCadastroPiloto)
    
    '''define as variaveis de acordo com o input do usuario'''
    def defineVar(self):
        self.constructorId = self.ConstructorId.text()
        self.constructorRef = self.ConstructorRef.text()
        self.nome = self.Nome.text()
        self.nacionalidade = self.Nacionalidade.text()
        self.url = self.URL.text()
        '''chama funcao para checar o id da escuderia'''
        self.checkConstructorId()
        '''caso o id fornecido seja valida ele cadastra no banco de dados'''
        if(self.checkConstructorIdIndex == 1):
            self.insertData()
            self.IdEscuderia.setText("Escuderia cadastrada")
        else:
            self.deleteInfo()
            self.IdEscuderia.setText("Id de Escuderia inválido")

    '''funcao que coloca as informacoes no banco de dados'''
    def insertData(self):
        cur.execute(f"INSERT INTO Constructors (constructorid, constructorref, name, nationality, url) VALUES ('{self.constructorId}','{self.constructorRef}', '{self.nome}', '{self.nacionalidade}', '{self.url}');")
        conn.commit()
        self.deleteInfo()

    '''funcao que checa se o id fornecido ja existe'''
    def checkConstructorId(self):
        '''busca para ver se um id ja existe no banco de dados'''
        cur.execute(f"SELECT constructorId FROM constructors WHERE constructorId = '{self.constructorId}'")
        '''caso nada for encontrado na busca o index é 1 e caso contrario 9'''
        if(cur.fetchone() == None):
            self.checkConstructorIdIndex = 1
        else:
            self.checkConstructorIdIndex = 0
    
    '''funcao para deletar os dados colocados na pagina'''
    def deleteInfo(self):
        self.ConstructorId.setText(" ")
        self.ConstructorRef.setText(" ")
        self.Nome.setText(" ")
        self.Nacionalidade.setText(" ")
        self.URL.setText(" ")
        
    '''funcao que te manda para a tela de overview do admin'''
    def goToAdminOverview(self):
        telaadmin = TelaAdmin()
        widget.addWidget(telaadmin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    '''funcao que te manda para a tela de cadastro do piloto do admin'''
    def goToCadastroPiloto(self):
        telacadastropiloto = TelaCadastroPiloto()
        widget.addWidget(telacadastropiloto)
        widget.setCurrentIndex(widget.currentIndex()+1)

'''classe da tela de cadastro do piloto'''
class TelaCadastroPiloto(QMainWindow):
    '''iniciando a tela do cadastro do piloto'''
    def __init__(self):
        super(TelaCadastroPiloto, self).__init__()
        loadUi("Tela6.ui",self)
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.CadastroBotao.clicked.connect(self.defineVar)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.AdminOverview.clicked.connect(self.goToAdminOverview)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.CadastroEscuderia.clicked.connect(self.goToCadastroEscuderia)

    '''define as variaveis de acordo com o input do usuario'''
    def defineVar(self):
        self.driverId = self.DriverId.text()
        self.driverRef = self.DriverRef.text()
        self.numero = self.Numero.text()
        self.codigo = self.Codigo.text()
        self.nacionalidade = self.Nacionalidade.text()
        self.nome = self.Nome.text()
        self.sobrenome = self.Sobrenome.text()
        '''a variavel tempVar foi usada para pegar a data fornecida pelo usuario'''
        tempVar = self.DataDeNascimento.date()
        '''a variavel temp foi usada para transformar a data no formato "2020-01-01"'''
        temp = str(tempVar.toPyDate())
        '''a variavel tempVar2 foi usada para substituir os - pelas / '''
        tempVar2 = temp.replace('-','/') 
        self.dataDeNascimento = tempVar2
        '''chama funcao que checa se o id piloto ja existe e seta um index'''
        self.checkDriverId()
        '''caso o index setado na funcao anterior seja 1 é chamada a funcao para inserir os dados no banco caso o index seja 0 ele nao eh cadastrado'''
        if(self.checkPilotoIndex == 1):
            self.insertData()
            self.CadastroPiloto.setText("Piloto cadastrado")
        else:
            self.deleteInfo()
            self.CadastroPiloto.setText("Piloto já cadastrado")
    
    '''inseri os dados no banco de dados'''
    def insertData(self):
        cur.execute(f"INSERT INTO Driver(driverid,driverref,number,code,forename,surname,dob,nationality) VALUES({self.driverId},'{self.driverRef}',{self.numero},'{self.codigo}','{self.nome}','{self.sobrenome}','{self.dataDeNascimento }','{self.nacionalidade}')")
        conn.commit()
        self.deleteInfo()

    '''checa se o id fornecido ja existe no banco de dados'''
    def checkDriverId(self):
        '''busca para ver se ja existe dado Id'''
        cur.execute(f"SELECT driverId FROM driver WHERE driverId = '{self.driverId}'")
        '''o index eh setado como 1 caso nao exista e 0 caso exista'''
        if(cur.fetchone() == None):
            self.checkPilotoIndex = 1
        else:
            self.checkPilotoIndex = 0
    
    '''deleta as informacoes na tela'''
    def deleteInfo(self):
        self.DriverId.setText(" ")
        self.DriverRef.setText(" ")
        self.Numero.setText(" ")
        self.Codigo.setText(" ")
        self.Nacionalidade.setText(" ")
        self.Nome.setText(" ")
        self.Sobrenome.setText(" ")

    '''funcao que te manda para a tela de overview do admin'''
    def goToAdminOverview(self):
        telaadmin = TelaAdmin()
        widget.addWidget(telaadmin)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    '''funcao que te manda para a tela de cadastro do escuderia do admin'''
    def goToCadastroEscuderia(self):
        telacadastroescuderia = TelaCadastroEscuderia()
        widget.addWidget(telacadastroescuderia)
        widget.setCurrentIndex(widget.currentIndex()+1)

'''clase da tela de consulta da escuderia'''
class TelaConsultaEscuderia(QMainWindow):
    '''iniciando a classe'''
    def __init__(self,id,nome):
        super(TelaConsultaEscuderia, self).__init__()
        loadUi("Tela7.ui",self)
        self.id = int(id)
        self.nome = nome
        self.Escuderia.setText(self.nome)
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.BuscaPiloto.clicked.connect(self.busca)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.OverviewEscuderia.clicked.connect(self.goToEscuderiaOverview)

    '''funcao que colca as informacoes na tela'''
    def busca(self):
        self.nomePiloto = self.NomeInput.text()
        '''chama a funcao para checagem do nome do piloto e seta um index'''
        self.checkPiloto()
        if(self.idCheckIndex == 0):
            self.Nome.setText("Piloto nao encontrado")
            self.DataDeNascimento.setText(" ")
            self.Nacionalidade.setText(" ")
        elif(self.idCheckIndex == 1):
            self.Nome.setText(f"Nome: {self.nomeCompleto}")
            self.DataDeNascimento.setText(f"Data de Nascimento: {self.dataDeNascimento}")
            self.Nacionalidade.setText(f"Nacionalidade: {self.nacionalidade}")
    
    '''funcao que chaca se um piloto ja correu ou nao para a escuderia'''
    def checkPiloto(self):
        cur.execute(f"SELECT DISTINCT CONCAT(a.forename,' ', a.surname) nome_completo,a.dob data_nascimento,nationality nacionalidade FROM driver a INNER JOIN results b ON (b.driverid = a.driverid) WHERE b.constructorid = '{self.id}' AND a.forename = '{self.nomePiloto}';")
        result = cur.fetchmany(2)
        '''a variavel tempVar foi utilizada para verificar caso a funcao cur.fetchmany() resulte em [] que seria uma busca sem resultados'''
        tempVar = str(result)
        if(tempVar == '[]'):
            self.idCheckIndex = 0
        else:
            for row in result:
                self.nomeCompleto = str(row[0])
                self.dataDeNascimento = str(row[1])
                self.nacionalidade = str(row[2])
            self.idCheckIndex = 1
    
    '''funcao que te manda para a tela de overview da escuderia'''
    def goToEscuderiaOverview(self):
        telaescuderia = TelaEscuderia(self.nome)
        widget.addWidget(telaescuderia)
        widget.setCurrentIndex(widget.currentIndex()+1)

'''classe da tela do relatorio 1'''
class TelaRelatorio1(QMainWindow):
    '''iniciando a classe'''
    def __init__(self):
        super(TelaRelatorio1, self).__init__()
        loadUi("Tela8.ui", self)
        '''chama a funcao que pega o resultado da busca e os coloca na tela'''
        self.getStatus()
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.OverviewAdmin.clicked.connect(self.goToAdmin)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio2.clicked.connect(self.goToRelatorio2)

    '''funcao que pega o resultado da busca do relatorio 1'''
    def getStatus(self):
        cur.execute("SELECT a.status,COUNT(b.resultid) total_resultados FROM status a INNER JOIN results b ON (b.statusid = a.statusid) GROUP BY (a.status, a.statusid)ORDER BY a.statusid")
        result = cur.fetchmany(135)
        i = 0
        self.Tabela.setRowCount(135)
        for row in result:
            self.statusNome = str(row[0])
            self.numero = str(row[1])
            self.Tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(self.statusNome))
            self.Tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(self.numero))
            i = i+1

    '''funcao para ir para a tela de overview do admin'''
    def goToAdmin(self):
        telaadmin = TelaAdmin()
        widget.addWidget(telaadmin)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    '''funcao que encaminha o usuario para a tela do relatorio 2'''
    def goToRelatorio2(self):
        telarelatorio2 = TelaRelatorio2()
        widget.addWidget(telarelatorio2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

'''classe da tela do relatorio 2'''
class TelaRelatorio2(QMainWindow):
    '''iniciando a classe'''
    def __init__(self):
        super(TelaRelatorio2, self).__init__()
        loadUi("Tela9.ui", self)
        self.BuscaCidade.clicked.connect(self.procuraCidade)
        self.OverviewAdmin.clicked.connect(self.goToAdmin)
        self.Relatorio1.clicked.connect(self.goToRelatorio1)

    '''funcao que pega o resultado da busca do relatorio 2 e coloca os resultados numa tabela na tela'''
    def procuraCidade(self):
        self.cidade = self.NomeCidade.text()
        cur.execute(f"SELECT b.name nome_cidade, a.name nome_aeroporto, a.iatacode codigo_iata_aeroporto,a.city cidade_aeroporto,a.type tipo_aeroporto,earth_distance(ll_to_earth(a.latdeg, a.longdeg), ll_to_earth(b.lat, b.long)) distancia FROM (SELECT name, iatacode, city, latdeg, longdeg, type, isocountry FROM airports) a, (SELECT name, lat, long FROM geocities15k) b WHERE earth_distance(ll_to_earth(a.latdeg, a.longdeg), ll_to_earth(b.lat, b.long)) <= 100000 AND a.type IN ('medium_airport', 'large_airport') AND a.isocountry = 'BR' AND b.name = '{self.cidade}';")
        result = cur.fetchmany(200)
        self.Tabela.setRowCount(len(result))
        i = 0
        '''pega os resultados, coloca eles numa variavel e utiliza elas para colocar as informacoes na tabela'''
        for row in result:
            self.nomeCidade = str(row[0])
            self.codigo = str(row[1])
            self.nomeAeroporto = str(row[2])
            self.cidadeAeroporto = str(row[3])
            self.tipo = str(row[4])
            self.distancia = str(row[5])
            self.Tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(self.nomeCidade))
            self.Tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(self.codigo))
            self.Tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(self.nomeAeroporto))
            self.Tabela.setItem(i, 3, QtWidgets.QTableWidgetItem(self.cidadeAeroporto))
            self.Tabela.setItem(i, 4, QtWidgets.QTableWidgetItem(self.tipo))
            self.Tabela.setItem(i, 5, QtWidgets.QTableWidgetItem(self.distancia))
            i = i + 1

    '''funcao para ir para a tela de overview do admin'''
    def goToAdmin(self):
        telaadmin = TelaAdmin()
        widget.addWidget(telaadmin)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    '''funcao que encaminha o usuario para a tela do relatorio 1'''
    def goToRelatorio1(self):
        telarelatorio1 = TelaRelatorio1()
        widget.addWidget(telarelatorio1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

'''classe da tela do relatorio 3'''
class TelaRelatorio3(QMainWindow):
    '''iniciando a classe'''
    def __init__(self,id,nome):
        super(TelaRelatorio3, self).__init__()
        loadUi("Tela10.ui", self)
        self.id = id
        self.nome = nome
        self.Escuderia.setText(self.nome)
        '''chama a funcao para colocar os resultados na tela'''
        self.showData()
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.EscuderiaOverview.clicked.connect(self.goToEscuderia)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio4.clicked.connect(self.goToRelatorio4)

    '''funcao que pega o resultado da busca do relatorio 3 e os coloca em uma tabela na tela'''
    def showData(self):
        cur.execute(f"SELECT nome_completo, total_vitorias FROM listagem_pilotos_escuderia({self.id})")
        result = cur.fetchmany(800)
        i = 0
        self.Tabela.setRowCount(len(result))
        for row in result:
            self.nomePiloto = str(row[0])
            self.totalVitorias = str(row[1])
            self.Tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(self.nomePiloto))
            self.Tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(self.totalVitorias))
            i = i + 1


    '''funcao para ir para a tela de overview da escuderia'''
    def goToEscuderia(self):
        telaescuderia = TelaEscuderia(self.nome)
        widget.addWidget(telaescuderia)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    '''funcao que encaminha o usuario para a tela do relatorio 4'''
    def goToRelatorio4(self):
        telarelatorio4 = TelaRelatorio4(self.id,self.nome)
        widget.addWidget(telarelatorio4)
        widget.setCurrentIndex(widget.currentIndex() + 1)

'''classe da tela do relatorio 4'''
class TelaRelatorio4(QMainWindow):
    '''iniciando a classe'''
    def __init__(self,id,nome):
        super(TelaRelatorio4, self).__init__()
        loadUi("Tela11.ui", self)
        self.id = id
        self.nome = nome
        self.Escuderia.setText(self.nome)
        '''chama a funcao para colocar os resultados na tela'''
        self.showData()
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.EscuderiaOverview.clicked.connect(self.goToEscuderia)
        
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio3.clicked.connect(self.goToRelatorio3)

    '''funcao que pega o resultado da busca do relatorio 4 e os coloca em uma tabela na tela'''
    def showData(self):
        cur.execute(f"SELECT status, quantidade_resultados FROM quantidade_resultados_status_escuderia({self.id});")
        result = cur.fetchmany(135)
        i = 0
        self.Tabela.setRowCount(len(result))
        for row in result:
            self.statusNome = str(row[0])
            self.numero = str(row[1])
            self.Tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(self.statusNome))
            self.Tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(self.numero))
            i = i + 1

    '''funcao para ir para a tela de overview da escuderia'''
    def goToEscuderia(self):
        telaescuderia = TelaEscuderia(self.nome)
        widget.addWidget(telaescuderia)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    '''funcao que encaminha o usuario para a tela do relatorio 3'''
    def goToRelatorio3(self):
        telarelatorio3 = TelaRelatorio3(self.id,self.nome)
        widget.addWidget(telarelatorio3)
        widget.setCurrentIndex(widget.currentIndex() + 1)

'''classe da tela do relatorio 5'''
class TelaRelatorio5(QMainWindow):
    '''iniciando a classe'''
    def __init__(self,id,nomeCompleto, nome):
        super(TelaRelatorio5, self).__init__()
        loadUi("Tela12.ui", self)
        self.id = id
        self.nomeCompleto = nomeCompleto
        self.nome = nome
        self.Piloto.setText(self.nomeCompleto)
        '''chama a funcao para colocar os resultados na tela'''
        self.showData()
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.PilotoOverview.clicked.connect(self.goToPiloto)

        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio6.clicked.connect(self.goToRelatorio6)

    '''funcao que pega o resultado da busca do relatorio 5 e os coloca em um tabela na tela'''
    def showData(self):
        cur.execute(f"SELECT nome_corrida, ano_corrida, total_vitorias FROM quantidade_vitorias_rollup_piloto({self.id})")
        result = cur.fetchmany(500)
        i = 0
        self.Tabela.setRowCount(len(result))
        for row in result:
            self.nomeInput = str(row[0])
            self.anoCorrida = str(row[1])
            self.totalVitorias = str(row[2])
            self.Tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(self.nomeInput))
            self.Tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(self.anoCorrida))
            self.Tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(self.totalVitorias))
            i = i + 1

    '''funcao para ir para a tela de overview do piloto'''
    def goToPiloto(self):
        telapiloto = TelaPiloto(self.nome)
        widget.addWidget(telapiloto)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    '''funcao que encaminha o usuario para a tela do relatorio 6'''
    def goToRelatorio6(self):
        telarelatorio6 = TelaRelatorio6(self.id, self.nomeCompleto, self.nome)
        widget.addWidget(telarelatorio6)
        widget.setCurrentIndex(widget.currentIndex() + 1)

'''classe da tela do relatorio 6'''
class TelaRelatorio6(QMainWindow):
    '''iniciando a classe'''
    def __init__(self,id,nomeCompleto,nome):
        super(TelaRelatorio6, self).__init__()
        loadUi("Tela13.ui", self)
        self.id = id
        self.nomeCompleto = nomeCompleto
        self.nome = nome
        self.Piloto.setText(self.nomeCompleto)
        '''chama a funcao para colocar os resultados na tela'''
        self.showData()
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.PilotoOverview.clicked.connect(self.goToPiloto)
        '''detecta quando o usuario clica no botao e encaminha para a funcao'''
        self.Relatorio5.clicked.connect(self.goToRelatorio5)
    
    '''funcao que pega o resultado da busca do relatorio 6 e os coloca em um tabela na tela'''
    def showData(self):
        cur.execute(f"SELECT status, quantidade_resultados FROM quantidade_resultados_status_piloto({self.id})")
        result = cur.fetchmany(500)
        i = 0
        self.Tabela.setRowCount(len(result))
        for row in result:
            self.status = str(row[0])
            self.numerosStatus = str(row[1])
            self.Tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(self.status))
            self.Tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(self.numerosStatus))
            i = i + 1

    '''funcao para ir para a tela de overview do piloto'''
    def goToPiloto(self):
        telapiloto = TelaPiloto(self.nome)
        widget.addWidget(telapiloto)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    '''funcao que encaminha o usuario para a tela do relatorio 5'''
    def goToRelatorio5(self):
        telarelatorio5 = TelaRelatorio5(self.id, self.nomeCompleto, self.nome)
        widget.addWidget(telarelatorio5)
        widget.setCurrentIndex(widget.currentIndex() + 1)

'''iniciacao da tela de login'''
app = QApplication(sys.argv)
'''criacao do vetor de telas'''
widget = QtWidgets.QStackedWidget()
telalogin = TelaLogin()
widget.addWidget(telalogin)
'''setando as dimensoes da tela'''
widget.setFixedHeight(700)
widget.setFixedWidth(850)
widget.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")

cur.close()
print("Successfully connected!")

conn.close()