#--> Archivo que convierte el texto para la Impresora a un pdf
# --> Daniel Ricardo Basto Rivero
# -------------------------------------------

import itertools
import sys
from random import randint
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_pdf(archin, archout):
    c = canvas.Canvas(archout+".pdf", pagesize=letter)
    width, height = letter
    max_rows_per_page = 66
    anchocar_z = 4;
    anchonormal_z = 4;
    anchoconden_z = 2
    anchodoble_z = 5;
    # Margin.
    x_offset = 20
    y_offset = 20
    xini_z = 0;
    yini_z = 0;
    xfin_z = 0;
    yfin_z = 0;
    # Space between rows.
    padding = 10;
    numlin_z = 0;
    xx_z = height - x_offset;
    yy_z = y_offset;
    carini_z = 0;
    carfin_z = 0;
    c.setFont("Courier", 9);
    #c.setFont("Courier-Bold", 9)
    underline_z = 0;
    condensed_z = 0;
    doubled_z	= 0;
    micar_z = "";
    auxi_z = "";

    miformato_z = open(archin, "r")
    linformato_z = miformato_z.readlines()
    for linea_z in linformato_z:
       linea_z = linea_z.strip('\n\r')
       carini_z = 0;
       carfin_z = len(linea_z);
       xx_z = height - (numlin_z * padding) - x_offset
       yy_z = y_offset
       xini_z = xx_z;
       yini_z = yy_z;
       yinisub_z = yini_z;
       yfinsub_z = xini_z;
       numlin_z = numlin_z + 1;
       
       while carini_z < carfin_z:
          micar_z = linea_z[carini_z:carini_z + 1];

          if(ord(micar_z ) == 12):
            c.showPage();
            xx_z = height - x_offset;
            yy_z = y_offset;
            xini_z = xx_z;
            yini_z = yy_z;
            numlin_z = 1;
            if condensed_z ==  1:
              anchocar_z = anchoconden_z;
              c.setFont("Courier", 6);
            else:
              anchocar_z = anchonormal_z;
              c.setFont("Courier", 9);
            #End If
            carini_z = carini_z;
          #End if
          if(ord(micar_z ) == 15):
            condensed_z = 1;
            anchocar_z = anchoconden_z;
            c.setFont("Courier", 6);
            carini_z = carini_z;
          #End if
          if(ord(micar_z ) == 18):
            condensed_z = 0;
            anchocar_z = anchonormal_z;
            c.setFont("Courier", 9);
            carini_z = carini_z;
          #End if
          if(ord(micar_z ) == 14):
            doubled_z = 1;
            anchocar_z = anchodoble_z;
            c.setFont("Courier", 12);
            carini_z = carini_z;
          #End if
          if(ord(micar_z ) == 20):
            doubled_z = 0;
            anchocar_z = anchonormal_z;
            c.setFont("Courier", 9);
            carini_z = carini_z;
          #End if
          if(ord(micar_z ) == 27):
            auxi_z =  linea_z[carini_z+1:carini_z+3];
            if auxi_z == "-1":
              underline_z = 1;
              carini_z = carini_z + 2;
              yinisub_z = yini_z;
            #End if

            if auxi_z == "-0":
              underline_z = 0;
              carini_z = carini_z + 2;
              yfinsub_z = yini_z;
              c.line(yinisub_z, xini_z-2, yfinsub_z, xini_z-2);
            #End if
          #End if
                    
         
          if(numlin_z > max_rows_per_page):
            c.showPage()
            numlin_z = 0;
            if condensed_z ==  1:
              anchocar_z = anchoconden_z;
              c.setFont("Courier", 6);
            else:
              anchocar_z = anchonormal_z;
              c.setFont("Courier", 9);
            #End If
 
          #End if

          if ord(micar_z) > 30:
            xx_z = xini_z;
            yy_z = yini_z;
            c.drawString(yy_z, xx_z, micar_z);
            yini_z = yini_z + anchocar_z + 2;
          #End if
           
          carini_z = carini_z + 1;
       #End while

    #End For
    c.showPage()
    c.save()


archin = sys.argv[1]
archout = sys.argv[2]
export_to_pdf(archin, archout)
