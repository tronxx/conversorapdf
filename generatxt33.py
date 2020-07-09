#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from Numerals import numerals
import os, sys
import textwrap
import re
#Importamos el módulo
from xml.dom import minidom
import xml.dom.minidom

#Creamos una función que busca un tag dado en un fichero XML
#y nos devuelve una lista con todos los contenidos que había
#dentro de los tags.

def buscaXMLTag(xmlFile,xmlTag):
  resultList = []
  dom = minidom.parse(xmlFile)
  nodes = dom.childNodes
  comprobante = nodes[0]
  compAtrib = dict(comprobante.attributes.items())
  
  
  for ii_z in ['Sello', 'Certificado', 
    'Folio', 'Serie', 'FormaPago', 'Fecha',
    'MetodoPago', 'Total', 'NoCertificado', 'LugarExpedicion', 'Version'
    ]:
    dato_z = ''
    if ii_z in compAtrib.keys():
       dato_z =  compAtrib[ii_z]
    #End if
    if ii_z == "NoCertificado":
       ii_z = "noCertificadoSAT";
    if ii_z == "Total":
       ii_z = "total";
    if ii_z == "Folio":
       ii_z = "folio";
    if ii_z == "Serie":
       ii_z = "serie";
    if ii_z == "FormaPago":
       ii_z = "metodoDePago";
    if ii_z == "Fecha":
       ii_z = "fecha";
    if ii_z == "MetodoPago":
       ii_z = "metodoDePago";
    
    resultList.append([ii_z, dato_z])
  #End for
  ## Ahora voy a buscar el CFDIOriginal si es NC
  cfdirelacionados_z  = comprobante.getElementsByTagName('cfdi:CfdiRelacionado')
  ii_z = "UUID"
  dato_z = ''
  for minodo_z in cfdirelacionados_z:
      if minodo_z.hasAttribute(ii_z): 
         dato_z = minodo_z.getAttribute(ii_z)
         ii_z = 'FolioFiscalOrig'
         resultList.append([ii_z, dato_z])
      #End If
  #End For
  
  ## Ahora voy a completar la direccion de Expedicion
  dato_z = ''
  receptores_z  = comprobante.getElementsByTagName('cfdi:ExpedidoEn')
  for receptor_z in receptores_z:
    for ii_z in ['calle', 'noExterior', 'colonia', 'municipio', 'LugarExpedicion', 'estado']:
      if receptor_z.hasAttribute(ii_z): 
        if ii_z == 'calle':
           dato_z = dato_z + 'Calle '
        elif ii_z == 'noExterior':
           dato_z = dato_z + ' N.'
        elif ii_z == 'colonia':
           dato_z = dato_z + ' Col:'
        else :
           dato_z = dato_z + ' '
        #End if
        dato_z =  dato_z + receptor_z.getAttribute(ii_z)
      #End If
    #End for
  #End for
  resultList.append(['LugarExpedicion', dato_z])
  
  
  ## Ahora voy a buscar los datos del Receptor:
  receptores_z  = comprobante.getElementsByTagName('cfdi:Receptor')
  for receptor_z in receptores_z:
    for ii_z in ['Nombre']:
      if receptor_z.hasAttribute(ii_z): 
        dato_z  = receptor_z.getAttribute(ii_z)
        dato_z = dato_z.encode('ascii', 'replace')
        if ii_z == "Nombre":
           ii_z = "nombre"
        resultList.append([ii_z, dato_z])
      #End If
    #End For
  #End for
  receptores_z  = comprobante.getElementsByTagName('tfd:TimbreFiscalDigital')
  for receptor_z in receptores_z:
    for ii_z in ['UUID', 'selloCFD', 'noCertificadoSAT', 'selloSAT', 'version', 'FechaTimbrado']:
      if receptor_z.hasAttribute(ii_z): 
         dato_z  = receptor_z.getAttribute(ii_z)
         resultList.append([ii_z, dato_z])
      #End if
    #End for
  #End for
  receptores_z  = comprobante.getElementsByTagName('cfdi:Domicilio')
  direc_z = ""
  atrib_z = ""
  municipio_z = ""
  for receptor_z in receptores_z:
    for ii_z in ['calle', 'noExterior', 'colonia', 'localidad' ]:
      if receptor_z.hasAttribute(ii_z): 
         atrib_z = receptor_z.getAttribute(ii_z)
         if ii_z != "calle":
            direc_z = direc_z + " "
         #End if
         if ii_z == "noExterior":
            direc_z = direc_z + "N."
         #end if
         if ii_z == "colonia":
            if atrib_z == "0":
               atrib_z = ""
            #End if
            if atrib_z != "":
               direc_z = direc_z + "Col:"
          #End if
        #End if
      #end if
      direc_z  = direc_z + atrib_z
      #resultList.append([ii_z, dato_z])
    #End for
    if receptor_z.hasAttribute("municipio"): 
      municipio_z  = receptor_z.getAttribute("municipio")
  #End For
  resultList.append(["direc", direc_z])
  resultList.append(["municipio", municipio_z])
  
  renglones_z = comprobante.getElementsByTagName('cfdi:Conceptos')
  jj_z = 0;
  for mirenglon_z in renglones_z:
      jj_z = jj_z + 1
      node = mirenglon_z.getElementsByTagName('cfdi:Concepto')
      for minodo_z in node:
        if minodo_z.nodeType == xml.dom.Node.ELEMENT_NODE:
           for datoren_z in ['Cantidad', 'Descripcion', 'ValorUnitario']:
              if minodo_z.hasAttribute(datoren_z):
                dato_z =minodo_z.getAttribute(datoren_z)
                ii_z = datoren_z
                if ii_z == "Descripcion":
                   ii_z =  "descripcion" 
                if ii_z == "ValorUnitario":
                   ii_z =  "valorUnitario" 
                ii_z = ii_z + str(jj_z)
                resultList.append([ii_z, dato_z])
              #EndIf
           #End for
        #End if
      #End for
  #End for
  if jj_z < 2:
      resultList.append(["descripcion2", ""])
      resultList.append(["valorUnitario2", "0"])
  #End for
 
  return resultList

def currency(amount):
    temp = "%.2f" % amount
    profile=re.compile(r"(\d)(\d\d\d[.,])")
    while 1:
      temp, count = re.subn(profile,r"\1,\2",temp)
      if not count:
         break
    # optionally adds a dollar sign
    return temp
#End def                                               

#Ejecutamos la función y sacamos por pantalla todo el contenido encontrado
archxml_z = sys.argv[1]
archformato_z = sys.argv[2]
miformato_z = open(archformato_z, "r")
linformato_z = miformato_z.readlines()
claves_z = {
"@nfac":"folio", 
"@seriefac":"serie", 
"@fecha" : "fecha",
"@nombre" : "nombre",
"@direc" : "direc",
"@poblac": "municipio", 
"@uuidabono":"UUID", 
"@fechcerti":"FechaTimbrado", 
"@certiemi":"noCertificado",
"@concepto1": "descripcion1", 
"@importe1": "valorUnitario1",
"@concepto2": "descripcion2",
"@importe2": "valorUnitario2", 
"@impletras": "total", 
"@total":"total",
"@certisat":"noCertificadoSAT", 
"@uuidfacorig":"FolioFiscalOrig", 
"@formapago":"metodoDePago", 
"@lugexp":"LugarExpedicion",
"@cadena":"certificado", 
"@sellodigital":"sello", 
"@sellosat":"selloSAT"
}
datos_z = buscaXMLTag(archxml_z, 'cfdi:Comprobante')
misdatos_z = dict(datos_z)
#print misdatos_z.keys()
#print misdatos_z.values()
#print claves_z.keys()
#print claves_z.values()
repite_z = "NO"
numlins_z = 0;
lineasxpag_z = 33
for linea_z in linformato_z:
    numlins_z = numlins_z + 1
    repite_z = ""
    for miclave_z in claves_z.keys():
        if linea_z.find(miclave_z) > -1:
             nvaclave_z = claves_z[miclave_z]
             if nvaclave_z in misdatos_z:
                nvodato_z = misdatos_z[nvaclave_z]
             
             #nvodato_z = misdatos_z.get(nvaclave_z, default=None)
             if miclave_z == "@cadena":
                nvodato_z = "||"
                if "version" in misdatos_z:
                  nvodato_z = nvodato_z + misdatos_z['version']
                if "UUID" in misdatos_z:
                  nvodato_z = nvodato_z + "|" +  misdatos_z['UUID']
                if "fecha" in misdatos_z:
                  nvodato_z = nvodato_z + "|" + misdatos_z['fecha']
                if "sello" in misdatos_z:
                  nvodato_z = nvodato_z + "|" + misdatos_z['sello']
                if "noCertificadoSAT" in misdatos_z:
                  nvodato_z = nvodato_z + "|" + misdatos_z['noCertificadoSAT']
                nvodato_z = nvodato_z + "||"
             #End if 
            
             if miclave_z == "@concepto1" or miclave_z == "@concepto2":
                miclave_z = miclave_z.ljust(45, ' ')
                nvodato_z = nvodato_z.ljust(45, ' ')
             #End if
             if miclave_z == "@importe1" or miclave_z == "@importe2":
                miclave_z = miclave_z.rjust(14, ' ')
                import_z = float(nvodato_z) * 1.16
                nvodato_z = currency(import_z)
                if nvodato_z == '0.00' :
                   nvodato_z = ''
                nvodato_z = nvodato_z.rjust(14, ' ')
             #End if
             if miclave_z == "@total":
                miclave_z = miclave_z.rjust(14, ' ')
                import_z = float(nvodato_z)
                nvodato_z = currency(import_z)
                nvodato_z = nvodato_z.rjust(14, ' ')
             #End if
             if miclave_z == "@impletras":
                total_z = float(nvodato_z)
                impletras_z = "%0.2f" % total_z
                impletras_z = " Pesos " + impletras_z[-2:] + "/100)"
                impletras_z = "(Son: " + numerals(int(total_z), 0) + impletras_z
                datimpletras_z = textwrap.wrap(impletras_z, 45)
                miclave_z = miclave_z.ljust(45, ' ')
                nvodato_z = datimpletras_z[0].ljust(45, ' ')
                if len(datimpletras_z) > 1:
                   repite_z = "REPITE_IMPLETRAS"
                #End if // En case de que haya que acompletar los datos del importe en letras
             #End if
             if miclave_z == "@sellodigital" or miclave_z == "@cadena" or miclave_z == "@sellosat":
                datimpletras_z = textwrap.wrap(nvodato_z, 130)
                nvodato_z = datimpletras_z[0]
                if len(datimpletras_z) > 1:
                   repite_z = "REPITE_SELLO_CADENA"
                #End if // En case de que haya que acompletar los datos del importe en letras
             #End if
             linea_z = linea_z.replace(miclave_z, nvodato_z)
        #End if
    #End for
    print linea_z.strip('\n\r')
    if repite_z == "REPITE_IMPLETRAS":
       ini_z = 0
       for nvodato_z in datimpletras_z:
         if ini_z > 0:
            milin_z = nvodato_z
            milin_z = nvodato_z.ljust(59, ' ') + "|" + " ".ljust(14, ' ') + "|"
            print milin_z
            numlins_z = numlins_z + 1
         #End if
         ini_z = ini_z + 1
       #End for
     #End if
    if repite_z == "REPITE_SELLO_CADENA":
       ini_z = 0
       for nvodato_z in datimpletras_z:
         if ini_z > 0:
            print nvodato_z
            numlins_z = numlins_z + 1
         #End if
         ini_z = ini_z + 1
       #End for
     #End if
#End for
residuo_z = 33 % numlins_z
if residuo_z > 0:
  lineasfalta_z = 33 - residuo_z
  for ii_z in range(lineasfalta_z):
      print
  #End for
#End if
