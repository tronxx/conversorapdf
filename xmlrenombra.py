# -*- coding: utf-8 -*-
import xml.dom.minidom
import os, sys

archxml_z = sys.argv[1]
archivo = open(archxml_z, "r")
document = archivo.read()

htmlini_z = "<html>"
htmlfin_z = "</html>"
bodyini_z = "<body>"
bodyfin_z = "</body>"
tablaini_z = "<table border=1>"
tablafin_z = "</table>"
renini_z = "<tr>"
renfin_z = "</tr>"
colini_z = "<td>"
colfin_z = "</td>"
nvalin_z = "<br>"

#document = """\
#<slideshow>
#<title>Demo slideshow</title>
#<slide><title>Slide title</title>
#<point>This is a demo</point>
#<point>Of a program for processing slides</point>
#</slide>
#
#<slide><title>Another demo slide</title>
#<point>It is important</point>
#<point>To have more than</point>
#<point>one slide</point>
#</slide>
#</slideshow>
#"""

dom = xml.dom.minidom.parseString(document)
node = dom.documentElement;

              

def get_atrib (nodo_z, atrib_z):
    if nodo_z.hasAttribute(atrib_z): 
       mivalor_z = nodo_z.attributes[atrib_z].value
    else:
       mivalor_z = "-1"

    return mivalor_z

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handleSlideshow(slideshow):
    print htmlini_z, bodyini_z
    print tablaini_z
    print renini_z, colini_z
    node = slideshow.documentElement
    fecha_z = get_atrib(node, 'fecha')
    subtotal_z = get_atrib(node, 'subTotal')
    descto_z = ""
    serie_z = ""
    folio_z = ""
    midescto_z = get_atrib(node, "descuento")
    if(midescto_z != "-1"):
       descto_z = "Descuento: " + midescto_z
    total_z = get_atrib(node, 'total')

    emisor_z = node.getElementsByTagName('cfdi:Emisor')
    nombreemi_z = get_atrib(emisor_z[0], 'nombre')
    rfcemi_z = get_atrib(emisor_z[0], 'rfc')
    print "Emisor :  %s Rfc: %s %s" % (nombreemi_z.encode('utf8', 'replace'), rfcemi_z.encode('utf8', 'replace'), nvalin_z)
    print "Fecha  :  %s Serie: %s Folio: %s  %s" % (fecha_z, serie_z, folio_z, nvalin_z)
    receptor_z  = node.getElementsByTagName('cfdi:Receptor')
    nombrerec_z = get_atrib(receptor_z[0], 'nombre')
    rfcrec_z    = get_atrib(receptor_z[0], 'rfc')
    print "Receptor : %s Rfc: %s %s" % (nombrerec_z.encode('utf8', 'replace'), rfcrec_z.encode('utf8', 'replace'), nvalin_z)
    print colfin_z, renfin_z
    print renini_z, colini_z
    print tablaini_z, renini_z
    print colini_z, "Cantidad", colfin_z
    print colini_z, "Codigo", colfin_z
    print colini_z, "Descripcion", colfin_z
    print colini_z, "Unidad", colfin_z
    print colini_z, "Precio U", colfin_z
    print colini_z, "Importe", colfin_z
    print renfin_z
    conceptos_z = node.getElementsByTagName('cfdi:Concepto')
    for miconcep_z in conceptos_z:
        print renini_z
        codigo_z = ""
        if miconcep_z.nodeType == xml.dom.Node.ELEMENT_NODE:
           print colini_z, get_atrib(miconcep_z, 'cantidad'), colfin_z
           codigo_z = get_atrib(miconcep_z, 'noIdentificacion')

           print colini_z, codigo_z, colfin_z, \
                 colini_z, get_atrib(miconcep_z, 'descripcion'), colfin_z, \
           	 colini_z, get_atrib(miconcep_z, 'unidad').encode('utf8', 'replace'), colfin_z, \
           	 colini_z, get_atrib(miconcep_z, 'valorUnitario'), colfin_z, \
           	 colini_z, get_atrib(miconcep_z, 'importe'), colfin_z
        print renfin_z
    #End For
    print tablafin_z
    print colfin_z, renfin_z

    complementos_z = node.getElementsByTagName('tfd:TimbreFiscalDigital')
    uuid_z = get_atrib(complementos_z[0], 'UUID')
    #complementos_z = node.getElementsByTagName('cfdi:Traslados')
    iva_z = "0"
    complementos_z = node.getElementsByTagName('cfdi:Traslado')
    for miimpto_z in complementos_z:
        nombre_z = get_atrib(miimpto_z, 'impuesto')
        if nombre_z == "IVA":
           iva_z = get_atrib(miimpto_z,  'importe')
        #End if
    #End for

    print renini_z
    print colini_z
    print "UUID: %s %s Subtotal: %s %s Iva: %s Total: %s " % (uuid_z, nvalin_z, subtotal_z, descto_z, iva_z, total_z)
    print colfin_z
    print renfin_z
    print tablafin_z
    print bodyfin_z, htmlfin_z



def cfdi33(slideshow):
    print htmlini_z, bodyini_z
    print tablaini_z
    print renini_z, colini_z
    node = slideshow.documentElement
    fecha_z = get_atrib(node, 'Fecha')
    subtotal_z = get_atrib(node, 'SubTotal')
    descto_z = ""
    serie_z = ""
    folio_z = ""
    midescto_z = get_atrib(node, "Descuento")
    if(midescto_z != "-1"):
       descto_z = "Descuento: " + midescto_z
    total_z = get_atrib(node, 'Total')
    serie_z = get_atrib(node, 'Serie')
    folio_z = get_atrib(node, 'Folio')

    emisor_z = node.getElementsByTagName('cfdi:Emisor')
    nombreemi_z = get_atrib(emisor_z[0], 'Nombre')
    rfcemi_z = get_atrib(emisor_z[0], 'Rfc')
    print "Emisor :  %s Rfc: %s %s" % (nombreemi_z.encode('utf8', 'replace'), rfcemi_z.encode('utf8', 'replace'), nvalin_z)
    print "Fecha  :  %s Serie: %s Folio: %s  %s" % (fecha_z, serie_z, folio_z, nvalin_z)
    receptor_z  = node.getElementsByTagName('cfdi:Receptor')
    nombrerec_z = get_atrib(receptor_z[0], 'Nombre')
    rfcrec_z    = get_atrib(receptor_z[0], 'Rfc')
    usocfdi_z    = get_atrib(receptor_z[0], 'UsoCFDI')
    print "Receptor : %s Rfc: %s Uso Cfdi: %s %s" % (nombrerec_z.encode('utf8', 'replace'), rfcrec_z.encode('utf8', 'replace'), usocfdi_z, nvalin_z)
    print colfin_z, renfin_z
    print renini_z, colini_z 
    print tablaini_z, renini_z, \
          colini_z, "Piva", colfin_z, \
          colini_z, "Codigo", colfin_z, \
          colini_z, "Cantidad", colfin_z, \
          colini_z, "Descripcion", colfin_z, \
          colini_z, "Unidad", colfin_z, \
          colini_z, "Precio U", colfin_z, \
          colini_z, "Importe", colfin_z, \
          renfin_z
    conceptos_z = node.getElementsByTagName('cfdi:Concepto')
    for miconcep_z in conceptos_z:
        codigo_z = ""
        if miconcep_z.nodeType == xml.dom.Node.ELEMENT_NODE:
           codigo_z = get_atrib(miconcep_z, 'ClaveProdServ')
           miiva_z = miconcep_z.getElementsByTagName('cfdi:Impuestos')
           piva_z = ""
           for esteiva_z in miiva_z:
             traslados_z = esteiva_z.getElementsByTagName('cfdi:Traslados')
             mitraslado_z = traslados_z[0].getElementsByTagName('cfdi:Traslado')
             piva_z = get_atrib(mitraslado_z[0], 'TasaOCuota')[2:4]
             
           print renini_z, \
           	colini_z, piva_z, colfin_z, \
           	colini_z, codigo_z, colfin_z, \
           	colini_z, get_atrib(miconcep_z, 'Cantidad'), colfin_z, \
           	colini_z, get_atrib(miconcep_z, 'Descripcion').encode('utf8', 'replace'), colfin_z, \
           	colini_z, get_atrib(miconcep_z, 'Unidad').encode('utf8', 'replace'), colfin_z, \
           	colini_z, get_atrib(miconcep_z, 'ValorUnitario'), colfin_z, \
           	colini_z, get_atrib(miconcep_z, 'Importe'), colfin_z, renfin_z

    #End For
    print tablafin_z
    print colfin_z, renfin_z

    complementos_z = node.getElementsByTagName('tfd:TimbreFiscalDigital')
    uuid_z = get_atrib(complementos_z[0], 'UUID')
    #complementos_z = node.getElementsByTagName('cfdi:Traslados')
    iva_z = 0
    nodoshijos_z = node.childNodes
    for minodo_z in nodoshijos_z:
        nombrenodo_z = minodo_z.nodeName 
        if nombrenodo_z == "cfdi:Impuestos":
           traslados_z = minodo_z.getElementsByTagName('cfdi:Traslado')
           for miimpto_z in traslados_z:
                nombre_z = get_atrib(miimpto_z, 'Impuesto')
                if nombre_z == "002":
                   iva_z = get_atrib(miimpto_z,  'Importe')
                #End if
            #End For
        #End If
    #End for

    print renini_z
    print colini_z
    print "UUID: %s %s Subtotal: %s %s " % (uuid_z, nvalin_z, subtotal_z, descto_z)
    if descto_z > "":
       print " Importe: %s " % ( float(total_z) - float(iva_z))

    print " Iva: %s Total: %s " % (iva_z, total_z)
    print colfin_z
    print renfin_z
    print tablafin_z
    print bodyfin_z, htmlfin_z

     
    ## Voy a listar los hijos
    #--> handleHijos(node, 0)
    #listaNodos = node.childNodes
    #for nodo in listaNodos:
    #     print "Tengo Nodo Hijo: %s" % nodo.nodeName
    #     for (name, value) in nodo.attributes.items():
    #         print '    Attr -- Name: %s  Value: %s' % (name, value)
    #     #End for
    ##Enf if     print nodo.NodeName
     
      
#    handleSlideshowTitle(slideshow.getElementsByTagName("title")[0])
#    slides = slideshow.getElementsByTagName("slide")
#    handleToc(slides)
#    handleSlides(slides)
#    print "Fin"

def handleHijos(nodoconhijos, deep):
    listaNodos = nodoconhijos.childNodes
    miesp_z = "  " * deep
    for nodohijo in listaNodos:
        if nodohijo.nodeType == xml.dom.Node.ELEMENT_NODE:
           print "%sTengo Nodo Hijo: %s" % (miesp_z, nodohijo.nodeName)
           for (name, value) in nodohijo.attributes.items():
               print '%s Attr -- Name: %s  Value: %s' % (miesp_z, name, value)
           #End for
        #End if
        handleHijos (nodohijo, deep + 1)
    #Enf if     print nodo.NodeName

def handleSlides(slides):
    for slide in slides:
        handleSlide(slide)

def handleSlide(slide):
    handleSlideTitle(slide.getElementsByTagName("title")[0])
    handlePoints(slide.getElementsByTagName("point"))

def handleSlideshowTitle(title):
    print "<title>%s</title>" % getText(title.childNodes)

def handleSlideTitle(title):
    print "<h2>%s</h2>" % getText(title.childNodes)

def handlePoints(points):
    print "<ul>"
    for point in points:
        handlePoint(point)
    print "</ul>"

def handlePoint(point):
    print "<li>%s</li>" % getText(point.childNodes)

def handleToc(slides):
    for slide in slides:
        title = slide.getElementsByTagName("title")[0]
        print "<p>%s</p>" % getText(title.childNodes)

" Este seria el Main ";

version_z  = get_atrib(node, 'version')
fecha_z = get_atrib(node, 'Fecha')
emisor_z = node.getElementsByTagName('cfdi:Emisor')
nombreemi_z = get_atrib(emisor_z[0], 'nombre')
rfcemi_z = get_atrib(emisor_z[0], 'Rfc')
serie_z = get_atrib(node, 'Serie')
folio_z = get_atrib(node, 'Folio')
archivo.close();
if(serie_z == "-1"):
   serie_z = "XX";
if(folio_z == "-1"):
   folio_z = fecha_z[-2:]
nvafecha_z = fecha_z[:4] + fecha_z[5:7] + fecha_z[8:10];
nvonombre_z = nvafecha_z + "_" + rfcemi_z + "_" + serie_z + "_" + folio_z + ".xml";
#print "NvoNombre:" + nvonombre_z;
if(nvonombre_z != archxml_z ):
  print "renombrando:" + archxml_z + " -> " + nvonombre_z;
  os.rename(archxml_z, nvonombre_z);
#End if
