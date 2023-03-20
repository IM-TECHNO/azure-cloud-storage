import os
from flask import Flask, request, redirect, url_for, render_template
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = Flask(__name__)

blob_service_client = BlobServiceClient.from_connection_string("<connection string>")

container_client = blob_service_client.get_container_client("<container name>")

app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            return redirect(url_for('upload_file'))
        else:
            return redirect(url_for('login_error'))

    return render_template('login.html')



@app.route('/dashboard', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(file.read())
        
        return redirect(url_for('uploaded_file', filename=filename))
    return '''
        <!doctype html>
        <html>
            <body>
                <style>
                    body{
                        font-family: 'Poppins', sans-serif;
                        background-color:#f2f2f2;
                        height: 100vh;
                        width:100vw ;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 1.2rem;
                    }
                    h3{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content:center;      
                 }
                    form {
                      margin: 0 auto;
                      width: 400px;
                      padding: 50px;
                    }
                    input{
                      width: 100%;
                      padding: 0.5em;
                      border: 1px solid #CCC;
                      border-radius: 0.3em;
                      margin: 0.5em 0;
                      font-family: 'Poppins', sans-serif;
                      font-size: 1rem;
                    }
                    #file{
                      width: 100%;
                      padding: 0.5em;
                      border: 1px solid #CCC;
                      border-radius: 0.3em;
                      margin: 0.5em 0;
                      background-color: #17e364;
                      font-family: 'Poppins', sans-serif;
                      
                      
                    }
                    button:hover{
                      background-color: #f2f2f2;
                    }
                    clrs{
                        background-color: #17e364;
                    }
                  </style>
                
                
                <form method=post enctype=multipart/form-data>
                    <h3>Azure File Storage</h3>
                    <div class="clrs">
                    <input type=file name=file id="file">
                    <input type=submit value=Upload id="sum">
                    </div>
                </form>
            </body>
        </html>
    '''

@app.route('/login-error')
def login_error():
    return render_template('login-error.html')

@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_client.container_name}/{filename}"
    return f'''
        <!doctype html>
        <html>
        <head>
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
            </head>
            <body>
                <style>
                    body{{
                        font-family: 'Poppins', sans-serif;
                        background-color:#90988c;
                        height: 100vh;
                        width:100vw ;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    h1{{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content:center;
                    }}
                    .a{{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content:center;
                    }}
                </style>
                <div class="a">
                <h1>File {filename} uploaded successfully to Azure Blob Storage.</h1>
                <br>
                <button><a href="{url}">URL to File</a></button>
                </div>
            </body>
        </html>
    '''
if __name__ == '__main__':
    app.run(debug=True)