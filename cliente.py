"""
Implementar una aplicación cliente de FTP, con las siguientes características:
    Soportar los comandos más comunes de FTP.
    Se debe poder subir y bajar archivos desde un servidor de FTP.
"""
import ftplib
import string
import sys
import os
import random
from getpass import getpass

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()

if len(sys.argv) < 2:
    print("Error: Ingrese la IP")
    exit()

ip = sys.argv[1]
port = 21

if len(sys.argv) >= 3:
    port = int(sys.argv[2])

with ftplib.FTP() as ftp:
    # conexión al servidor local
    ftp.connect(ip, port)
    print("Conectado usando IP: "+ip+" y puerto: "+str(port))
    
    # obtener mensaje de bienvenida
    print(ftp.getwelcome())

    # identificación
    user = input("Usuario: ")
    pw = getpass("Contraseña: ")
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
                    print("exit: Cerrar conexión al servidor")
                    print("cls|clear: Limpiar consola")
                    print("ls: Listar contenidos del directorio remoto actual")
                    print("lls: Listar contenidos del directorio local actual")
                    print("cd <nombre_dir>: Cambiar directorio remoto actual")
                    print("lcd <nombre_dir>: Cambiar directorio local actual")
                    print("mkdir <nombre_dir>: Crear directorio remoto")
                    print("rmdir <nombre_dir>: Borrar directorio remoto")
                    print("get|pull <nombre_archivo_remoto> [nombre_archivo_local]: Obtener archivo remoto")
                    print("put|push <nombre_archivo_local> [nombre_archivo_remoto]: Subir archivo local")
                    print("rm|delete <nombre_archivo>: Borrar archivo remoto")
                case "exit":
                    end = True
                case "clear"|"cls":
                    cls()

                #Comandos remotos
                case "ls":
                    print(ftp.retrlines('LIST'))
                case "cd":
                    if len(words) != 2:
                        raise Exception("Debe ingresar la ruta del directorio")
                    print(ftp.cwd(words[1]))
                case "mkdir":
                    if len(words) != 2:
                        raise Exception("Debe ingresar el nombre del directorio a crear")
                    print(ftp.mkd(words[1]))
                case "rmdir":
                    if len(words) != 2:
                        raise Exception("Debe ingresar el nombre del directorio a borrar")
                    print(ftp.rmd(words[1]))
                case "get"|"pull":
                    if len(words) < 2:
                        raise Exception("Debe ingresar el nombre del archivo a obtener")
                    if len(words) > 3:
                        raise Exception("Arg esperados: <archivo_a_obtener> [nombre_de_archivo_local]")
                    tmpstr = ''.join(random.choices(string.ascii_letters, k=12))
                    with open(tmpstr, 'wb') as file:
                        print(ftp.retrbinary("RETR "+words[1], lambda data: file.write(data)))
                    if len(words) == 2:
                        os.rename(tmpstr, words[1])
                    if len(words) == 3:
                        os.rename(tmpstr, words[2])
                case "put"|"push":
                    if len(words) < 2:
                        raise Exception("Debe ingresar el nombre del archivo a subir")
                    if len(words) > 3:
                        raise Exception("Arg esperados: <archivo_a_subir> [nombre_de_archivo_remoto]")
                    with open(words[1], 'rb') as file:
                        if len(words)==2:
                            print(ftp.storbinary('STOR '+words[1], file))
                        else:
                            print(ftp.storbinary('STOR '+words[2], file))
                case "rm"|"delete":
                    if len(words) < 2:
                        raise Exception("Debe ingresar el nombre del archivo a borrar")
                    print(ftp.delete(words[1]))

                #Comandos locales
                case "lcd":
                    if len(words) != 2:
                        raise Exception("Debe ingresar el nombre del directorio local")
                    os.chdir(words[1])
                    print("Directorio actual: "+words[1])
                case "lls":
                    for item in os.listdir():
                        print(item)

        except Exception as e:
            print(e)
