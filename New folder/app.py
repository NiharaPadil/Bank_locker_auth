# # app.py

# from flask import Flask, render_template
# from Bank_locker_auth.main import some_function_from_main
# from Bank_locker_auth.AddToDatabase import some_function_from_AddToDatabase
# from Bank_locker_auth.EncodeGenerator import some_function_from_EncodeGenerator


# app = Flask(__name__)

# @app.route('/')
# def index():

#     return render_template('index.html')
# def styles():
#     return render_template('styles.css')
# def script():
#     return render_template('script.js')


from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authorize', methods=['POST'])
def authorize():
    os.system('python main.py')
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9550)

