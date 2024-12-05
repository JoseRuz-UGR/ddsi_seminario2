from flask import Flask, request, jsonify, render_template
import pyodbc

#DB Connection
def odbc_connection():
    with open('app/credentials.txt', 'r') as file:
        content = file.read()

    server = 'oracle0.ugr.es'
    port = '1521'
    service_name = 'practbd'
    username = content
    password = content

    connectionString = f'DRIVER={{Oracle in instantclient_23_6}};DBQ={server}:{port}/{service_name};UID={username};PWD={password}'
    conn = pyodbc.connect(connectionString)

    return conn

#Create app
app = Flask(__name__)

#Main Menu----------------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

#Create Tables----------------------------------------------------------------------------------------------------------
@app.route('/create_tables', methods=['POST'])
def create_tables():

    #Drop tables
    try:
        cursor.execute("DROP TABLE Detalle_Pedido")
        print("\nTabla 'Detalle_Pedido' eliminada.")
    except pyodbc.Error:
        print("La tabla 'Detalle_Pedido' no existe o no pudo ser eliminada.")

    try:
        cursor.execute("DROP TABLE Pedido")
        print("\nTabla 'Pedido' eliminada.")
    except pyodbc.Error:
        print("La tabla 'Pedido' no existe o no pudo ser eliminada.")

    try:
        cursor.execute("DROP TABLE Stock")
        print("\nTabla 'Stock' eliminada.")
    except pyodbc.Error:
        print("La tabla 'Stock' no existe o no pudo ser eliminada.")

    #Create tables
    crear_tabla_stock = """
    CREATE TABLE Stock (
        Cproducto NUMBER PRIMARY KEY,
        Cantidad NUMBER NOT NULL
    )
    """

    crear_tabla_pedido = """
    CREATE TABLE Pedido (
        Cpedido NUMBER PRIMARY KEY,
        Ccliente NUMBER NOT NULL,
        Fecha_pedido DATE NOT NULL
    )
    """

    crear_tabla_detalle_pedido = """
    CREATE TABLE Detalle_Pedido (
        Cpedido NUMBER,
        Cproducto NUMBER,
        Cantidad NUMBER NOT NULL,
        CONSTRAINT fk_pedido FOREIGN KEY (Cpedido) REFERENCES Pedido(Cpedido),
        CONSTRAINT fk_producto FOREIGN KEY (Cproducto) REFERENCES Stock(Cproducto)
    )
    """

    try:
        cursor.execute(crear_tabla_stock)
        print("\nTabla 'Stock' creada con éxito.")
    except pyodbc.Error as e:
        print("Error al crear la tabla 'Stock':", e)

    try:
        cursor.execute(crear_tabla_pedido)
        print("\nTabla 'Pedido' creada con éxito.")
    except pyodbc.Error as e:
        print("Error al crear la tabla 'Pedido':", e)

    try:
        cursor.execute(crear_tabla_detalle_pedido)
        print("\nTabla 'Detalle_Pedido' creada con éxito.")
    except pyodbc.Error as e:
        print("Error al crear la tabla 'Detalle_Pedido':", e)
    connection.commit()

    #Fill tables
    tuplas_a_rellenar = [
        (1, 10), (2, 20), (3, 30), (4, 40), (5, 50), (6, 60), (7, 70), (8, 80), (9, 90), (10, 100)
    ]

    for cproducto, cantidad in tuplas_a_rellenar:
        try:
            cursor.execute("INSERT INTO Stock (Cproducto, Cantidad) VALUES (:1, :2)", (cproducto, cantidad))
        except pyodbc.Error as e:
            print(f"Error al insertar producto {cproducto}: {e}")

    print("\nTabla 'Stock' ha sido rellenada 10 tuplas predefinidas.")

    return jsonify({"message": "¡Tablas creadas correctamente!"})

#Show Tables------------------------------------------------------------------------------------------------------------
@app.route('/table', methods=['GET'])
def show_tables():
    cursor.execute("SELECT Cproducto, Cantidad FROM Stock")
    data = cursor.fetchall()

    return render_template('table.html', columns=data)

#Add order--------------------------------------------------------------------------------------------------------------
@app.route('/add_order', methods=['GET'])
def add_order():
    return render_template('add_order.html')

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

#Main function
if __name__ == '__main__':
    #DB connection initialization
    connection=odbc_connection()
    cursor=connection.cursor()
    print("Conexión exitosa con BD")

    #App run
    app.run()

    cursor.close()
    connection.close()
    print("Conexión cerrada")
    print ("Saliendo del programa")
