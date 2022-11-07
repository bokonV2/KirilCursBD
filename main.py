from flask import Flask, render_template, request
from myUtilsDB import *


app = Flask(__name__)
sections = getSections()
superSections = getAllSupersections()

@app.context_processor
def inject_user():
    return dict(sections=sections, superSections=superSections)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/addSection', methods=['POST'])
def addSection():
    res = request.form
    if res.get('section_id') != '0':
        addNewSection(res.get('name'), res.get('section_id'))
    return render_template('admin.html')

@app.route('/admin/addItems', methods=['POST'])
def addItems():
    res = request.form
    print(res)
    addNewItem(
        res.get('name'),
        res.get('image'),
        res.get('count'),
        res.get('coast'),
        res.get('description'),
        res.get('section_id')
    )
    return render_template('admin.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def postLogin():
    res = request.form
    return render_template('login.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/register')
def registerGet():
    return render_template('register.html')

@app.route('/register', methods=['post'])
def registerPost():
    res = request.form
    return render_template('register.html')
    return render_template('index.html')

@app.route('/section/<int:id>')
def section(id):
    items = getAllItems(id)
    return render_template('section.html', items=items)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
