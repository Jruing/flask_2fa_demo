import base64
import io
from flask import Flask, render_template,request
import pyotp
import qrcode
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "cf57246e0a8cd0eb"
app.template_folder = "templates"
CORS(app)

data = {
    "username":"admin",
    "password":"admin",
    "secret":"IM6YOMCQSOFLQLEGX3W5UEGGATZSDFKN"
}
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    body = request.get_json()
    username = body["username"]
    password = body["password"]
    secret = pyotp.random_base32()
    # secret = "123123"
    totp = pyotp.TOTP(secret)
    print(totp.now())
    otpauth_url = totp.provisioning_uri(name=username, issuer_name="2FA Authentication") 
    print(otpauth_url)  
    # 生成二维码
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(otpauth_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 返回 PNG 二进制
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    img_bytes = buf.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    print({
        "username":username,
        "password":password,
        "secret":secret
    })
    img_data_uri = f"data:image/png;base64,{img_base64}"
    return {"status":0,"msg":"注册成功","qrcode":img_data_uri}

@app.route('/login',methods=['POST'])
def login():
    body = request.get_json()
    username = body["username"]
    password = body["password"]
    code = body["code"]
    if username == data["username"] and password == data["password"]:
        totp = pyotp.TOTP(data["secret"])
        if totp.verify(code,valid_window=1):
            return {"status":0,"msg":"登录成功"}
        else:
            return {"status":1,"msg":"登录失败"}
    else:
        return {"status":1,"msg":"登录失败"}

if __name__ == "__main__":
    app.run(debug=True)
