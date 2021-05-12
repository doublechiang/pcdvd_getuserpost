import logging
from flask import Flask, render_template, request, url_for, Response
from io import BytesIO    

# Local import
from pcdvd_forum import PcdvdForum

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route('/', methods=['get', 'post'])
def getUserPost():
    if request.method == 'POST':
        user=request.form.get('username')
        thread=request.form.get('thread')
        logging.info(user, thread)
        pcdvd = PcdvdForum()
        # pcdvd.getUserPostByThread(thread, user)
        # buf = BytesIO()
        # for p in html_doc:
        #     buf.write(p.encode('utf-8'))
        return Response(pcdvd.getUserPostByThread(thread, user))
        
    return render_template('main.html')

if __name__ == '__main__':
    app.run(port=5000)