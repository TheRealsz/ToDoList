CREATE DATABASE ToDoList;
USE ToDoList;

Create table Usuarios(
	ID int primary key auto_increment,
    username varchar(100) not null unique,
    senha varchar (100) not null,
    fullname varchar (150) not null
);

Create Table Statuses(
	ID int primary key unique auto_increment,
    descricao varchar(80) not null
);

Create Table Tasks(
	ID int primary key unique auto_increment,
    nome varchar(80) not null,
	descricao varchar(300),
    data_final date,
	userID int,
    statusID int,
    
    foreign key (userID) references Usuarios(ID),
    foreign key (statusID) references Statuses(ID)
);


INSERT INTO Statuses values (null, 'Nao feito');
INSERT INTO Statuses values (null, 'Fazendo');
INSERT INTO Statuses values (null, 'Feito');
