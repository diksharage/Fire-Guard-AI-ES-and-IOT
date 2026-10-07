import codecs
import re

file_path = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\pages\VirtualCircuit.jsx"

with codecs.open(file_path, 'r', 'utf-8') as f:
    content = f.read()

content = content.replace("\\'", "'")

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(content)
