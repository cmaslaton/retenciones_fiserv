import fitz
import re

regex = r'[\d.]+,[\d]{2}[+-]?'


def iibb(dir_pdf):

    doc=fitz.open(dir_pdf)
    suma_iibb = 0
    for _ in range(doc.page_count):
        page = doc[_]
        words = page.get_text_blocks("words")
        g = [tupla for tupla in words if "SIRTAC" in tupla[4]]
        for i in range(len(g)):
            num = re.findall(regex, g[i][4])[0]
            if num[-1:] == '-':
                num = num[-1:] + num[:-1]
            suma_iibb += float(num.replace('.','').replace(',','.'))
    return suma_iibb
