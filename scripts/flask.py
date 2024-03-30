from flask import Flask  
import os
app = Flask(__name__)  
  
@app.route('/')  
def hello_world():  
    os.system(f"python self_explorer.py --app didi --root_dir ../")
    return 'Hello, World!'  

if __name__ == '__main__':  
    app.run()