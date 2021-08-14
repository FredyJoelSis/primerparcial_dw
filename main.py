import urllib
import os

import sqlalchemy
from pydantic import BaseModel
import databases
from databases import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from sqlalchemy.sql.sqltypes import Integer

DATABASE_URL ="postgres://ttcaoeqqllfegc:6a6ce83beff944fd12d8a8512e5b74c2ab3e7b6810718e4106939dbe6232298c@ec2-3-217-68-126.compute-1.amazonaws.com:5432/dcedsrjffik858"


 

host_server = os.environ.get('host_server','localhost')
db_server_port= urllib.parse.quote_plus(str(os.environ.get('db_server_port','5432')))
database_name= os.environ.get('database_name','fastapi')
db_username= urllib.parse.quote_plus(str(os.environ.get('db_username','postgres')))
db_password= urllib.parse.quote_plus(str(os.environ.get('db_password','123456')))
ssl_mode= urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))

#DATABASE_URL= 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server,db_server_port, database_name, ssl_mode)
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


empleado = sqlalchemy.Table(
    'empleado',
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("nombre",sqlalchemy.String),
    sqlalchemy.Column("apellido",sqlalchemy.String),
    sqlalchemy.Column("direccion",sqlalchemy.String),
    sqlalchemy.Column("telefono",sqlalchemy.String),
    sqlalchemy.Column("salario",sqlalchemy.String),
    sqlalchemy.Column("porcentaje_comision_ventas",sqlalchemy.String),
    sqlalchemy.Column("edad",sqlalchemy.String),
    sqlalchemy.Column("telefono",sqlalchemy.String),
    sqlalchemy.Column("status",sqlalchemy.Boolean),

)

cliente = sqlalchemy.Table(
    'cliente',
    metadata,
    sqlalchemy.Column("RUT",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("nombre",sqlalchemy.String),
    sqlalchemy.Column("apellido",sqlalchemy.String),
    sqlalchemy.Column("direccion",sqlalchemy.String),
    sqlalchemy.Column("telefono",sqlalchemy.String),
    sqlalchemy.Column("correo",sqlalchemy.String),
    sqlalchemy.Column("status",sqlalchemy.Boolean),
)

producto = sqlalchemy.Table(
    'producto',
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("nombre",sqlalchemy.String),
    sqlalchemy.Column("precio_actual",sqlalchemy.Integer),
    sqlalchemy.Column("stock",sqlalchemy.Integer),
    sqlalchemy.Column("nombre_proveedor",sqlalchemy.String),
    sqlalchemy.Column("porcentaje_ventas",sqlalchemy.Integer),
    
)

proveedor = sqlalchemy.Table(
    'proveedor',
    metadata,
    sqlalchemy.Column("RUT",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("nombre",sqlalchemy.String),
    sqlalchemy.Column("direccion",sqlalchemy.String),
    sqlalchemy.Column("telefono",sqlalchemy.Integer),
    sqlalchemy.Column("nomenclatura_direccion",sqlalchemy.String),
    
    
)



engine = sqlalchemy.create_engine(
    DATABASE_URL,pool_size=3, max_overflow=0
)
metadata.create_all(engine)



class EmpleadoIn(BaseModel):
    nombre:str
    apellido:str
    status: bool
    direccion:str
    telefono:str
    salario:str
    porcentaje_comision_ventas:str
    edad:str
    telefono:str

class Empleado(BaseModel):
    id: int
    nombre:str
    apellido:str
    status: bool
    direccion:str
    telefono:str
    salario:str
    porcentaje_comision_ventas:str
    edad:str
    telefono:str




app = FastAPI(title="FAST API UMG ")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database = databases.Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnet()

@app.post("/empleados/",response_model=Empleado)
async def create_empleado(emp:EmpleadoIn):
    query= empleado.insert().values(nombre=emp.nombre, apellido=emp.apellido, status=emp.status, direccion=emp.direccion, telefono=emp.telefono, salario=emp.salario, porcentaje_comision_ventas=emp.porcentaje_comision_ventas, edad=emp.edad, telefono=emp.telefono)
    
    last_record_id =await database.execute(query)
    return {**emp.dict(), "id":last_record_id}


@app.get("/getEmpleado/",response_model=List[Empleado] )
async def getEmpleado(skip: int=0, take: int=20):
    query= empleado.select().offset(skip).limit(take)
    return await database.fetch_all(query)



@app.get("/getEmpleado/{empleado_id}",response_model=Empleado)
async def getEmpleadoId(emp_id: int ):
    query= empleado.select().where(empleado.c.id==emp_id  )
    return await database.fetch_one(query)

@app.delete("/empleadoDelete/{empleado_id}/")
async def del_empleado(emp_id: int):
    query = empleado.delete().where(empleado.c.id==emp_id)
    await database.execute(query)
    return {"message":" Empleado with id:{} deleted succesfully!".format(emp_id)}

@app.put("/empleadoUpdate/{emp_id}",response_model=Empleado)
async def setEmpleadoId(emp_id: int,emp:EmpleadoIn):
    query = empleado.update().where(empleado.c.id==emp_id).values(nombre=emp.nombre, apellido=emp.apellido,status=emp.status, direccion=emp.direccion, telefono=emp.telefono, salario=emp.salario, porcentaje_comision_ventas=emp.porcentaje_comision_ventas, edad=emp.edad, telefono=emp.telefono)
    await database.execute(query)
    return {**emp.dict(),"id":emp_id}






