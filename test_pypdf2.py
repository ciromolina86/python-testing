import PyPDF2

def read_pdf(path='PDFs/demo.pdf'):
    with open(path, 'rb') as f:
        pdf_reader = PyPDF2.PdfFileReader(f)

        # for num in range(pdf_reader.numPages):
        #     page = pdf_reader.getPage(num)
        #     print(type(page))
        #     pageText = page.extractText()
        #     print(pageText)

        return pdf_reader.getPage(0)

def write_pdf(path='PDFs/test_pdf.pdf'):
    with open(path, 'wb') as f:
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(read_pdf())

        pdf_writer.write(f)


# def merge_pdf(path='PDFs/test_pdf.pdf'):
#     with open(path, 'wb') as f:
#         pdf_writer = PyPDF2.PdfFileMerger()
#         pdf_writer.append(fileobj=f)
#
#         # pdf_writer.write(f)


merge_pdf()
