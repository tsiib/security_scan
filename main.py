#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import time
import flask
from PyPDF2 import PdfFileMerger
from flask import Flask, render_template, request, logging, url_for
# from flask_socketio import SocketIO
from docfile import PDF
import pdfkit

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


# socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/was")
def was():
    return render_template("was.html")


# @socketio.on('result')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#    print('received my event: ' + str(json))
#    socketio.emit('my response', json, callback=messageReceived)

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/result", methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        url = request.form.get('url')
        print('started executing command ...')

        def inner():
            res = ['python2', 'rapidscan.py', url]

            a = subprocess.Popen(res, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 )
            # stdout, stderr = a.communicate()


            with a.stdout:
                for line in iter(a.stdout.readline, b""):
                    line = str(line, 'utf-8')
                    line2 = line.encode('latin-1', 'replace').decode('latin-1')
                    sys.stdout.flush()
                    # pdf.write(5, str(line2))
                    # pdf.ln()
                    time.sleep(1)

                    yield line2.strip() + "\n"

                    pdf = PDF()
                    pdf.alias_nb_pages()
                    pdf.add_page()
                    pdf.set_font("Arial", size=10)

                    if line2.startswith("_") is True:
                        pdf.write(5, str(line2))
                        #pdf.multi_cell(10, 5, str(line2), 0, 1)
                        pdf.ln()

                    pdf.output("summary.pdf", "F")

                #elif line2.startswith(".") is False:
                #pdf.write(5, str(line2))
                #    pdf.multi_cell(10, 5, str(line2), 0, 1)
                #pdf.ln()
                #pdf.output("scan_detail.pdf", "F")

            #pdfs = ['scan_cover.pdf', 'summary.pdf', 'scan_detail.pdf']
            #merger = PdfFileMerger()

            #for pdf in pdfs:
             #   merger.append(pdf)

            #merger.write("Report0.pdf")
            #merger.close()

        # return flask.Response(inner(), mimetype='text/html')

        return flask.render_template("handle_data.html", response=inner(), language='Python', framework='Flask')
        # env = Environment(loader=FileSystemLoader('templates'))
        # tmp1 = env.get_template('handle_data.html')
        # css_url = url_for('static', filename='css/template.css')
        # was_url = url_for(filename='was.html')
        # waf_url = url_for(filename='waf.html')
        # handle_url = url_for(filename='handle_data.html')
        # return flask.Response(tmp1.generate(response=inner()), mimetype='text/html')

        # return flask.Response(tmp1.generate(response=response if response is None else response()))


@app.route("/waf")
def waf():
    return render_template("waf.html")


if __name__ == "__main__":
    try:
        app.run(debug=True)

    except Exception as e:
        logging.fatal(e, exc_info=True)
