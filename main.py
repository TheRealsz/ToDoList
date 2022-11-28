from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import *
import sys
import os 
os.system("pip install mysql-connector-python")
import mysql.connector
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

#####Comando abaixo só é necessário executar uma única vez
#Faz a instalação do conector MySQL

password = os.getenv("passwordBD")
bd = os.getenv("bdName")

def conectarBD(host, usuario, senha, DB):
    connection = mysql.connector.connect( #Informando os dados para conexão com o BD
        host = host, #ip do servidor do BD
        user= usuario, #Usuário do MySQL 
        password=senha, #Senha do usuário do MySQL
        database=DB  #nome do DB criado
    ) #Define o banco de dados usado

    return connection

def verUser():
    connection = conectarBD("localhost","root", password, bd) #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco
    Username = telaLogin.inputUsername.text()
    Password = telaLogin.inputPassword.text()
    sql = "Select username, senha from Usuarios where username = %s and senha = %s"
    data = (Username, Password)

    cursor.execute(sql, data) 
    result = cursor.fetchone() 
    
    if result:
        telaLogin.close()
        telaMain.show()
    else:
        QtWidgets.QMessageBox.warning(telaLogin, 'ERRO!', "O usuario ou a senha nao existe!")

def abrirTelaCadastro():
    telaLogin.close()
    telaCadastro.show()

def voltarTelaLogin():
    telaCadastro.close()
    telaLogin.show()
    
def cadastro():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()
    cFullname = telaCadastro.inputCFullname.text()
    cUsername = telaCadastro.inputCUsername.text()
    cPassword = telaCadastro.inputCPassword.text()
    sqlExist = "Select username, fullname from Usuarios where username = %s or fullname = %s"
    dataExist = (cUsername, cFullname)

    cursor.execute(sqlExist, dataExist) 
    result = cursor.fetchone() 
    
    if cFullname == "" or cUsername == "" or cPassword == "":
        QtWidgets.QMessageBox.warning(telaCadastro, 'Atençao!', "Informe os dados necessarios para fazer o cadastro!")
    
    elif result:
        QtWidgets.QMessageBox.warning(telaCadastro, 'Atençao!', "O username ou o nome completo do usuario ja existe!")
    
    else:
        sql = "INSERT INTO Usuarios (username, senha, fullname) VALUES (%s, %s, %s)"
        data = (cUsername, cPassword, cFullname)

        cursor.execute(sql, data) 
        connection.commit() 
        userid = cursor.lastrowid

        cursor.close()
        connection.close() 
        QtWidgets.QMessageBox.about(telaCadastro, 'SUCESSO!', "Foi cadastrado o novo usuario de ID: " + str(userid))

        telaCadastro.close()
        telaMain.show()

# def insert_BD():
#     connection = conectarBD("localhost","root","aulasDB_2022","projeto") #Recebe a conexão estabelecida com o banco
#     cursor = connection.cursor() #Cursor para comunicação com o banco
#     Nome = tela.txtNome.text()
#     CPF = tela.txtCPF.text()
#     endereco = tela.txtEndereco.text() + " " + tela.txtNumero.text()

#     sql = "INSERT INTO Cliente (nome, cpf, endereco) VALUES (%s, %s, %s)"
#     data = (
#     Nome,
#     CPF,
#     endereco
#     )

#     cursor.execute(sql, data) #Executa o comando SQL
#     connection.commit() #Efetua as modificações

#     userid = cursor.lastrowid #Obtém o último ID cadastrado

#     cursor.close() #Fecha o cursor
#     connection.close() #Fecha a conexão com o BD

#     QtWidgets.QMessageBox.about(tela, 'SUCESSO!', "Foi cadastrado o novo cliente de ID: " + str(userid))

# def Limpar(): #Função usada para limpar o texto das caixas de texto
#     tela.txtNome.setText("")
#     tela.txtCPF.setText("")
#     tela.txtEndereco.setText("")
#     tela.txtNumero.setText("")
#     tela.dateEdit.setDate(QDate(2020, 6, 10))

# def AbrirTelaCadastro():
#     tela.show()
#     telaMenu.close()

# def AbrirTelaConsulta():
#     telaConsulta.show()
#     telaMenu.close()

app = QtWidgets.QApplication(sys.argv)
telaLogin = uic.loadUi('telaLogin.ui')
telaMain = uic.loadUi('telaMain.ui')
telaCadastro = uic.loadUi('telaCadastro.ui')
telaLogin.show()
telaLogin.btnLogin.clicked.connect(verUser)
telaLogin.btnTelaCadastro.clicked.connect(abrirTelaCadastro)
telaCadastro.btnCadastro.clicked.connect(cadastro)
telaCadastro.btnVoltarLogin.clicked.connect(voltarTelaLogin)
#tela.btnLimpar.clicked.connect(Limpar) #Vinculando a função Limpar ao botão btnLimpar
#tela.btnCadastrar.clicked.connect(insert_BD)
app.exec()




#tela_teste.btnLogar.clicked.connect(Login)

#QtWidgets.QMessageBox.about(TELA, 'TITLE', 'MESSAGE')