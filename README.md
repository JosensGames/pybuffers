# python-buffers
Escribe en bytes al igual que uint8_t, uint16_t, bool, ... en C++; a través de python!

## Ejemplos:
Crear un búfer:
```python
buffer = Buffer()
buffer.put_u8(100)
buffer.put_string("Hola Mundo")
buffer.seek(0)
print(buffer.get_u8())
print(buffer.get_string())
```
Aquí creamos un búfer y luego, le agregamos un byte con el valor de 100, un string y luego imprimimos su contenido.

## Leer un archivo
```python
from io import open

with open("config.dat", 'br') as file:
    content = file.read()
    file.close()

buffer = Buffer(content)
print(buffer.get_u8())
print(buffer.get_u8())
print(buffer.get_u32())
```
En este ejemplo, cargamos un archivo en modo bytes-lectura, y luego lo movemos hacia el buffer, para posteriormente, imprimir sus valores.

# Ejemplo con Sockets
A continuación, crearemos un servidor con socket de python y enviaremos un búfer a un cliente.
```python
from socket import socket, AF_INET, SOCK_STREAM
from buffers import *

# Crear paquete
msg = Buffer()
msg.put_string("Player #1")
msg.put_u8(46) # Nivel
msg.put_u16(6500) # Vida
msg.put_u16(1200) # Mana

# Crear servidor
Server = socket(AF_INET, SOCK_STREAM)
Server.bind(("127.0.0.1", 7171))
Server.listen(4)

# Escuchar una conexión
client, address = Server.accept()

# Mandar el jugador
client.send(msg.get_content())

# Cerrar conexión
client.close()
Server.close()
```

Ahora, crearemos el cliente
```python
from socket import socket, AF_INET, SOCK_STREAM
from buffers import *


Connection = socket(AF_INET, SOCK_STREAM)
Connection.connect(("127.0.0.1", 7171))

msg = Buffer(Connection.recv(256))
print(msg.get_string()) # Nombre
print(msg.get_u8()) # Nivel
print(msg.get_u16()) # Vida
print(msg.get_u16()) # Mana

Connection.close()
```
Podremos ver que con el servidor, creamos la instancia socket, y mandamos un búfer ya listo, para posteriormente, leerlo con el cliente.
