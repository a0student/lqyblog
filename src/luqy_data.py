from pypdf import PdfReader
import regex, glob, docx
import pandas as pd

def pdf2data(title, pdf_file):
    reader = PdfReader(pdf_file)

    content = ""
    for page in reader.pages:
        content += page.extract_text()

    pattern = regex.compile(r'\p{Han}\n\p{Han}')
    matches = regex.findall(pattern, content)
    for match in matches:
        new_str = match.replace("\n", "")
        content = content.replace(match, new_str)
    return content

def doc2data(doc_file):
    doc = docx.Document(doc_file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    content = '<br>'.join(fullText)
    content = content.replace("<br><br>", "<br>")
    content = content.replace("<br><br>", "<br>")
    content = content.replace("<br><br>", "<br>")
    pattern = regex.compile(r'\p{Han}<br>\p{Han}')
    matches = regex.findall(pattern, content)
    for match in matches:
        new_str = match.replace("<br>", "")
        content = content.replace(match, new_str)
    content = content.replace("<br>", "<br><br>")
    return content

def doc2df(doc_dir):
    file_list = glob.glob(f"{doc_dir}/*/*.docx")
    data_list = []
    for file in file_list:
        year, name = file.split("/")[-2:]
        date, title = name.split("-")[-2:]
        title = title.split(".")[0]
        publish_date = year + "-" + date[:2] + "-" + date[2:]
        content = doc2data(file)
        data_list.append((title, publish_date, content))
        print(title)
    columns = ["title", "publish_date", "content"]
    df_lecture = pd.DataFrame(data=data_list, columns=columns)
    df_lecture.to_pickle(f"{doc_dir}/latest_lecture.pkl")

doc_dir = "../doc"
doc2df(doc_dir)