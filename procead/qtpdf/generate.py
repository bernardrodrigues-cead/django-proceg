from jinja2 import Environment, FileSystemLoader

import pdfkit

def generate_pdf(
        template_path,
        template_dir,
        media_dir,
        template_context,
        page_size="A4",
        page_orientation="Portrait"):

    #we use an array to pass the result asynchronously
    ob = []
    
    jinja_env = Environment(loader=FileSystemLoader(template_dir))

    template_context['media_dir'] = media_dir
    template = jinja_env.get_template(template_path)
    html = template.render(**template_context)
    
    options = {
        'page-size': page_size,
        'orientation': page_orientation,
        'margin-top': '0.25in',
        'margin-bottom': '0.80in',
        'margin-right': '0.30in',
        'margin-left': '0.30in',
        'encoding': "UTF-8",
        'enable-local-file-access': "",
    }
    
    WKHTMLTOPDF_PATH = '/usr/local/bin/wkhtmltopdf'

    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    pdf = pdfkit.from_string(html, options=options, configuration=config)
    
    return pdf