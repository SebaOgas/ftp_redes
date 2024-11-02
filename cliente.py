"""
Implementar una aplicación cliente de FTP, con las siguientes características:
    Soportar los comandos más comunes de FTP.
    Se debe poder subir y bajar archivos desde un servidor de FTP.
"""
import ftplib
import sys
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()

if len(sys.argv) < 1:
    raise Exception("Ingrese la IP")

ip = sys.argv[1]
port = int(sys.argv[2])

if port is None:
    port = 21

with ftplib.FTP() as ftp:
    # conexión al servidor local
    ftp.connect(ip, port)
    
    # obtener mensaje de bienvenida
    print(ftp.getwelcome())

    # identificación
    user = input("Usuario: ")
    pw = input("Contraseña: ")
    ret_login = ""
    end = False

    try:
        ret_login = ftp.login(user, pw)
    except ftplib.error_perm as e:
        ret_login = e
        end = True
    
    print(ret_login)

    
    while not end:
        line = input("> ")
        words = line.split(" ")
        cmd = words[0].lower()
        try:
            match cmd:
                case "help":
                    print("Comandos: ")
                    print("ls: Listar contenidos del directorio actual")
                case "exit":
                    end = True
                case "clear":
                    cls()
                case "ls":
                    print(ftp.retrlines('LIST'))
                case "cd":
                    if len(words) != 2:
                        raise Exception("Debe ingresar la ruta del directorio")
                    ftp.cwd(words[1])
        except Exception as e:
            print(e)


            



    """ # crear directorio
    ftp.mkd(f'ejemplo_1')
    print('Creado directorio ejemplo_1\n')
    
    # cambiar de directorio
    ftp.cwd('/ejemplo_1/')
    print('Cambiar a directorio ejemplo_1\n')

    #subir un fichero de texto
    with open('test.txt', 'rb') as txt_file:
        ftp.storbinary('STOR prueba_up.txt', txt_file)

    # ver directorio
    print(ftp.retrlines('LIST'))

    # cambiar de directorio
    ftp.cwd('/')
    print('Cambiar a directorio raíz\n')

    # ver directorio
    print(ftp.retrlines('LIST'))
 """