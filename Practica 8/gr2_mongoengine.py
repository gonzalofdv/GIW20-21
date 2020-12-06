"""

Jin Wang Xu, Fernando González Zamorano, Jorge Borja García y Gonzalo Figueroa del Val declaramos que esta solución es fruto exclusivamente
de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

"""


"""

SI EJECUTAMOS EL COMANDO PARA LANZAR TODOS LOS TESTS CONJUNTOS, NOS DA ERROR
EL TEST DE USUARIOS INVALIDOS, EN CAMBIO, SI LANZAMOS UNICAMENTE EL TEST
DE USUARIOS INVALIDOS, TODO FUNCIONA CORRECTAMENTE

"""

from mongoengine import PULL
from mongoengine import connect
from mongoengine import ValidationError
from mongoengine import IntField, FloatField, StringField
from mongoengine import ComplexDateTimeField, DateTimeField
from mongoengine import Document, DynamicDocument, EmbeddedDocument
from mongoengine import ListField, ReferenceField, EmbeddedDocumentField

connect('giw_mongoengine')

class Producto(Document):
	codigo_barras = StringField(primary_key=True, regex="^\d{13}$") #codigo de barras EAN-13 #añadirlo con regex?¿?¿¿?
	nombre = StringField(required=True, min_length=2) #mismo nombre que la linea
	categoria_principal = IntField(required=True, min_value=0)
	categorias_secundarias = ListField(IntField(min_value=0)) #Categoria principal en el primer lugar de la lista

	def clean(self):
		self.validate(clean=False)
		#FORMATO CODIGO DE BARRAS:
		# primeros digitos: Organización Nacional Sistema EAN, en España, Aecoc y código 84 
		# entre 5 y 8 digitos, Codigo de empresa que identifica al propietario de la marca
		# Código de producto: que completa los 12 primeros dígitos
		# Dígito de control: un solo dígito para verificar que el código leído es correcta
		# PARA CALCULARLO: se suman los dígitos de las posiciones impares, se multiplica por 3,
		# se le suman los dígitos de las posiciones pares y a este resultado se le resta el siguiente
		# múltiplo de 10. El resultado final debe coincidir con el dígito de control

		digitoControl = 0

		#Recorrer digitos de posiciones impares para sumarlos
		for i in range(1, 12, 2):
			digitoControl += int(self.codigo_barras[i])

		#Multiplicamos por 3
		digitoControl *= 3

		#Sumamos digitos de posiciones pares
		for i in range(0, 11, 2):
			digitoControl += int(self.codigo_barras[i])


		#Restamos siguiente múltiplo de 10 o lo que es lo mismo, hacer mod 10
		#digitoFinal = 10 - digitoControl % 10
		digitoFinal = (10 - (digitoControl % 10)) % 10

		if digitoFinal != int(self.codigo_barras[12]):
			raise ValidationError("El dígito de control no es correcto")

		#Solo haremos esta comprobación en caso de que existan categorias secundarias
		if len(self.categorias_secundarias) != 0:
			if self.categoria_principal != self.categorias_secundarias[0]:
				raise ValidationError("La categoria principal del producto no está la primera en la lista de categorías secundarias")


class Tarjeta(EmbeddedDocument):
	nombre = StringField(required=True, min_length=2)
	numero = StringField(required=True, regex="^\d{16}$")
	mes = StringField(required=True, regex = "^(0[1-9]|1[0-2])$")
	año = StringField(required=True, regex='^\d{2}$')
	ccv = StringField(required=True, regex='^\d{3}$')


class Linea(EmbeddedDocument):
	num_items = IntField(required=True, min_value=1)
	precio_item = FloatField(required=True, min_value=0.0)
	name = StringField(required=True, min_length=2) #mismo nombre que el producto
	total = FloatField(required=True, min_value=0.0) #cantidad por precio producto
	ref = ReferenceField(Producto, required=True)

	def clean(self):
		self.validate(clean=False)
		#Comprobamos que el nombre de la linea es el mismo que el nombre del producto
		if(self.name != self.ref.nombre):
			raise ValidationError("El nombre de la linea no se corresponde con el nombre del producto referenciado")
		#Queremos comprobar que el precio total se corresponde con la mult de cantidad y precio
		if round(self.num_items * self.precio_item, 2) != self.total: #Vamos a redondear siempre a 2 decimales ya que a veces las multiplicaciones
		#de int * float dan valores con más decimales, en el caso de la linea 2, al multiplicar 3 * 3.55, nos devuelve 10.6499999999 en vez de 10.65
		#Las operaciones siempre nos van a dar dos decimales, por lo que redondeamos a 2.
			raise ValidationError("El precio de la linea no se corresponde con el número de productos por su precio")

class Pedido(Document):
	total = FloatField(required=True, min_value=0) #Suma precios de sus lineas de pedido
	fecha = ComplexDateTimeField(required=True)
	lineas = ListField(EmbeddedDocumentField(Linea, required=True))

	def clean(self):
		self.validate(clean=False)
		#Queremos comprobar que el precio total es la suma de precios de la lista de lineas
		precio = 0
		correcto = True
		productos = []

		for lineaPedido in self.lineas:
			if lineaPedido.name not in productos: #Comprobamos si cada linea corresponde a un producto único (no hay varias lineas sobre un mismo producto)
				productos.append(lineaPedido.name)
				precio += lineaPedido.total
			else:
				correcto = False
				break

		if correcto == False:
			raise ValidationError("Hay varias lineas sobre el mismo producto")
		if round(precio,2) != self.total: #Volvemos a redondear por un fallo que nos da 30.9399999 en lugar de 30.94
			raise ValidationError("No se corresponde el precio del pedido con la suma de los totales de las lineas de pedidos")

class Usuario(Document):
	dni = StringField(primary_key=True, max_length = 9, regex = "^[0-9]{8}[A-Z]{1}$") #Formato de dni #añadirlo con regex
	nombre = StringField(required=True, min_length=2)
	apellido1 = StringField(required=True, min_length=2)
	apellido2 = StringField()
	f_nac = DateTimeField(required=True, separator="-")
	tarjetas = ListField(EmbeddedDocumentField(Tarjeta))
	pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=PULL))

	def clean(self):
		self.validate(clean=False)

		letrasDNI = "TRWAGMYFPDXBNJZSQVHLCKE"
		#COGEMOS LOS 8 DIGITOS
		digitos = int(self.dni[:8])
		#DIVIDIR ENTRE 23 Y COGEMOS EL RESTO
		resto = digitos % 23
		#COMPARAR RESTO CON ÍNDICE DE LA LETRA QUE HEMOS OBTENIDO DEL DNI INTRODUCIDO
		#SI COINCIDEN: CORRECTO, SI NO: INCORRECTO
		if (self.dni[8] != letrasDNI[resto]):
			raise ValidationError("Letra del DNI incorrecta")



def inserta():

	#2 usuarios, cada uno con al menos 2 tarjetas
	#Cada usuario al menos 2 pedidos con más de una linea cada uno

	producto = Producto(codigo_barras="8480000917072", nombre="Mascarillas quirurgicas",	categoria_principal=0, categorias_secundarias=[0, 4])
	producto.save()
	producto = Producto(codigo_barras="8480000770936", nombre="Gel hidroalcoholico",	categoria_principal=0, categorias_secundarias=[0, 4])
	producto.save()
	producto = Producto(codigo_barras="8410261160108", nombre="Zumo naranja",	categoria_principal=1)
	producto.save()
	producto = Producto(codigo_barras="5713448955980", nombre="Calcetines negros",	categoria_principal=2, categorias_secundarias=[2, 9, 3])
	producto.save()
	producto = Producto(codigo_barras="7312040097708", nombre="Vodka blanco",	categoria_principal=1, categorias_secundarias=[1, 7])
	producto.save()

	linea1 = Linea(
		num_items = 7,
		precio_item = 0.50,
		name = "Mascarillas quirurgicas",
		total = 3.50,
		ref = Producto.objects.get(nombre="Mascarillas quirurgicas")
	)

	linea2 = Linea(
		num_items = 3,
		precio_item = 3.55,
		name = "Gel hidroalcoholico",
		total = 10.65,
		ref = Producto.objects.get(nombre="Gel hidroalcoholico")
	)

	linea3 = Linea(
		num_items = 14,
		precio_item = 0.97,
		name = "Zumo naranja",
		total = 13.58,
		ref = Producto.objects.get(nombre="Zumo naranja")
	)

	linea4 = Linea(
		num_items = 2,
		precio_item = 6.93,
		name = "Calcetines negros",
		total = 13.86,
		ref = Producto.objects.get(nombre="Calcetines negros")
	)

	linea5 = Linea(
		num_items = 1,
		precio_item = 39.95,
		name = "Vodka blanco",
		total = 39.95,
		ref = Producto.objects.get(nombre="Vodka blanco")
	)

	pedido1 = Pedido(
		total=14.15,
		fecha="2020,03,01,14,10,43,123456",
		lineas=[linea1, linea2]
	)
	pedido1.save()

	pedido2 = Pedido(
		total=53.81,
		fecha="2020,03,01,14,10,43,123456",
		lineas=[linea4, linea5]
	)
	pedido2.save()

	pedido3 = Pedido(
		total=81.54,
		fecha="2020,03,01,14,10,43,123456",
		lineas=[linea1, linea2, linea3, linea4, linea5]
	)
	pedido3.save()

	pedido4 = Pedido(
		total=30.94,
		fecha="2020,03,01,14,10,43,123456",
		lineas=[linea3, linea4, linea1]
	)	
	pedido4.save()

	tarjeta1 = Tarjeta(nombre = "Gonzalo", numero = "1234567812345678", mes = "11", año = "21", ccv = "852")

	tarjeta2 = Tarjeta(nombre = "Gonzalo", numero = "8765432187654321", mes = "11", año = "21", ccv = "258")

	tarjeta3 = Tarjeta(nombre = "Fernando", numero = "1122334455667788", mes = "06", año = "21", ccv = "117")

	tarjeta4 = Tarjeta(nombre = "Fernando", numero = "8877665544332211", mes = "01", año = "22", ccv = "765")

	usuario = Usuario(
		dni="50489867Z",
		nombre="Gonzalo",
		apellido1="Figueroa",
		apellido2="del Val",
		f_nac="1998, 3, 1",
		tarjetas=[tarjeta1, tarjeta2],
		pedidos=[pedido2, pedido4]
	)
	usuario.save()

	usuario = Usuario(
		dni="52103478Z",
		nombre="Fernando",
		apellido1="Gonzalez",
		apellido2="Zamorano",
		f_nac="1999, 1, 13",
		tarjetas=[tarjeta3, tarjeta4],
		pedidos=[pedido1, pedido3]
	)
	usuario.save()


inserta()