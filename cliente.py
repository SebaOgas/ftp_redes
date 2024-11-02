"""
Implementar una aplicación cliente de FTP, con las siguientes características:
    Soportar los comandos más comunes de FTP.
    Se debe poder subir y bajar archivos desde un servidor de FTP.
"""
import ftplib

with ftplib.FTP() as ftp:
    # conexión al servidor local
    ftp.connect('127.0.0.1', 2121)
    
    # obtener mensaje de bienvenida
    print(ftp.getwelcome())

    # identificación
    ftp.login('admin', 'admin')

    # ver directorio
    print(ftp.retrlines('LIST'))

    # crear directorio
    ftp.mkd(f'ejemplo_1')
    print('Creado directorio ejemplo_1\n')
    
    # cambiar de directorio
    ftp.cwd('/ejemplo_1/')
    print('Cambiar a directorio ejemplo_1\n')

    #subir un fichero de texto
    with open('prueba.txt', 'rb') as txt_file:
        ftp.storbinary('STOR prueba_up.txt', txt_file)

    # ver directorio
    print(ftp.retrlines('LIST'))

    # cambiar de directorio
    ftp.cwd('/')
    print('Cambiar a directorio raíz\n')

    # ver directorio
    print(ftp.retrlines('LIST'))
