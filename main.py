import time
import os
import google.generativeai as genai

from PIL import Image

import pypdfium2 as pdfium
import markdown

def read_images(path):
    # If it is .pdf, convert it to images
    if path.endswith('.pdf'):
        images = []
        pdf = pdfium.PdfDocument(path)
        for i in range(len(pdf)):
            page = pdf[i]
            image = page.render(scale=4).to_pil()
            images.append(image)
        return images
    else:
        # Otherwise assume its a directory of images
        images = []
        for file in os.listdir(path):
            image = Image.open(f'{path}/{file}')
            images.append(image)
        return images

GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-1.5-flash')

path = input('Enter the PDF path or directory of images: ')

prompt = '''
Please perform OCR on the attached image containing mathematical content. Convert all text to markdown format, ensuring that every piece of mathematical content is represented using LaTeX within `$...$` delimiters. Do not use HTML, Unicode characters, or any other formatting—only LaTeX for all mathematical expressions.
For example:
* Fractions should be written as `$\\frac{a}{b}$`.
* Integrals should appear as `$\\int_a^b f(x) \\, dx$`.
* Any superscripts or subscripts should be formatted using LaTeX, such as `$x^2$` or `$a_i$`.
If you encounter any graphs or diagrams, please provide a detailed description of the content in text form in the form `[diagram: <description>]`.
Contents pages should be formatted without any dotted lines. List the page number directly after the title. For example:
```
# Contents

1. Introduction: 1
2. Methods: 3
3. Results: 5

```
Your output should strictly adhere to these guidelines, focusing only on the textual and mathematical content, with all mathematical elements formatted exclusively using LaTeX. Graphs and diagrams should be replaced with a detailed description.
'''

total_result_text = ''

last_image = None
last_response = None
for image in read_images(path):
    parts = [{'role': 'user', 'parts': [prompt]}]
    if last_image:
        parts.append({'role': 'user', 'parts': [last_image]})
        parts.append({'role': 'model', 'parts': [last_response]})
    parts.append({'role': 'user', 'parts': [image]})
    do_continue = True
    while do_continue:
        try:
            result = model.generate_content(parts, generation_config={'temperature': 0.1})
            print(result)
            result_text = result.text
            print(result_text)
        except Exception as e:
            print('Retrying...', e)
            time.sleep(15)
            continue
        time.sleep(5)
        do_continue = False
    total_result_text += result_text.strip() + '\n'
    last_image = image
    last_response = result_text.strip()

result_html = markdown.markdown(total_result_text, extensions=['extra', 'tables'])

with open('template.html', 'r') as f:
    template = f.read()
result = template.replace('${text}', result_html)

with open(f'{path}.html', 'w', encoding='UTF-8') as f:
    f.write(result)
