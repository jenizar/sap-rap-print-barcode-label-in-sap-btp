from markupsafe import Markup
import json
import urllib.request
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jinja2
import pdfkit
import os
import ast

app = Flask(__name__)
# Configuration
OUTPUT_FOLDER = 'HTML_LABEL'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/barcode', methods=['GET', 'POST'])
def show_element():
    data = request.get_json()   
    json_string = json.dumps(data)
    json_output = json.loads(json_string) 
    python_list = ast.literal_eval(json_output)
    print(type(python_list))
    print(python_list)    
    for item in python_list:  
        ebeln = item['ebeln']
        matnr = item['matnr']
        maktx = item['maktx']
        produ = item['produ']
        deliv = item['deliv']
        quant = item['quant']
        ldate = item['ldate']
        rfrom = item['rfrom']
        rdest = item['rdest'] 

    context = {
            'ebeln': ebeln,
            'matnr': matnr,
            'maktx': maktx,
            'produ': produ,
            'deliv': deliv,
            'quant': quant,
            'ldate': ldate,
            'rfrom': rfrom,
            'rdest': rdest,
        } 
    # Render template
    rendered_html = render_template('page.html', **context)  
    # Save to file
    filename = f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(OUTPUT_FOLDER, filename)      
    with open(filepath, 'w', encoding='utf-8') as f:
         f.write(rendered_html)
        
    return jsonify({
            'success': True,
            'message': 'HTML file generated successfully',
            'filename': filename,
            'path': os.path.abspath(filepath)
        })
    return render_template("index.html", data = json_output)
if __name__ == "__main__":
    app.run()
