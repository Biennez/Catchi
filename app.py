from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample user data (replace this with a database in a real application)
users = {'user1': 'password1', 'user2': 'password2', 'zymaun': 'zymaun'}

products = {
    '1': {'name': 'Product 1', 'price': 10.0},
    '2': {'name': 'Product 2', 'price': 20.0},
    '3': {'name': 'Product 3', 'price': 30.0},
    '4': {'name': 'Product 4', 'price': 40.0}
}

shops = {
    'shop1': {'name': 'Shop 1', 'image_url': '/static/1.jpg', 'products': {'1': {'name': 'Product A', 'price': 10.0}, '2': {'name': 'Product B', 'price': 20.0}}},
    'shop2': {'name': 'Shop 2', 'image_url': '/static/2.jpeg', 'products': {'3': {'name': 'Product C', 'price': 15.0}, '4': {'name': 'Product D', 'price': 25.0}}}
}


@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username, products=products)
    return 'You are not logged in | <a href="/login">Login</a>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))

        return 'Invalid username or password'

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            users[username] = password
            return redirect(url_for('login'))

        return 'Username already exists. Choose a different one.'

    return render_template('signup.html')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        product = products.get(product_id)

        if product:
            cart = session.get('cart', {})
            cart[product_id] = cart.get(product_id, 0) + quantity
            session['cart'] = cart

    cart_items = [
        {'product': products[product_id], 'quantity': quantity}
        for product_id, quantity in session.get('cart', {}).items()
    ]

    return render_template('cart.html', cart=cart_items)

@app.route('/shop/<shop_id>')
def shop(shop_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    shop_info = shops.get(shop_id)
    if not shop_info:
        return 'Shop not found'

    return render_template('dashboard.html', username=session['username'], shops=shops, shop_info=shop_info)


if __name__ == '__main__':
    app.run(debug=True)
