from estudo_caso.extrator_pdf import extrair_texto

text = extrair_texto("data/pdfs/Lei_14945_31072024.pdf")

print(text[:2000])