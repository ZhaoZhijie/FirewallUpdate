from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(24)

PASSWORD_FILE = 'password.txt'
PORT = 6789

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        with open(PASSWORD_FILE, 'r') as f:
            correct_password = f.read().strip()

        user_password = request.form['password']

        if user_password == correct_password:
            ip_address = request.remote_addr
            rulestr = f'sudo ufw allow from {ip_address} to any port {PORT}'

            try:
                result = subprocess.run(rulestr.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                print(f"Command output: {result.stdout.decode('utf-8')}")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e.stderr.decode('utf-8')}")

            flash('地址更新成功', 'success')
        else:
            flash('密码不正确', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)