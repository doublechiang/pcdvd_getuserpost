import logging
from flask import Flask, render_template, request, url_for, send_file
from io import BytesIO    

# Local import
from pcdvd_forum import PcdvdForum

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/', methods=['get', 'post'])
def getUserPost():
    if request.method == 'POST':
        user=request.form.get('username')
        thread=request.form.get('thread')
        logging.info(user, thread)
        html_doc = PcdvdForum().getUserPostByThread(thread, user)
        buf = BytesIO()
        for p in html_doc:
            buf.write(p.encode('utf-8'))
        
        buf.seek(0)
        return send_file(buf, as_attachment=True, attachment_filename='pcdvd.html', mimetype='text/html')

    return  render_template('main.html')

if __name__ == '__main__':
    app.run(port=5000)