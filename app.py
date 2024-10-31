from flask import Flask, request, render_template, redirect, url_for
from models import db, Product, Price

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:eWbcsVjtfEMfledXaccIgQkeCpDlbwGJ@postgres.railway.internal:5432/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    for product in products:
        # Calcular os preços associados ao produto
        prices = Price.query.filter_by(product_id=product.id).order_by(Price.date).all()
        product.prices = prices  # Adiciona os preços ao objeto do produto
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        barcode = request.form['barcode']
        new_product = Product(name=name, barcode=barcode)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/add_price/<int:product_id>', methods=['POST'])
def add_price(product_id):
    price_value = request.form['price']
    new_price = Price(price=float(price_value), product_id=product_id)
    db.session.add(new_price)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    prices = Price.query.filter_by(product_id=product_id).all()
    lowest_price = min([p.price for p in prices], default=None)
    last_price = prices[-1].price if prices else None
    return render_template('index.html', product=product, lowest_price=lowest_price, last_price=last_price)

if __name__ == '__main__':
    # with app.app_context():
    #      db.drop_all()  # Cuidado: isso remove todas as tabelas e dados
    #      db.create_all()  # Cria as tabelas novamente
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
