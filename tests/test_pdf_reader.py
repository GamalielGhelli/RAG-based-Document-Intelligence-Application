from estudo_caso.extrator_pdf import extrair_texto

texto = extrair_texto("data/pdfs/Lei_14945_31072024.pdf")

print(texto[:2000])