from flask import Flask, render_template, request, session, redirect
from myUtilsDB import *


app = Flask(__name__)
app.secret_key = "qwe213waf544yre4y6s4i6i"
sections = getSections()
superSections = getAllSupersections()
# session['user'] = None

@app.context_processor
def inject_user():
    user = session.get('user')
    if user:
        cartLen = getCartLen(user['id'])
    else:
        
        cartLen = ""
    return dict(
        sections = sections, 
        superSections = superSections, 
        user = user,
        cartLen = cartLen
    )

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
    products, fullPrice = getAllCart(session['user']['id'])
    return render_template('cart.html', products=products, fullPrice=fullPrice)

@app.route('/cart/addItem/<int:item_id>/<int:id>')
def addItemToCart(item_id, id):
    addItemTocart(session['user']['id'], item_id)
    return redirect(f'/section/{id}')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def postLogin():
    res = request.form
    user = userLogin(res.get('number'), res.get('password'))
    session['user'] = user
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
    registerNewUser(
        res.get('name'), 
        res.get('lastName'), 
        res.get('number'), 
        res.get('mail'), 
        res.get('password')
    )
    user = userLogin(res.get('number'), res.get('password'))
    session['user'] = user
    return render_template('orders.html')
    return render_template('register.html')

@app.route('/section/<int:id>')
def section(id):
    items = getAllItems(id)
    return render_template('section.html', items=items, id=id)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
