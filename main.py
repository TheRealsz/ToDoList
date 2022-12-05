from PyQt5 import uic, QtWidgets    
from PyQt5.QtCore import *
import sys
import os 
os.system("pip install mysql-connector-python")
import mysql.connector
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

password = os.getenv("passwordBD")
bd = os.getenv("bdName")

def conectarBD(host, usuario, senha, DB):
    connection = mysql.connector.connect( 
        host = host, 
        user= usuario, 
        password=senha, 
        database=DB 
    ) 

    return connection

def verUser():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor() 
    
    Username = telaLogin.inputUsername.text()
    Password = telaLogin.inputPassword.text()
    
    sql = "Select username, senha from Usuarios where username = %s and senha = %s"
    data = (Username, Password)
    cursor.execute(sql, data) 
    
    result = cursor.fetchone() 
    
    if result:
        telaLogin.close()
        telaMain.show()
 
        sqlID = "Select ID from Usuarios where username = %s"
        dataID = Username
        cursor.execute(sqlID, (dataID,))
        global userID
        userID = cursor.fetchone()

        cursor.close()
        connection.close()
        telaLogin.inputUsername.clear()
        telaLogin.inputPassword.clear()
        listarItensUsuario()
        updateUserinfo()
    else:
        QtWidgets.QMessageBox.warning(telaLogin, 'ERRO!', "O usuario ou a senha nao existe!")

def updateUserinfo():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()
    sqlExist = f"Select * from Usuarios where ID = {userID[0]}"
    cursor.execute(sqlExist) 

    result = cursor.fetchone() 

    fullname = result[3]
    fullnameLen = fullname.__len__()
    telaMain.lFullname.setFixedWidth(fullnameLen * 24)
    telaMain.lFullname.setText(str(fullname) + " ")

def funLogout():
    telaConta.close()
    telaLogin.show()

def abrirTelaCadastro():
    telaLogin.close()
    telaCadastro.show()

def abrirTelaAdd():
    telaMain.close()
    telaAdd.show()

def abrirTelaInfoID():
    telaMain.close()
    telaInfoID.show()

def abrirTelaEditStatus():
    telaMain.close()
    telaEditStatus.show()

def abrirTelaManConta():
    telaMain.close()
    telaConta.show()

def abrirTelaDelete():
    telaMain.close()
    telaDelete.show()

def abrirTelaEditCont():
    telaConta.close()
    telaEditCont.show()

def abrirTelaDelConta():
    telaConta.close()
    telaDeleteCont.show()

def voltarTelaLogin():
    telaCadastro.close()
    telaLogin.show()

def volTelaMainAdd():  
    telaAdd.close()
    telaMain.show()
    listarItensUsuario()

def volTelaMainDel():
    telaDelete.close()
    telaMain.show()
    listarItensUsuario()

def volTelaMainES():
    telaEditStatus.close()
    telaMain.show()
    listarItensUsuario()
 
def volTelaMainIID():
    telaInfoID.close()
    telaMain.show()
    listarItensUsuario()

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
        return
    
    if result:
        QtWidgets.QMessageBox.warning(telaCadastro, 'Atençao!', "O username ou o nome completo do usuario ja existe!")
    
    else:
        sql = "INSERT INTO Usuarios (username, senha, fullname) VALUES (%s, %s, %s)"
        data = (cUsername, cPassword, cFullname)

        cursor.execute(sql, data) 
        connection.commit() 
        userid = cursor.lastrowid

        QtWidgets.QMessageBox.about(telaCadastro, 'SUCESSO!', "Foi cadastrado o novo usuario de ID: " + str(userid))

        sqlID = "Select ID from Usuarios where username = %s"
        dataID = cUsername
        cursor.execute(sqlID, (dataID,))
        global userID
        userID = cursor.fetchone()
  

        cursor.close()
        connection.close() 
        telaCadastro.inputCFullname.clear()
        telaCadastro.inputCUsername.clear()
        telaCadastro.inputCPassword.text()
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
        return

    if name == "" or data_final == "":
        QtWidgets.QMessageBox.warning(telaAdd, 'Atençao!', "Informe os dados necessarios para criar a task!")
      
    else:
        if aFazer == True:
            sql = "INSERT INTO Tasks (nome, descricao, data_final, userID, statusID) VALUES (%s, %s, %s, %s, %s)"
            data = (name, desc, data_final, userID[0], 1)

            cursor.execute(sql, data) 
            connection.commit() 
            taskID = cursor.lastrowid

            QtWidgets.QMessageBox.about(telaAdd, 'SUCESSO!', "Foi cadastrado a nova task de ID: " + str(taskID))

        if fazendo == True:
            sql = "INSERT INTO Tasks (nome, descricao, data_final, userID, statusID) VALUES (%s, %s, %s, %s, %s)"
            data = (name, desc, data_final, userID[0], 2)

            cursor.execute(sql, data) 
            connection.commit() 
            taskID = cursor.lastrowid

            QtWidgets.QMessageBox.about(telaAdd, 'SUCESSO!', "Foi cadastrado a nova task de ID: " + str(taskID))

        if feito == True:
            sql = "INSERT INTO Tasks (nome, descricao, data_final, userID, statusID) VALUES (%s, %s, %s, %s, %s)"
            data = (name, desc, data_final, userID[0], 3)

            cursor.execute(sql, data) 
            connection.commit() 
            taskID = cursor.lastrowid

            QtWidgets.QMessageBox.about(telaAdd, 'SUCESSO!', "Foi cadastrado a nova task de ID: " + str(taskID))     

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

def editStatusTask():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()

    Id = telaEditStatus.inputID.text()
    aFazer = telaEditStatus.rbFazer.isChecked()
    feito = telaEditStatus.rbFeito.isChecked()
    fazendo = telaEditStatus.rbFazendo.isChecked()

    if aFazer == False and feito == False and fazendo == False:
        QtWidgets.QMessageBox.warning(telaEditStatus, 'Atençao!', "Informe o Status de sua task para poder editar ela")
        return

    if Id == "":
        QtWidgets.QMessageBox.warning(telaEditStatus, 'Atençao!', "Informe o ID para editar o status da task!")
      
    else:
        if aFazer == True:
            sql = "UPDATE Tasks SET statusID = %s WHERE ID = %s"
            data = (1, Id)

            cursor.execute(sql, data) 
            connection.commit() 


        if fazendo == True:
            sql = "UPDATE Tasks SET statusID = %s WHERE ID = %s"
            data = (2, Id)

            cursor.execute(sql, data) 
            connection.commit() 


        if feito == True:
            sql = "UPDATE Tasks SET statusID = %s WHERE ID = %s"
            data = (3, Id)

            cursor.execute(sql, data) 
            connection.commit() 

        QtWidgets.QMessageBox.about(telaEditStatus, 'SUCESSO!', f"O status da task de ID {Id} foi atualizado!")
        cursor.close() 
        connection.close()
        telaEditStatus.inputID.clear()
        telaEditStatus.close()
        telaMain.show()
        listarItensUsuario()   

def getIdEdit():
    global IdTaskEdit
    IdTaskEdit = telaInfoID.inputID.text()

    if IdTaskEdit == "":
        QtWidgets.QMessageBox.warning(telaInfoID, 'Atençao!', "Informe o ID da task para poder edita-la!")

    else:
        telaInfoID.close()
        telaEdit.show()

def editTask():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()

    name = telaEdit.inputName.text()
    desc = telaEdit.inputDescricao.text()
    data_final = telaEdit.inputData.text()

    if name == "" or data_final == "":
        QtWidgets.QMessageBox.warning(telaEdit, 'Atençao!', "Informe os dados necessarios para editar o status da task!")
      
    else:
        sql = "UPDATE Tasks SET nome = %s, descricao = %s, data_final = %s WHERE ID = %s"
        data = (name, desc, data_final, IdTaskEdit)

        cursor.execute(sql, data) 
        connection.commit() 

        QtWidgets.QMessageBox.about(telaEditStatus, 'SUCESSO!', f"O a task de ID {IdTaskEdit} foi atualizada!")
        cursor.close() 
        connection.close()
        telaEdit.inputName.clear()
        telaEdit.inputDescricao.clear()
        telaEdit.inputData.clear()
        telaEdit.close()
        telaMain.show()
        listarItensUsuario()   

def volTelaIID():
    telaEdit.close()
    telaInfoID.show()

def volTelaMainC():
    telaConta.close()
    telaMain.show()
    listarItensUsuario()

def voltTelaContaEC():
    telaEditCont.close()
    telaConta.show()

def editCont():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()
    global ecFullName
    global ecUsername
    global ecPassword
    ecFullName = telaEditCont.inputName.text()
    ecUsername = telaEditCont.inputUsername.text()
    ecPassword = telaEditCont.inputPassword.text()

    sqlExist = "Select username, fullname from Usuarios where (username = %s or fullname = %s) and ID <> %s"
    dataExist = (ecUsername, ecFullName, userID[0])
    cursor.execute(sqlExist, dataExist) 
    print (ecFullName, ecUsername)
    result = cursor.fetchone()
    print(result) 

    
    if ecFullName == "":
        sqlName = f"select fullname from Usuarios where ID = {userID[0]} "

        cursor.execute(sqlName) 
        ecFullName = cursor.fetchone()
        ecFullName = ecFullName[0]
        
    if ecUsername == "":
        sqlUser = f"select username from Usuarios where ID = {userID[0]} "

        cursor.execute(sqlUser) 
        ecUsername = cursor.fetchone()
        ecUsername = ecUsername[0]
    
    if ecPassword == "":
        sqlPassword = f"select senha from Usuarios where ID = {userID[0]} "

        cursor.execute(sqlPassword) 
        ecPassword = cursor.fetchone()
        ecPassword = ecPassword[0]
    
    if result:
        QtWidgets.QMessageBox.warning(telaEditCont, 'Atençao!', "O username ou o nome completo do usuario ja existe!")
        return

    sql = "UPDATE Usuarios SET fullname = %s, username = %s, senha = %s WHERE ID = %s"
    data = (ecFullName, ecUsername, ecPassword, userID[0])

    cursor.execute(sql, data) 
    connection.commit() 

    QtWidgets.QMessageBox.about(telaEditCont, 'SUCESSO!', f"A sua conta foi atualizada!")   

    cursor.close()
    connection.close()
    telaEditCont.inputName.clear()
    telaEditCont.inputUsername.clear()
    telaEditCont.inputPassword.clear()
    updateUserinfo()
    telaEditCont.close()
    telaMain.show() 
    listarItensUsuario()

def voltTelaContDC():
    telaDeleteCont.close()
    telaConta.show()

def deleteCont():
    connection = conectarBD("localhost","root", password, bd) 
    cursor = connection.cursor()
    sql = f"DELETE FROM Tasks WHERE userID = {userID[0]}"
    cursor.execute(sql) 
    connection.commit()

    sql = f"DELETE FROM Usuarios WHERE ID = {userID[0]}"
    cursor.execute(sql) 
    connection.commit()
    QtWidgets.QMessageBox.about(telaDeleteCont, 'SUCESSO!', f"A sua conta foi excluida!") 
    cursor.close()
    connection.close() 
    telaDeleteCont.close()
    telaLogin.show()

app = QtWidgets.QApplication(sys.argv)
telaLogin = uic.loadUi('telaLogin.ui')
telaMain = uic.loadUi('telaMain.ui')
telaCadastro = uic.loadUi('telaCadastro.ui')
telaAdd = uic.loadUi('telaAdd.ui')
telaEdit = uic.loadUi('telaEdit.ui')
telaEditStatus = uic.loadUi('telaEditStatus.ui')
telaDelete = uic.loadUi('telaDelete.ui')
telaInfoID = uic.loadUi('telaInfoID.ui')
telaConta = uic.loadUi('telaConta.ui')
telaEditCont = uic.loadUi('telaEditCont.ui')
telaDeleteCont = uic.loadUi('telaDeleteCont.ui')
telaLogin.show()
telaLogin.btnLogin.clicked.connect(verUser)
telaLogin.btnTelaCadastro.clicked.connect(abrirTelaCadastro)
telaCadastro.btnCadastro.clicked.connect(cadastro)
telaCadastro.btnVoltarLogin.clicked.connect(voltarTelaLogin)
telaMain.btnTelaAdd.clicked.connect(abrirTelaAdd)
telaMain.btnTelaEdit.clicked.connect(abrirTelaInfoID)
telaMain.btnTelaEditStatus.clicked.connect(abrirTelaEditStatus)
telaMain.btnTelaDelete.clicked.connect(abrirTelaDelete)
telaMain.btnConta.clicked.connect(abrirTelaManConta)
telaAdd.btnAdd.clicked.connect(addTask)
telaAdd.btnVoltarTelaMainAdd.clicked.connect(volTelaMainAdd)
telaDelete.btnDelete.clicked.connect(deleteTask)
telaDelete.btnVoltarTelaMainD.clicked.connect(volTelaMainDel)
telaEditStatus.btnEditStatus.clicked.connect(editStatusTask)
telaEditStatus.btnVoltarTelaMainES.clicked.connect(volTelaMainES)
telaInfoID.btnNextTelaEdit.clicked.connect(getIdEdit)
telaInfoID.btnVoltarTelaMainIID.clicked.connect(volTelaMainIID)
telaEdit.btnEdit.clicked.connect(editTask)
telaEdit.btnVoltarTelaIIDE.clicked.connect(volTelaIID)
telaConta.btnVoltaTelaMainC.clicked.connect(volTelaMainC)
telaConta.btnTelaEditConta.clicked.connect(abrirTelaEditCont)
telaConta.btnTelaDelConta.clicked.connect(abrirTelaDelConta)
telaConta.btnLogout.clicked.connect(funLogout)
telaEditCont.btnVoltaTelaContEC.clicked.connect(voltTelaContaEC)
telaEditCont.btnEdit.clicked.connect(editCont)
telaDeleteCont.btnVoltTelaContaDC.clicked.connect(voltTelaContDC)
telaDeleteCont.btnDeleteCont.clicked.connect(deleteCont)
app.exec()
