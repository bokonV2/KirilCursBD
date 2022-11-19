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
    orders = getAllOrders()
    users = getAllUsers()
    return render_template('admin.html', orders=orders, users=users)

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
    if session['user']:
        products, fullPrice = getAllCart(session['user']['id'])
    else:
        products = None
        fullPrice = 0 
    return render_template('cart.html', products=products, fullPrice=fullPrice)

@app.route('/cart/addItem/<int:item_id>/<int:id>')
def addItemToCart(item_id, id):
    if session['user']:
        addItemTocart(session['user']['id'], item_id)
    return redirect(f'/section/{id}')

@app.route('/cart/removeItem/<int:item_index>')
def removeItemFromCart(item_index):
    if session['user']:
        removeItemCart(session['user']['id'], item_index)
    return redirect('/cart')

@app.route('/cart/submit/<int:fullPrice>', methods=['POST'])
def postCartSubmit(fullPrice):
    res = request.form
    if session['user']:
        order = cartSubmit(session['user']['id'], fullPrice, res.get('addres'))
    return redirect(f'/orders/{order.id}')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def postLogin():
    res = request.form
    user = userLogin(res.get('number'), res.get('password'))
    if user:
        session['user'] = user
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/orders/<int:id>')
def orders(id):
    order = getOrder(id)
    return render_template('orders.html', order=order)

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
    return redirect('/')

@app.route('/section/<int:id>')
def section(id):
    items = getAllItems(id)
    return render_template('section.html', items=items, id=id)

@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
