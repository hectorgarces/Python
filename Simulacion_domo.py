# -*- coding: cp1252 -*-
# Importar librerias de manejo de imagenes
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Importar librerias de fuentes de texto
import tkFont
#from tkinter import font

# Importar la libreria de FTP
from ftplib import FTP



# Importar librerias de OPENCV
import cv2
import cv2.cv as cv
import numpy as np
import sys

import time
import os

# Importar la libreria de SSH
import paramiko
import socket
#import pxssh
#import libssh2

server_IP = '192.168.23.148'
server_user = 'siva'
server_password = 'oracle'
ssh_port = 22

# Cliente FTP
cliente_ftp = FTP('192.168.23.148') # Conexion
cliente_ftp.login('siva', 'oracle') # Usuario y contraseña

# Cliente SSH
#conexion_ssh = paramiko.Transport((server_IP, ssh_port)) # Conexion
conexion_ssh = paramiko.SSHClient()
conexion_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
conexion_ssh.connect(hostname=server_IP, username=server_user, password=server_password) #Usuario y Contraseña
#cliente_ssh = conexion_ssh.open_session() # Se abre la conexion

# Segundos de espera entre generación de las imagenes
wait_time = 0

num_por = raw_input('Introduzca el número de pórticos por concesionaria a simular: ')
num_cam = raw_input('Introduzca el número de cámaras por pórtico a simular: ')
ftp_on = raw_input('¿Desea enviar las imagenes por FTP? (si/no): ')

initial_dir = os.getcwd()

#idPOR = num_por  #ID del portico  
#idCAM = num_cam  #ID de la cámara 
#cam.

# Inicio del bucle para la generación de imágenes
index = 0
while index < 100:
    # Se define la fuente de texto a usar
    # Tipo de fuente CV_FONT_HERSHEY_SIMPLEX = Sans-Serif de tamaño normal
    # Escalado en altura = 0.5
    # Escalado en anchura = 0.5
    # Grado de inclinacion de la letra (cursiva) = 0
    # Grado de grosor = 1
    # Tipo de linea = 8
    font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3, 0, 1, 8)
    
    # Se obtiene la fecha y hora actuales, para posteriormente escribirlo sobre las imagenes
    horaRaw = time.time()
    horaFormato = time.ctime(horaRaw) 
    
    # Se obtiene el nombre del fichero a almacenar excepto el id del portico
    seconds = time.strftime("%S",time.gmtime(horaRaw)) #Segundos
    minutes = time.strftime("%M",time.gmtime(horaRaw)) #Minutos
    hour = time.strftime("%H",time.gmtime(horaRaw))    #Hora
    day = time.strftime("%d",time.gmtime(horaRaw))     #Dia
    month = time.strftime("%m",time.gmtime(horaRaw))   #Mes
    year = time.strftime("%Y",time.gmtime(horaRaw))    #Año

    #IDs de las concesionarias
    id_concesionarias = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

    #Se almacenan los nombres de las imagenes de fondo usado en cada Concesionaria
    load_image_name= ['','','','','','','','','','','']
    load_image_name[1] = "Durban_SA.jpg"
    load_image_name[2] = "71.jpg"
    load_image_name[3] = 'BBT_toll_plaza_jeh.jpg'
    load_image_name[4] = 'ji_0379.jpg'
    load_image_name[5] = 'BAKWENA-TOLL-PLAZA.jpg'
    load_image_name[6] = 'peaje 6.jpg'
    load_image_name[7] = 'peaje 7.jpg'
    load_image_name[8] = 'peaje 8.jpg'
    load_image_name[9] = 'peaje 9.jpg'
    load_image_name[10] = 'peaje 10.jpg'
   
    indice_concesionaria = 1  
    for concesionaria in id_concesionarias:
        idCONC = concesionaria
        idPOR = 1
        idCAM = 1
        # Se forma el nombre del path
        #image_name = "img_" + idCONC + "_" + str(idPOR) + "_" + str(idCAM) + "_" + year + "_" + month + "_" + day + "_" + hour + "_" + minutes + "_" + seconds + ".jpg"
        #image_path = "Cliente\\Images 3\\" + image_name
        # Se carga el nombre de la imagenes
        name = load_image_name[indice_concesionaria]
        indice_concesionaria = indice_concesionaria + 1

        while idPOR <= int(num_por):
            idCAM = 1
            while idCAM <= int(num_cam):
                print "Generando imagenes de la Camara = " + str(idCAM) + " | Portico = " + str(idPOR) + " | Concesionaria = " + idCONC
                time.sleep(1)
                # Se forma el nombre del fichero de imagen
                image_name = "img_" + idCONC + "_" + str(idPOR) + "_" + str(idCAM) + "_" + year + "_" + month + "_" + day + "_" + hour + "_" + minutes + "_" + seconds + ".jpg"  
                
                #Se ubica en el directorio raiz
                os.chdir(initial_dir)
                # Se lee la imagen
                image = cv.LoadImage(name)    
                # Se añade el texto en la imagen
                # En la Linea 1 => Texto de identificación de la CONCESIONARIA 
                cv.PutText(image, 'CONCESIONARIA: ' + idCONC, (0,10), font, cv.RGB(250,255,255) )
                # En la Linea 2 => Texto de identificación del PORTICO
                cv.PutText(image, 'PORTICO: ' + str(idPOR), (0,20), font, cv.RGB(250,255,255) )
                # En la Linea 3 => Texto de identificación de la cámara
                cv.PutText(image, 'CAMARA: ' + str(idCAM), (0,30), font, cv.RGB(250,255,255) )
                # En la Linea 4 => Texto de Fecha y hora
                cv.PutText(image, horaFormato, (0,40), font, cv.RGB(250,255,255) )

                # Se almacena la imagen en LOCAL
                # Se forma el directorio en el que almacenar imagen en local
                image_dir = "IMAGES\\" + idCONC + "\\" + str(idPOR) + "\\" + str(idCAM) + "\\" + year + "\\" + month + "\\" + day + "\\" + hour + "\\"                        
                # Si no existe el directorio, se crea. Comprobando toda la ruta
                if not os.path.isdir(image_dir):
                    # IMAGES
                    try:
                        os.chdir("IMAGES")
                    except:
                        os.mkdir("IMAGES")
                        os.chdir("IMAGES")

                    # CONCESIONARIA
                    try:
                        os.chdir(idCONC)
                    except:
                        os.mkdir(idCONC)
                        os.chdir(idCONC)

                    # PORTICO
                    try:
                        os.chdir(str(idPOR))
                    except:
                        os.mkdir(str(idPOR))
                        os.chdir(str(idPOR))

                    # CAMARA
                    try:
                        os.chdir(str(idCAM))
                    except:
                        os.mkdir(str(idCAM))
                        os.chdir(str(idCAM))

                    # AÑO
                    try:
                        os.chdir(year)
                    except:
                        os.mkdir(year)
                        os.chdir(year)

                    # MES
                    try:
                        os.chdir(month)
                    except:
                        os.mkdir(month)
                        os.chdir(month)

                    # DIA
                    try:
                        os.chdir(day)
                    except:
                        os.mkdir(day)
                        os.chdir(day)

                    # HORA
                    try:
                        os.chdir(hour)
                    except:
                        os.mkdir(hour)
                        os.chdir(hour)
                    
                    cv.SaveImage(image_name, image)
 #                   print "Directorio Local Creado. IMAGEN ALMCENADA en: " + image_name

                # Si el directorio existe, se almacena la imagen
                else:    
                    # Se obtiene la ruta de la imagen
                    image_path = image_dir + image_name
                    # Se almacena la imagen
                    cv.SaveImage(image_path, image)
 #                   print "Directorio Local existente. IMAGEN ALMCENADA en: " + image_path


                ################################################################################################################################
                # Se almacena la imagen en remoto
                # Se almacena la imagen en remoto en windows: Unidad X conectada a 192.168.23.147
                #image_dir_2 = "X:\\" + image_path
                 # Si no existe el directorio, se crea
                #if not os.path.isdir(image_dir_2):
                #    os.mkdir(image_dir_2)
                #image_path_2 = image_dir_2 + image_name
                #cv.SaveImage(image_path2, image)
                ################################################################################################################################


                ################################################################################################################################
                # Se almacena en el servidor FTP, si lo hemos configurado
                if ftp_on == "si":
                    # Se almacena la imagen en el servidor FTP
                    # "/var/ftp/pub/IMAGEN" + "/" +
                    # Se accede al directorio raiz de las imagenes
                    result = cliente_ftp.cwd("/var/ftp/pub/IMAGES")

                    # Se accede al directorio de la CONCESIONARIA (si no existe se crea)
                    try:
                        cliente_ftp.cwd(idCONC)
                    except:
                        cliente_ftp.mkd(idCONC)
                        cliente_ftp.cwd(idCONC)

                    # Se accede al directorio del PORTICO (si no existe se crea)
                    try:
                        cliente_ftp.cwd(str(idPOR))
                    except:
                        cliente_ftp.mkd(str(idPOR))
                        cliente_ftp.cwd(str(idPOR))

                    # Se accede al directorio de la CAMARA (si no existe se crea)
                    try:
                        cliente_ftp.cwd(str(idCAM))
                    except:
                        cliente_ftp.mkd(str(idCAM))
                        cliente_ftp.cwd(str(idCAM))

                    # Se accede al directorio del AÑO (si no existe se crea)
                    try:
                        cliente_ftp.cwd(year)
                    except:
                        cliente_ftp.mkd(year)
                        cliente_ftp.cwd(year)

                    # Se accede al directorio del MES (si no existe se crea)
                    try:
                        cliente_ftp.cwd(month)
                    except:
                        cliente_ftp.mkd(month)
                        cliente_ftp.cwd(month)

                    # Se accede al directorio del DÍA (si no existe se crea)
                    try:
                        cliente_ftp.cwd(day)
                    except:
                        cliente_ftp.mkd(day)
                        cliente_ftp.cwd(day)

                    # Se accede al directorio de la HORA(si no existe se crea)
                    try:
                        cliente_ftp.cwd(hour)
                    except:
                        cliente_ftp.mkd(hour)
                        cliente_ftp.cwd(hour)

                    #Se ubica en el directorio raiz de la maquina local
                    os.chdir(initial_dir)
                    # Se obtiene la ruta de la imagenes
                    image_path = image_dir + image_name
                    # Se abre, en local, la imagen creada.
                    f = open(image_path, 'rb')
 #                   print "Imagen ubicada en " + image_path + " ALMCENADA vía FTP" 

                    # Se envía la imagen por FTP al servidor a la carpeta /AAAA/MM/DD/HH
                    cliente_ftp.storbinary('STOR ' + image_name, f)
                    # se cambian los permisos del fichero a 766
                    cliente_ftp.sendcmd('SITE CHMOD 766 ' + image_name)
                    
                    # Se ejecuta el comando via SSH para copiar el fichero "last.jpg"
                    image_dir_ssh = '/var/ftp/pub/IMAGES/'+idCONC+'/'+str(idPOR)+'/'+str(idCAM)+'/'+year+'/'+month+'/'+day+'/'+hour+'/'
                    image_path_ssh = image_dir_ssh + image_name
                    comando_ssh = 'cp -p ' + image_path_ssh + ' /var/ftp/pub/IMAGES/' + idCONC + '/' + str(idPOR) + '/' + str(idCAM) + '/final.jpg'
 #                   print "Ejecutando por SSH el comando: " + comando_ssh
                    #cliente_ssh.cwd("/var/ftp/pub/IMAGES/" + idCONC + str(idPOR) + str(idCAM))
                    stdin, stdout, stderr = conexion_ssh.exec_command(comando_ssh)
                    print stdout.read()
                    #print cliente_ssh.exec_command(comando_ssh)


                    # Se envía la imagen por FTP al directorio raiz de la camara
                    #f = open(image_path, 'rb')
                    #cliente_ftp.cwd("/var/ftp/pub/IMAGES")# + idCONC + str(idPOR) + str(idCAM))
                    #cliente_ftp.cwd(idCONC)
                    #cliente_ftp.cwd(str(idPOR))
                    #cliente_ftp.cwd(str(idCAM))
                    #cliente_ftp.storbinary('STOR last.jpg', f)
                    
                #FIN del if ftp_on == si
                ################################################################################################################################

                    
                idCAM = idCAM + 1
                
            idPOR = idPOR + 1
            
            # FIN del while indice_camara <= num_camara:
            
          # FIN del while indice_portico <= num_por:                        
 
    # FIN del "for portico in num_porticos:"

    # se realiza la espera entre la generación de imágenes
    time.sleep(wait_time)

    index = index + 1
    # FIN del "while index < 3600:"
