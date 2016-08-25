# -*- coding: cp1252 -*-
import os
import shutil
import glob
import numpy as np
from lxml import etree
import datetime

working_dir = raw_input('Insert the name of Working Directory: ')

num_transitos = 0;
num_ficheros = 0;
xml_files = os.listdir(str(working_dir));
#xml_files = os.listdir('datos1')
#t_init = datetime.datetime.no()
#print "Inicializado el proceso de Chequeo de transitos powered by Python ... en " + str(t_init)
for file in xml_files:
    # Si la extension del fichero es XML, se analiza el contenido
    if file[-4:]==".xml":
        filename = working_dir + "/" + str(file)
        # Se forma el path del fichero xml, que esta dentro de la carpeta "datos1"
        filexml = open(filename)
        datosxml = filexml.read()
        # Se pasa el fichero a una estructura etree para manejar el XML
        root_xml_file = etree.fromstring(datosxml)

        # Se busca el ID_TRANSITO
        vdac_id_transit_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/ID_TRANS_VDAC")
        try:
            vdac_id_transit = int(vdac_id_transit_xml_tag.text);
        except Exception, e:
            print "Transito sin vehiculo, solo con TAG"
            continue
        
        # Se busca la etiqueta "HEIGHT"
        vdac_height_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/HEIGHT")
        vdac_height = int(vdac_height_xml_tag.text)
        # Se busca la etiqueta "WIDTH"
        vdac_width_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/WIDTH")
        vdac_width = int(vdac_width_xml_tag.text)
        # Se busca la etiqueta "LENGTH"
        vdac_length_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/LENGTH")
        vdac_length = int(vdac_length_xml_tag.text)

        transit_filenames = working_dir + "/*." + str(vdac_id_transit) + ".*"
        #print transit_filenames
        ficheros = glob.glob(str(transit_filenames))
        #print ficheros

        # Se analizan las nubes de puntos que tengan longitud. Si la longitud = 0 todos los puntos tienen coordenada Y=0
        if vdac_length > 1:
            # Ligeros o motos
            if vdac_height < 210:
                # MOTO
                if vdac_width < 100:
                    print "COPIANDO LOS FICHEROS PCD DE MOTO. ID=" + str(vdac_id_transit) +  " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length);
                    for fichero in ficheros:
                        #print fichero
                        shutil.copy(fichero, working_dir + "/motos/");

                #Ligero con remolque
                elif vdac_length > 1000:
                    print "COPIANDO LOS FICHEROS PCD DE LIGERO CON REMOLQUE. ID=" + str(vdac_id_transit) +  " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length);
                    for fichero in ficheros:
                        #print fichero
                        shutil.copy(fichero, working_dir+ "/ligerosRemolque/");

                # Ligero
                else:
                    print "COPIANDO LOS FICHEROS PCD DE LIGERO. ID=" + str(vdac_id_transit) +  " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length);
                    for fichero in ficheros:
                        #print fichero
                        shutil.copy(fichero, working_dir + "/ligeros/");

            #Furgonetas o Van o Minibus
            elif vdac_height < 300:
                print "COPIANDO LOS FICHEROS PCD DE FURGONETA. ID=" + str(vdac_id_transit) +  " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length);           
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir+ "/furgonetas/");
            
            # Pesados
            else:
                print "COPIANDO LOS FICHEROS PCD DE PESADO. ID=" + str(vdac_id_transit) +  " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length);           
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir+ "/pesados/");

        else:
            print "El fichero: " + file + " NO tiene una nube de puntos válida"
    
    
#t_end = datetime.datetime.now()
#print "Finalizando el proceso de Chequeo de transitos powered by Python ... en " + str(t_end)
