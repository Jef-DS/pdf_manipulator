from PyPDF4 import PdfFileReader, PdfFileWriter
from io import BytesIO
def parse_range(range_string):
    page_list_step1 = [num.strip() for num in range_string.split(',')]
    page_list_step2 = []
    for item in page_list_step1:
        if '-' in item:
            (begin, end) = item.split('-')
            for page in range(int(begin), int(end)+1):
                page_list_step2.append(page)
        else:
            page_list_step2.append(int(item));
    return page_list_step2

def merge_files(file_list):
    writer = PdfFileWriter()
    output_buffer = BytesIO()
    for file_item in file_list:
        filename, rangestring = file_item
        pages = parse_range(rangestring)
        with  open(filename, "rb") as filereader:
            reader = PdfFileReader(filereader)
            for page in pages:
                writer.addPage(reader.getPage(page))
            writer.write(output_buffer)
    return output_buffer
    
if __name__ == '__main__':
    files = [('samples/file1_2021_04_06.pdf','0-1'),
             ('samples/file2_2021_05_06.pdf','0,5add')]
    buffer = merge_files(files);
    with open('samples/output.pdf', 'wb') as f:
        f.write(buffer.getbuffer())