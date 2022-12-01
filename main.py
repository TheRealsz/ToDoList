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
        sqlName = "Select fullname from Usuarios where username = %s"
        dataName = Username
        cursor.execute(sqlName, (dataName,))
        
        fullname = cursor.fetchone()
        
        telaLogin.close()
        telaMain.show()
        telaMain.lFullname.setText(str(fullname[0]))

        sqlID = "Select ID from Usuarios where username = %s"
        dataID = Username
        cursor.execute(sqlID, (dataID,))
        global userID
        userID = cursor.fetchone()

        cursor.close()
        connection.close()
        listarItensUsuario()
    else:
        QtWidgets.QMessageBox.warning(telaLogin, 'ERRO!', "O usuario ou a senha nao existe!")

def abrirTelaCadastro():
    telaLogin.close()
    telaCadastro.show()

def abrirTelaAdd():
    telaMain.close()
    telaAdd.show()

def abrirTelaEdit():
    telaMain.close()
    telaEdit.show()

def abrirTelaEditStatus():
    telaMain.close()
    telaEditStatus.show()

def abrirTelaDelete():
    telaMain.close()
    telaDelete.show()

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

        QtWidgets.QMessageBox.about(telaCadastro, 'SUCESSO!', "Foi cadastrado o novo usuario de ID: " + str(userid))

        sqlName = "Select fullname from Usuarios where username = %s"
        dataName = cUsername
        cursor.execute(sqlName, (dataName,))

        fullname = cursor.fetchone()
        telaMain.lFullname.setText(str(fullname[0]))

        sqlID = "Select ID from Usuarios where username = %s"
        dataID = cUsername
        cursor.execute(sqlID, (dataID,))

        userID = cursor.fetchone()
        print(str(userID[0]))

        cursor.close()
        connection.close() 

        telaCadastro.close()
        telaMain.show()
        listarItensUsuario()

def listarItensUsuario():
    telaMain.lwFazer.clear()
    telaMain.lwFazendo.clear()
    telaMain.lwFeito.clear()
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()
    sqlTask = "Select * from Tasks where userID = %s"
    dataTask = str(userID[0])
    cursor.execute(sqlTask, (dataTask,))
    task = cursor.fetchall()
    inicio = 0
    while inicio < task.__len__():
        idTask = task[inicio][0]
        nameTask = task[inicio][1]
        descTask = task[inicio][2]
        dateTask = task[inicio][3]
        listTask = f"{idTask}. {nameTask} \n Descricao: {descTask} \n Data final: {dateTask} \n"
        statusTask = task [inicio][5]
        if statusTask == 1:
            telaMain.lwFazer.addItem(listTask)
        if statusTask == 2:
            telaMain.lwFazendo.addItem(listTask)
        if statusTask == 3:
            telaMain.lwFeito.addItem(listTask)
            
        inicio = inicio+1

def addTask():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()

    name = telaAdd.inputName.text()
    desc = telaAdd.inputDescricao.text()
    data_final = telaAdd.inputData.text()
    aFazer = telaAdd.rbFazer.isChecked()
    feito = telaAdd.rbFeito.isChecked()
    fazendo = telaAdd.rbFazendo.isChecked()

    if aFazer == False and feito == False and fazendo == False:
        QtWidgets.QMessageBox.warning(telaAdd, 'Atençao!', "Informe o Status de sua task para poder criar ela")

    if name == "" or data_final == "":
        QtWidgets.QMessageBox.warning(telaCadastro, 'Atençao!', "Informe os dados necessarios para criar a task!")
      
    else:
        if aFazer == True:
            sql = "INSERT INTO Tasks (nome, descricao, data_final, userID, statusID) VALUES (%s, %s, %s, %s, %s)"
            data = (name, desc, data_final, userID[0], 1)

            cursor.execute(sql, data) 
            connection.commit() 
            taskID = cursor.lastrowid

            QtWidgets.QMessageBox.about(telaCadastro, 'SUCESSO!', "Foi cadastrado a nova task de ID: " + str(taskID))

        if fazendo == True:
            sql = "INSERT INTO Tasks (nome, descricao, data_final, userID, statusID) VALUES (%s, %s, %s, %s, %s)"
            data = (name, desc, data_final, userID[0], 2)

            cursor.execute(sql, data) 
            connection.commit() 
            taskID = cursor.lastrowid

            QtWidgets.QMessageBox.about(telaCadastro, 'SUCESSO!', "Foi cadastrado a nova task de ID: " + str(taskID))

        if feito == True:
            sql = "INSERT INTO Tasks (nome, descricao, data_final, userID, statusID) VALUES (%s, %s, %s, %s, %s)"
            data = (name, desc, data_final, userID[0], 3)

            cursor.execute(sql, data) 
            connection.commit() 
            taskID = cursor.lastrowid

            QtWidgets.QMessageBox.about(telaCadastro, 'SUCESSO!', "Foi cadastrado a nova task de ID: " + str(taskID))     

        cursor.close() 
        connection.close()
        telaAdd.inputName.clear()
        telaAdd.inputDescricao.clear()
        telaAdd.inputData.clear()
        telaAdd.close()
        telaMain.show()
        listarItensUsuario()   

def deleteTask():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()
    idTask = telaDelete.inputID.text()
    
    if idTask == "":
        QtWidgets.QMessageBox.warning(telaDelete, 'Atençao!', "Informe os dados necessarios para deletar a task!")

    else:
        sql = "DELETE FROM Tasks WHERE ID = %s"
        data = idTask

        cursor.execute(sql, (data,)) 
        connection.commit()

        recordsaffected = cursor.rowcount

        QtWidgets.QMessageBox.about(telaDelete, "Sucesso!", f"{recordsaffected} registros excluídos")

    cursor.close()
    connection.close() 
    telaDelete.inputID.clear()
    telaDelete.close()
    telaMain.show()
    listarItensUsuario()

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
telaAdd = uic.loadUi('telaAdd.ui')
telaEdit = uic.loadUi('telaEdit.ui')
telaEditStatus = uic.loadUi('telaEditStatus.ui')
telaDelete = uic.loadUi('telaDelete.ui')
telaLogin.show()
telaLogin.btnLogin.clicked.connect(verUser)
telaLogin.btnTelaCadastro.clicked.connect(abrirTelaCadastro)
telaCadastro.btnCadastro.clicked.connect(cadastro)
telaCadastro.btnVoltarLogin.clicked.connect(voltarTelaLogin)
telaMain.btnTelaAdd.clicked.connect(abrirTelaAdd)
telaMain.btnTelaEdit.clicked.connect(abrirTelaEdit)
telaMain.btnTelaEditStatus.clicked.connect(abrirTelaEditStatus)
telaMain.btnTelaDelete.clicked.connect(abrirTelaDelete)
telaAdd.btnAdd.clicked.connect(addTask)
telaDelete.btnDelete.clicked.connect(deleteTask)
#tela.btnLimpar.clicked.connect(Limpar) #Vinculando a função Limpar ao botão btnLimpar
#tela.btnCadastrar.clicked.connect(insert_BD)
app.exec()





#tela_teste.btnLogar.clicked.connect(Login)

#QtWidgets.QMessageBox.about(TELA, 'TITLE', 'MESSAGE')