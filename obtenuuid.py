#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import urllib 
import os, sys 
import string

def busca_uuid (archivo_z, cadena_z):
    uuid_z = "-1"
    try:
       arch_z  = open(archivo_z, 'r')
       for linea_z in arch_z.readlines():
           inicio_z = linea_z.find(cadena_z+'="')
           if inicio_z > 0:
             final_z = linea_z.find('"', inicio_z + 6)
             uuid_z = linea_z[inicio_z+6: final_z]
          #End if
    except IOError:
       uuid_z = "-1"

    return (uuid_z)

if len(sys.argv) > 2 :
  clave_z = sys.argv[2]
else :
   clave_z = "UUID"
#End if
miuuid_z = busca_uuid(sys.argv[1], clave_z)
print miuuid_z

