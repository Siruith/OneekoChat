from flask import *
from flask_socketio import *
from time import localtime, strftime

app = Flask(__name__)
app.debug = True
app.config.update(SECRET_KEY = '0508', USERNAME='Siruit', PASSWORD='0508')
nya = SocketIO(app)
namespace = "/Physx"



@nya.on("connected", namespace=namespace)
def connection():
	print("Usuario conectado.")
@nya.on("disconnected", namespace=namespace)
def disconnection():
	print("Usuario desconectado.")
@nya.on("notification", namespace=namespace)
def notification(message):
    print("Ha llegado un nuevo mensaje {!r}".format(message))
    nya.emit("notification", message, namespace=namespace)

Users = ['a']
Nicks = ['b']
Passwords = ['c']
ActualUser = str()
FriendsListRn = []
Time = strftime("%H, %M", localtime())


@app.route('/', methods=['GET', 'POST'])
def login():
	 
	#Esta funcion recoge los datos introducidos para el inicio de sesión y procede a la aplicacion si el usuario se encuentra registrado.
	 
	global Nicks, Users, Passwords
	if request.method == 'POST':
		li = request.form['Login']
		p = request.form['Password']
		session['Usuario'] = li
		ActualUser = str(li)
		if li not in Nicks or p not in Passwords:
			return render_template('denied.html')
		elif Nicks.index(li) == Passwords.index(p):
			return render_template('login.html')
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
			Users.append(u)
			Nicks.append(n)
			Passwords.append(p1)
			return render_template('log2.html')
		else:
			return render_template('registerfailed.html')
	return render_template('register.html')
@app.route('/AddF', methods=['POST', 'GET'])
def addf():

	#Esta funcion añade a los demas usuarios a la lista de contactos del usuario.

	if request.method == 'POST' :
		f = str(request.form['Add'])
		if f in Users and f != ActualUser :
			if f in FriendsListRn :
				return render_template('alreadyfriends.html')
			elif f not in FriendsListRn :
				FriendsListRn.append(f)
		elif f not in Users :
			return render_template('doesnotexist.html')

	return render_template('addf.html')


@app.route('/2Login', methods=['POST', 'GET'])
def log():
	 
	#Esta funcion lleva al usuario de nuevo a la pantalla de inicio de sesión en caso de que decida no crear una cuenta.
	 
	return render_template('log2.html')

@app.route('/2AddF', methods=['POST', 'GET'])
def goaddf():

	#Esta funcion se encarga de llevar al usuario a la pagina para añadir contactos a su lista.

	global Users, Passwords
	return render_template('addf.html')
@app.route('/2Dashboard', methods=['POST', 'GET'])
def dashboard():

	#Esta funcion lleva al usuario a su pantalla de inicio donde se mostrarán los chats.

	global Users
	return render_template('login.html')
@app.route('/About', methods=['POST', 'GET'])
def abouta():

	#Esta funcion lleva al usuario a la pagina de informacion de la aplicacion.

	return render_template('about.html')
@app.route('/Settings', methods=['POST', 'GET'])
def settings():

	#Esta funcion lleva al usuario a la pagina de configuracion.

	if request.method == 'POST' :
		if request.form['Set Password'] == request.form['Confirm Password'] :
			np = str(request.form['Set Password'])
			Passwords.pop(Users.index(ActualUser))
			Passwords.insert(Users.index(ActualUser, request.form['Set Password']))
	return render_template('settings.html')
@app.route('/Chatroom', methods=['Post', 'Get'])
def chat():

	#Esta funcion lleva al usuario a la sala del chat que seleccíono.

	if request.method == 'POST' :
		Message = request.form['Escriba aquí']
		print(Message)

	return render_template('chat.html')
if __name__ == "__main__":
	nya.run(app)