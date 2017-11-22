from flask import *
from flask_socketio import *

app = Flask(__name__)
app.debug = True
app.config.update(SECRET_KEY = '0508', USERNAME='Siruit', PASSWORD='0508')
io = SocketIO(app)
namespace = "/Physx"



@io.on("connected", namespace=namespace)
def connection():
	print("Usuario conectado.")
@io.on("disconnected", namespace=namespace)
def disconnection():
	print("Usuario desconectado.")
@io.on("notification", namespace=namespace)
def notification(message):
    print("Ha llegado un nuevo mensaje {!r}".format(message))
    io.emit("notification", message, namespace=namespace)

Users = ['a']
Nicks = ['b']
Passwords = ['c']
UserCount = 0
ActualUser = str()


@app.route('/', methods=['GET', 'POST'])
def login():
	 
	#Esta funcion recoge los datos introducidos para el inicio de sesión y procede a la aplicacion si el usuario se encuentra registrado.
	 
	global Nicks, Users, Passwords
	if request.method == 'POST':
		li = request.form['Login']
		p = request.form['Password']
		if li not in Nicks or p not in Passwords:
			return render_template('denied.html')
		elif Nicks.index(li) == Passwords[Nicks.index(li)]:
			ActualUser = str(li)
			return render_template('alreadychosen.html')
		else:
			return render_template('denied.html')
	return render_template('log2.html')

@app.route('/SignUp', methods=['POST', 'GET'])
def register():
	 
	#Esta funcion lleva al usuario a la pantalla de registro donde va a introducir sus datos para los siguientes inicios de sesión.
	 
	return render_template('register.html')


@app.route('/AddU', methods=['POST', 'GET'])
def addu():
	 
	#Esta funcion agrega los datos de inicio de sesión a una lista de datos y luego lo envía a la pantalla de inicio de sesión.
	 
	global Nicks, Users, Passwords, UserCount
	if request.method == 'POST':
		u = str(request.form['Full Name'])
		n = str(request.form['User Name'])
		p1 = str(request.form['Set Password'])
		p2 = str(request.form['Confirm Password'])
		if n in Nicks:
			return render_template('alreadychosen.html')
		elif p1 == p2:
			UserCount += 1
			Users.append(u)
			Nicks.append(n)
			Passwords.append(p1)
			return render_template('log2.html')
		else:
			return render_template('registerfailed.html')
	return render_template('register.html')

@app.route('/2Login', methods=['POST', 'GET'])
def log():
	 
	#Esta funcion lleva al usuario de nuevo a la pantalla de inicio de sesión en caso de que decida no crear una cuenta.
	 
	return render_template('log2.html')

@app.route('/2AddF', methods=['POST', 'GET'])
def addf():

	#Esta funcion se encarga de llevar al usuario a la pagina para añadir contactos a su lista.

	global Users, Passwords, UserCount
	return render_template('addf.html')

if __name__ == "__main__":
    io.run(app)