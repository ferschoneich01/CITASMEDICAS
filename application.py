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
@app.route('/especialidades')
def Especialidades():        
    return render_template('especialidades.html')

#ruta medicos
@app.route('/horarios', methods=["GET"])
def Horarios(): 
    if request.method == "GET":
        try:
            cursor=conexion.cursor()
            cursor.execute("select * from xdb.horario")
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
            query = "insert into xdb.medicos values((SELECT count(*)+1 FROM xdb.medicos),'"+nombre+"','"+apellido+"','"+dni+"','"+direccion+"','"+correo+"','"+telefono+"','"+sexo+"','"+numcol+"',TO_DATE('"+fechanac+"','YYYY/MM/DD'),1)"
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

            query = "insert into xdb.horario values((SELECT count(*)+1 FROM xdb.horario),"+medico+",TO_DATE('"+fechaAt+"','YYYY/MM/DD'),'TO_DATE('"+fechaAt+"','YYYY/MM/DD') "+horaInicio+":00',TO_DATE('"+fechaAt+"','YYYY/MM/DD') "+horaFin+":00)"
            cursor.execute(query)
            
        except Exception as err:
            print(err)
            return redirect('/horarios')
        else:
            print('datos insertados')
            conexion.commit()
            cursor.close()
            return redirect('/horario')

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
    
        
if __name__ == '__main__':
    app.run(port = 5000, Debug = True)