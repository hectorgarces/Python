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
        vdac_id_transit_xml_tag = root_xml_file.find("TRANSACTION_INDRA/ID_TRANSACTION")
        try:
            vdac_id_transit = int(vdac_id_transit_xml_tag.text);
        except Exception, e:
            print "Transito sin vehiculo, solo con TAG"
            continue;

        toll_class_xml_tag = root_xml_file.find("TRANSACTION_INDRA/TOLLCLASS")
        try:
            toll_class = int(toll_class_xml_tag.text);
        except Exception, e:
            print "Transito sin Clasificacion"
            continue;

        confidence_class_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/CONFIDENCE")
        try:
            confidence_class = int(confidence_class_xml_tag.text);
        except Exception, e:
            print "Clasificacion sin Confiabilidad";
        

        try:
            # Se busca la etiqueta "HEIGHT"
            vdac_height_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/HEIGHT");
            vdac_height = int(vdac_height_xml_tag.text);
            # Se busca la etiqueta "WIDTH"
            vdac_width_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/WIDTH");
            vdac_width = int(vdac_width_xml_tag.text);
            # Se busca la etiqueta "LENGTH"
            vdac_length_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/LENGTH");
            vdac_length = int(vdac_length_xml_tag.text);
            # Se busca la etiqueta "SPEED"
            vdac_length_xml_tag = root_xml_file.find("TRANSACTION_INDRA/VDACVEHICLE/SPEED");
            vdac_speed = int(vdac_length_xml_tag.text);
            
        except Exception, e:
            print "Valor de Alto, Ancho, Largo o Velocidad erroneo en el XML. ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length)+ " VELOCIDAD =" + str(vdac_speed);
            continue;

        transit_filenames = working_dir + "/*." + str(vdac_id_transit) + ".*"
        #print transit_filenames
        ficheros = glob.glob(str(transit_filenames))
        #print ficheros

        # Se analizan las nubes de puntos que tengan longitud. Si la longitud = 0 todos los puntos tienen coordenada Y=0
#        if vdac_length == 0:
#            print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE SIN LONGITUD. ID=" + str(vdac_id_transit) +  " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length);
#            for fichero in ficheros:
#                #print fichero
#                shutil.copy(fichero, working_dir + "/clase_0/");

                
        # Ligeros y Furgonetas
        if toll_class == 1:
            if confidence_class > 80:
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_1/");
            else:
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_1_lowConfidence/");

                
        # Buses y ligeros con Remolque
        elif toll_class == 2:
            if confidence_class > 80:
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_2/");
            else:
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_2_lowConfidence/");
                    

        # Camiones de 2 a 4 ejes. Camion menor de 10 metros
        elif toll_class == 3:
            if confidence_class > 80: 
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_3/");
            else:
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_3_lowConfidence/");
                    

        # Camiones de 5 a 6 ejes. Camion entre 10 y 20 metros
        elif toll_class == 4:
            if confidence_class > 80: 
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_4/");
            else:
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_4_lowConfidence/");
                    

        # Camiones con 7 o mas ejes. Camion de más de 20 metros
        elif toll_class == 5:
            if confidence_class > 80: 
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_5/");
            else:
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_5_lowConfidence/");     


        # Motos
        elif toll_class == 6:
            if confidence_class > 80: 
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_6/");
            else:
                print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
                for fichero in ficheros:
                    #print fichero
                    shutil.copy(fichero, working_dir + "/clase_6_lowConfidence/");         


        else:
            print "COPIANDO LOS FICHEROS DE UN VEHICULO CLASE " + str(toll_class) + ". ID=" + str(vdac_id_transit) + " CONFIDENCE=" + str(confidence_class) + " ALTO=" + str( vdac_height) + " ANCHO=" + str(vdac_width) + " LARGO =" + str(vdac_length) + " VELOCIDAD=" + str(vdac_speed);
            for fichero in ficheros:
                #print fichero
                shutil.copy(fichero, working_dir + "/clase_0/");
            print "El fichero: " + file + " NO tiene una CLASE válida"
    
    
#t_end = datetime.datetime.now()
#print "Finalizando el proceso de Chequeo de transitos powered by Python ... en " + str(t_end)
