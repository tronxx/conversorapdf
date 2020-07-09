# -*- coding: utf-8 -*-
import xml.dom.minidom
import os, sys
import re
import time

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
colinir_z = "<td align=\"right\">"
colfin_z = "</td>"
nvalin_z = "<br>"
reninitxt_z = ""
colinitxt_z = ""
colfintxt_z = "|"
renfintxt_z = ""

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
    serie_z = get_atrib(node, 'serie')
    folio_z = get_atrib(node, 'folio')

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
    print colini_z, "Fecha.Pago", colfin_z
    print colini_z, "UUID", colfin_z
    print colini_z, "FOLIO", colfin_z
    print colini_z, "SERIE", colfin_z
    print colini_z, "Parcialidad", colfin_z
    print colini_z, "Saldo.Ant", colfin_z
    print colini_z, "Importe", colfin_z
    print colini_z, "Saldo.Nvo", colfin_z
    print renfin_z
    todospagos_z = node.getElementsByTagName('cfdi:Complemento')
    pagos_z = todospagos_z.getElementsByTagName('pago10:Pagos')
    for mipago_z in pagos_z:
        print renini_z
        codigo_z = ""
        estepago_z = mipago_z.getElementsByTagName('pago10:Pago')
        if mipago_z.nodeType == xml.dom.Node.ELEMENT_NODE:
           fechapago_z = get_atrib(mipago_z, 'FechaPago')
           importe_z = get_atrib(mipago_z, 'Monto')
           estepago_z = estepago_z.getElementsByTagName('pago10:DoctoRelacionado')
           uuid_z = get_atrib(estepago_z, 'IdDocumento')
           serie_z = get_atrib(estepago_z, 'Serie')
           folio_z = get_atrib(estepago_z, 'Folio')
           parcialidad_z = get_atrib(estepago_z, 'NumParcialidad')
           sdoant_z = get_atrib(estepago_z, 'ImpSaldoAnt')
           nvosdo_z = get_atrib(estepago_z, 'ImpSaldoInsoluto')

           print colini_z, fechapago_z, colfin_z
           print colini_z, uuid_z, colfin_z
           print colini_z, folio_z, colfin_z
           print colini_z, serie_z, colfin_z
           print colini_z, parcialidad_z, colfin_z
           print colini_z, sdoant_z, colfin_z
           print colini_z, importe_z, colfin_z
           print colini_z, sdonvo_z, colfin_z
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
    print tablaini_z, renini_z
    print colini_z, "Fecha.Pago", colfin_z
    print colini_z, "UUID", colfin_z
    print colini_z, "FOLIO", colfin_z
    print colini_z, "SERIE", colfin_z
    print colini_z, "Parcialidad", colfin_z
    print colini_z, "Saldo.Ant", colfin_z
    print colini_z, "Importe", colfin_z
    print colini_z, "Saldo.Nvo", colfin_z
    print renfin_z
    total_z = 0
    todospagos_z = node.getElementsByTagName('cfdi:Complemento')
    pagos_z = node.getElementsByTagName('pago10:Pago')
    for mipago_z in pagos_z:
        print renini_z
        codigo_z = ""
        ##estepago_z = mipago_z.getElementsByTagName('pago10:Pago')
        if mipago_z.nodeType == xml.dom.Node.ELEMENT_NODE:
           fechapago_z = get_atrib(mipago_z, 'FechaPago')
           importe_z = get_atrib(mipago_z, 'Monto')
           estepago_z = mipago_z.getElementsByTagName('pago10:DoctoRelacionado')
           for esmipago_z in estepago_z:
               uuid_z = get_atrib(esmipago_z, 'IdDocumento')
               serie_z = get_atrib(esmipago_z, 'Serie')
               folio_z = get_atrib(esmipago_z, 'Folio')
               parcialidad_z = get_atrib(esmipago_z, 'NumParcialidad')
               sdoant_z = get_atrib(esmipago_z, 'ImpSaldoAnt')
               sdonvo_z = get_atrib(esmipago_z, 'ImpSaldoInsoluto')
               importe_z = get_atrib(esmipago_z, 'ImpPagado')
               total_z += float(importe_z)
            #End If

           print colini_z, fechapago_z[:10], colfin_z
           print colini_z, uuid_z, colfin_z
           print colinir_z, folio_z, colfin_z
           print colini_z, serie_z, colfin_z
           print colinir_z, parcialidad_z, colfin_z
           print colinir_z, currency(float(sdoant_z)), colfin_z
           print colinir_z, currency(float(importe_z)), colfin_z
           print colinir_z, currency(float(sdonvo_z)), colfin_z
           print renfin_z
    #End For

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
    print colini_z, "Total", colfin_z
    print colini_z, "UUID: %s " % (uuid_z), colfin_z
    print colini_z, colfin_z
    print colini_z, colfin_z
    print colini_z, colfin_z
    print colini_z, colfin_z
    print colinir_z, currency(total_z), colfin_z
    print renfin_z
    print tablafin_z
    print bodyfin_z, htmlfin_z

     
def txtcfdi33(slideshow):
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
    print imprifont('CONDENSADO_ON') + reninitxt_z + colinitxt_z + ('-' * 115)
    micad_z =   nombreemi_z 
    print colfintxt_z + micad_z.center(113, ' ') + colfintxt_z
    micad_z = time.strftime("%d/%m/%Y %H:%M:%S") + "  Poliza de Cobranza "
    print colfintxt_z + time.strftime("%d/%m/%Y %H:%M:%S") + " Poliza de Cobranza ".center(73, ' ') + " ".ljust(21, ' ') + colfintxt_z
    micad_z = "CFDI Pagos Emisor : " + nombreemi_z.encode('utf8', 'replace') + "      RFC: " + rfcemi_z.encode('utf8', 'replace') 
    print colfintxt_z + micad_z.ljust(113, ' ') + colfintxt_z
    micad_z = "Fecha             : " + fecha_z + "      Serie: " + serie_z + "      Folio:" + str(folio_z)
    print colfintxt_z + micad_z.ljust(113, ' ') + colfintxt_z
    receptor_z  = node.getElementsByTagName('cfdi:Receptor')
    nombrerec_z = get_atrib(receptor_z[0], 'Nombre')
    rfcrec_z    = get_atrib(receptor_z[0], 'Rfc')
    usocfdi_z    = get_atrib(receptor_z[0], 'UsoCFDI')
    micad_z = "Receptor          : " + nombrerec_z.encode('utf8', 'replace') + "      RFC:" + rfcrec_z.encode('utf8', 'replace') + "      Uso CFDI:" + usocfdi_z
    print colfintxt_z + micad_z.ljust(113, ' ') + colfintxt_z
    print reninitxt_z + colinitxt_z + ('-' * 115)
    print colfintxt_z + "Fecha.Pago".ljust(10, ' ') + colfintxt_z, #
    print colinitxt_z + "UUID".ljust(37, ' ')       + colfintxt_z, #
    print colinitxt_z + "FOLIO".ljust(6, ' ')       + colfintxt_z, #
    print colinitxt_z + "SERIE".ljust(6, ' ')       + colfintxt_z, #
    print colinitxt_z + "Pago".ljust(4, ' ')        + colfintxt_z, #
    print colinitxt_z + "Saldo.Ant".ljust(12, ' ')  + colfintxt_z, #
    print colinitxt_z + "Importe".ljust(12, ' ')    + colfintxt_z, #
    print colinitxt_z + "Saldo.Nvo".ljust(12, ' ')  + colfintxt_z, #
    print renfintxt_z
    total_z = 0
    todospagos_z = node.getElementsByTagName('cfdi:Complemento')
    pagos_z = node.getElementsByTagName('pago10:Pago')
    for mipago_z in pagos_z:
        codigo_z = ""
        ##estepago_z = mipago_z.getElementsByTagName('pago10:Pago')
        if mipago_z.nodeType == xml.dom.Node.ELEMENT_NODE:
           fechapago_z = get_atrib(mipago_z, 'FechaPago')
           importe_z = get_atrib(mipago_z, 'Monto')
           estepago_z = mipago_z.getElementsByTagName('pago10:DoctoRelacionado')
           for esmipago_z in estepago_z:
               uuid_z = get_atrib(esmipago_z, 'IdDocumento')
               serie_z = get_atrib(esmipago_z, 'Serie')
               folio_z = get_atrib(esmipago_z, 'Folio')
               parcialidad_z = get_atrib(esmipago_z, 'NumParcialidad')
               sdoant_z = get_atrib(esmipago_z, 'ImpSaldoAnt')
               sdonvo_z = get_atrib(esmipago_z, 'ImpSaldoInsoluto')
               importe_z = get_atrib(esmipago_z, 'ImpPagado')
               total_z += float(importe_z)
            #End If

           print colfintxt_z + fechapago_z[:10]                          + colfintxt_z, #
           print colinitxt_z + uuid_z.ljust(37, ' ')                     + colfintxt_z, #
           print colinitxt_z + folio_z.rjust(6, ' ')                     + colfintxt_z, #
           print colinitxt_z + serie_z.ljust(6, ' ')                     + colfintxt_z, #
           print colinitxt_z + parcialidad_z.rjust(4, ' ')               + colfintxt_z, #
           print colinitxt_z + currency(float(sdoant_z)).rjust(12, ' ')  + colfintxt_z, #
           print colinitxt_z + currency(float(importe_z)).rjust(12, ' ') + colfintxt_z, #
           print colinitxt_z + currency(float(sdonvo_z)).rjust(12, ' ')  + colfintxt_z, #
           print renfintxt_z
    #End For

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

    print reninitxt_z + colinitxt_z + ('-' * 115)
    print colfintxt_z + "Total".ljust(10, ' ')           + colfintxt_z, #
    print colinitxt_z + uuid_z.ljust(37, ' ')            + colfintxt_z, #
    print colinitxt_z + "".ljust(6, ' ')                 + colfintxt_z, #
    print colinitxt_z + "".ljust(6, ' ')                 + colfintxt_z, #
    print colinitxt_z + "".ljust(4, ' ')                 + colfintxt_z, #
    print colinitxt_z + "".ljust(12, ' ')                + colfintxt_z, #
    print colinitxt_z + currency(total_z).rjust(12, ' ') + colfintxt_z, #
    print colinitxt_z + "".ljust(12, ' ')                + colfintxt_z, #
    print renfintxt_z
    print reninitxt_z + colinitxt_z + ('-' * 115)
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

def imprifont(nombrefont_z):
  misfonts_z = {
    'CONDENSADO_ON'        : chr(15),
    'CONDENSADO_OFF'       : chr(18),
    'ON_LINE_EXPANDED_ON'  : chr(14),
    'ON_LINE_EXPANDED_OF'  : chr(20),
    'EMPHIZED_ON'          : chr(27)+chr(61),
    'EMPHIZED_OFF'         : chr(027)+chr(60),
    'SUBRAYADO_ON'         : chr(27)+'-1',
    'SUBRAYADO_OFF'        : chr(27)+'-0',
    'FORMFEED'             : '\f'
  }
 
  return (misfonts_z.get(nombrefont_z))
#End Def

node = dom.documentElement
version_z  = get_atrib(node, 'version')
if version_z == "-1":
    version_z  = get_atrib(node, 'Version')

#print "Version :", version_z
if version_z == "3.2":
   handleSlideshow(dom)

if version_z == "3.3":
   txtcfdi33(dom)

