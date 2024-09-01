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
Please perform OCR on the attached image containing mathematical content. Convert all text to plain text format, ensuring that every piece of mathematical content is represented using LaTeX within `$...$` delimiters. Do not use HTML, Unicode characters, or any other formatting—only LaTeX for all mathematical expressions.
For example:
* Fractions should be written as `$\\frac{a}{b}$`.
* Integrals should appear as `$\\int_a^b f(x) \\, dx$`.
* Any superscripts or subscripts should be formatted using LaTeX, such as `$x^2$` or `$a_i$`.
If you encounter any graphs or diagrams, attempt to draw a rough sketch using simple SVG. For each graph, generate a detailed caption that describes the graph's content and purpose, and include this caption as alt text within the SVG. For example:
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" role="img" aria-label="A graph of a parabola opening upwards. The parabola passes through the points (-2, 4), (0, 0), and (2, 4).">
    <g aria-hidden="true">
        <line x1="150" y1="0" x2="150" y2="300" stroke="black" stroke-width="2"/>
        <line x1="0" y1="150" x2="300" y2="150" stroke="black" stroke-width="2"/>

        <path d="M 50 150 Q 150 50 250 150" stroke="blue" stroke-width="2" fill="none"/>

        <text x="135" y="165" font-family="Arial" font-size="12" fill="black">-5</text>
        <text x="105" y="165" font-family="Arial" font-size="12" fill="black">-4</text>
        <text x="75" y="165" font-family="Arial" font-size="12" fill="black">-3</text>
        <text x="45" y="165" font-family="Arial" font-size="12" fill="black">-2</text>
        <text x="15" y="165" font-family="Arial" font-size="12" fill="black">-1</text>
        <text x="165" y="165" font-family="Arial" font-size="12" fill="black">1</text>
        <text x="195" y="165" font-family="Arial" font-size="12" fill="black">2</text>
        <text x="225" y="165" font-family="Arial" font-size="12" fill="black">3</text>
        <text x="255" y="165" font-family="Arial" font-size="12" fill="black">4</text>
        <text x="285" y="165" font-family="Arial" font-size="12" fill="black">5</text>

        <text x="155" y="135" font-family="Arial" font-size="12" fill="black">5</text>
        <text x="155" y="105" font-family="Arial" font-size="12" fill="black">4</text>
        <text x="155" y="75" font-family="Arial" font-size="12" fill="black">3</text>
        <text x="155" y="45" font-family="Arial" font-size="12" fill="black">2</text>
        <text x="155" y="15" font-family="Arial" font-size="12" fill="black">1</text>
        <text x="155" y="165" font-family="Arial" font-size="12" fill="black">0</text>
        <text x="155" y="195" font-family="Arial" font-size="12" fill="black">-1</text>
        <text x="155" y="225" font-family="Arial" font-size="12" fill="black">-2</text>
        <text x="155" y="255" font-family="Arial" font-size="12" fill="black">-3</text>
        <text x="155" y="285" font-family="Arial" font-size="12" fill="black">-4</text>
    </g>
</svg>
If generating a sketch is not possible, insert the placeholder `[Graph/Diagram]` and provide the detailed caption separately.
Your output should strictly adhere to these guidelines, focusing only on the textual and mathematical content, with all mathematical elements formatted exclusively using LaTeX. Graphs and diagrams should be represented with rough SVG sketches accompanied by descriptive alt text.
'''

result_text = ''

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
            result = model.generate_content(parts, generation_config={'temperature': 0, 'response_mime_type': 'text/plain'})
        except e:
            print('Retrying...', e)
            time.sleep(15)
            continue
        time.sleep(5)
        do_continue = False
    print(result)
    print(result.text)
    result_text += result.text.strip() + '\n'
    last_image = image
    last_response = result.text.strip()

result_html = markdown.markdown(result_text, extensions=['extra', 'tables'])

with open('template.html', 'r') as f:
    template = f.read()
result = template.replace('${text}', result_html)

with open(f'{path}.html', 'w', encoding='UTF-8') as f:
    f.write(result)
