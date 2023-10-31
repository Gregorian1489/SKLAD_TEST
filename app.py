from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testDB.db'
db = SQLAlchemy(app)
app.app_context().push()


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Double, nullable=False)

    def __repr__(self):
        return '<Products %r>' % self.id


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_loc = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Location %r>' % self.id


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), default=0)
    quantity = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Inventory %r>' % self.product_id


@app.route('/')
def index():
    allproducts = Products.query.all()
    all_locations = Location.query.all()
    return render_template("index.html", allproducts=allproducts, all_locations=all_locations)


@app.route('/create_product', methods=['POST', 'GET'])
def create_product():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        product = Products(name=name, description=description, price=price)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении товара произошла ошибка"

    else:
        return render_template("/")


@app.route('/delete_product', methods=['POST', 'GET'])
def delete_product():
    if request.method == "POST":
        id = int(request.form['product_id'])
        product = Products.query.get_or_404(id)

        try:
            db.session.delete(product)
            db.session.commit()
            return redirect('/')
        except:
            return "При удалении произошла ошибка"


@app.route('/create_location', methods=['POST', 'GET'])
def create_location():
    if request.method == "POST":
        name_loc = request.form['name_loc']
        location = Location(name_loc=name_loc)

        try:
            db.session.add(location)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении локации произошла ошибка"

    else:
        return render_template("/")


# @app.route('/')
# def products_show():
#     products_show = Products.query(Products.name).all()
#     return render_template("index.html", products_show=products_show)

if __name__ == "__main__":
    app.run(debug=True)
