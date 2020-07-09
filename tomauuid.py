#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import urllib 
import os, sys 
import string

def busca_uuid (archivo_z, clave_z):
    uuid_z = "-1"
    try:
       arch_z  = open(archivo_z, 'r')
       for linea_z in arch_z.readlines():
           inicio_z = linea_z.find(clave_z + '="')
           if inicio_z > 0:
             final_z = linea_z.find('"', inicio_z + len(clave_z)+2)
             uuid_z = linea_z[inicio_z+len(clave_z)+2: final_z]
          #End if
    except IOError:
       uuid_z = "-1"

    return uuid_z

uuid_z = busca_uuid(sys.argv[1], 'UUID')
folio_z = busca_uuid(sys.argv[1], 'folio')
serie_z = busca_uuid(sys.argv[1], 'serie')

print serie_z, folio_z, uuid_z
