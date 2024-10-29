USE IDS_API;

create table alumnos
(
    nombre   varchar(50) not null,
    apellido varchar(50) not null,
    padron   int         not null
        primary key
);

create table materias
(
    codigo       int         not null,
    departamento int         not null,
    nombre       varchar(50) null,
    primary key (codigo, departamento)
);

create table notas
(
    padron       int  not null,
    departamento int  not null,
    codigo       int  not null,
    nota         int  not null,
    fecha        date not null,
    constraint departamento
        foreign key (codigo, departamento) references materias (codigo, departamento),
    constraint padron
        foreign key (padron) references alumnos (padron)
);

