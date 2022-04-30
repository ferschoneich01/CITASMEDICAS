from pydoc import describe
from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle

#database conexion
try:
    conexion=cx_Oracle.connect(
        user='XDB',
        password='123456',
        dsn='localhost:1521/xe',
        encoding='UTF-8'

    )
except Exception as ex:
    print(ex)



app = Flask(__name__)

#ruta principal
@app.route('/')
def Index():   
    return render_template('index.html')

#ruta para crear cita medica
@app.route('/crear-cita')
def CrearCita():
    return render_template('citas.html')

#ruta medicos
@app.route('/medicos', methods=["GET"])
def Medicos():    
    if request.method == "GET":
        try:
            cursor=conexion.cursor()
            cursor.execute("select * from xdb.medicos")
            rows=cursor.fetchall()
            for row in rows:
                print(row) 
        except Exception as err:
            print(err)
            return redirect('/medicos')
        else:
            cursor.close()    
        return render_template('medicos.html',medicos=rows)

#ruta especialidades
@app.route('/especialidades', methods=["GET"])
def Especialidades():   
    if request.method == "GET":
        try:
            cursor=conexion.cursor()
            #cursor.execute("select id_medico_especialidad,m.nombre,e.nombre from xdb.medico_especialidad me inner join xdb.medicos m on me.id_medico = m.id_medico INNER JOIN xdb.especialidades e on e.id_especialidad = me.id_especialidad")
            #Mespecialidades=cursor.fetchall()
            cursor.execute("select * from xdb.medicos") 
            medicos=cursor.fetchall()
            cursor.execute("select * from xdb.especialidades") 
            especialidades=cursor.fetchall()
        except Exception as err:
            print(err)
            return redirect('/especialidades')
        else:
            cursor.close()     
    return render_template('especialidades.html',medicos=medicos, especialidades=especialidades)

#ruta medicos
@app.route('/horarios', methods=["GET"])
def Horarios(): 
    if request.method == "GET":
        try:
            cursor=conexion.cursor()
            cursor.execute("select id_horario,m.nombre,fechaatencio,inicioatencion,finatencion from xdb.horario h inner join xdb.medicos m on m.id_medico = h.medico")
            horarios=cursor.fetchall()
            cursor.execute("select * from xdb.medicos") 
            medicos=cursor.fetchall()
        except Exception as err:
            print(err)
            return redirect('/horarios')
        else:
            cursor.close()    
               
        return render_template('horarios.html',horarios=horarios,medicos=medicos)

#ruta añadir medico
@app.route('/addMedico',methods=["POST","GET"])
def addMedico():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        dni = request.form["dni"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        numcol = request.form["numcolegiatura"]
        sexo = request.form["sexo"]
        fechanac = request.form["fechanac"]
        
        try:      
            cursor=conexion.cursor()
            query = "insert into xdb.medicos values(NULL,'"+nombre+"','"+apellido+"','"+dni+"','"+direccion+"','"+correo+"','"+telefono+"','"+sexo+"','"+numcol+"',TO_DATE('"+fechanac+"','YYYY/MM/DD'),1)"
            cursor.execute(query)
            
        except Exception as err:
            print(err)
            return redirect('/medicos')
        else:
            print('datos insertados')
            conexion.commit()
            cursor.close()
            return redirect('/medicos')

@app.route('/addHorario',methods=["POST","GET"])
def addHorario():
    if request.method == "POST":
        medico = request.form["medico"]
        fechaAt = request.form["fechaAtencion"]
        horaInicio = request.form["inicioAtencion"]
        horaFin= request.form["finAtencion"]
        print(horaFin)
        try:      
            cursor=conexion.cursor()
            query = "insert into xdb.horario values(NULL,"+medico+",TO_DATE('"+fechaAt+"','YYYY/MM/DD'),TO_TIMESTAMP('"+horaInicio+":00', 'HH24:MI:SS'),TO_TIMESTAMP('"+horaFin+":00', 'HH24:MI:SS'))"
            cursor.execute(query)
            
        except Exception as err:
            print(err)
            return redirect('/horarios')
        else:
            print('datos insertados')
            conexion.commit()
            cursor.close()
            return redirect('/horarios')

@app.route('/addMEspecialidad',methods=["POST","GET"])
def addMEspecialidad():
    if request.method == "POST":
        medico = request.form["medico"]
        especialidad = request.form["especialidad"]
        
        try:      
            cursor=conexion.cursor()
            query = "insert into xdb.medico_especialidad values(NULL,"+medico+","+especialidad+")"
            cursor.execute(query)
            
        except Exception as err:
            print(err)
            return redirect('/especialidades')
        else:
            print('datos insertados')
            conexion.commit()
            cursor.close()
            return redirect('/especialidades')

@app.route('/addEspecialidad',methods=["POST","GET"])
def addEspecialidad():
    if request.method == "POST":
        nombre = request.form["Nombre"]
        descripcion= request.form["Descripcion"]
        
        try:      
            cursor=conexion.cursor()
            query = "insert into xdb.especialidades values(NULL,'"+nombre+"','"+descripcion+"')"
            cursor.execute(query)
            
        except Exception as err:
            print(err)
            return redirect('/especialidades')
        else:
            print('datos insertados')
            conexion.commit()
            cursor.close()
            return redirect('/especialidades')
            
@app.route('/deleteEspecialidad/<string:id>', methods=["GET","POST"])
def deleteEspecialidad(id):        
        try:  
            cursor=conexion.cursor()   
            cursor.execute('delete from especialidades where id_especialidad = {0}'.format(id))
            print('eliminando...')
        except Exception as err:
            print(err)
            return redirect('/especialidades')
        else:

            print('especialidad eliminada')
            conexion.commit()
            cursor.close()
            return redirect('/especialidades')

@app.route('/deleteMedico/<string:id>', methods=["GET","POST"])
def deleteMedico(id):        
        try:  
            cursor=conexion.cursor()   
            cursor.execute('delete from medicos where id_medico = {0}'.format(id))
            print('eliminando...')
        except Exception as err:
            print(err)
            return redirect('/medicos')
        else:

            print('medico eliminado')
            conexion.commit()
            cursor.close()
            return redirect('/medicos')

@app.route('/deleteHorario/<string:id>', methods=["GET","POST"])
def delete(id):        
        try:  
            cursor=conexion.cursor()   
            cursor.execute('delete from horario where id_horario = {0}'.format(id))
            print('eliminando...')
        except Exception as err:
            print(err)
            return redirect('/horarios')
        else:

            print('horario eliminado')
            conexion.commit()
            cursor.close()
            return redirect('/horarios')
    
        
if __name__ == '__main__':
    app.run(port = 5000, Debug = True)