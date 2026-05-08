import docx
import os

def read_docx(file_path):
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

filename = "Experiment-1_Creating Domain Specific Generalized Knowledge Graph(DS-GKG) for MITRE ATT&CK.docx"
if os.path.exists(filename):
    print(read_docx(filename))
else:
    print(f"File {filename} not found.")
