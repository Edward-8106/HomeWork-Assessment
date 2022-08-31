from multiprocessing import connection
from xml.dom.minidom import Document
from flask import Flask, render_template, request , redirect, url_for
from datetime import datetime
from tkinter import S
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Docs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    family_names = db.Column(db.String(200), nullable=False)
    contacts = db.Column(db.Integer, nullable=True)
    idnumber = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    address1 = db.Column(db.String(200), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    date_saved = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        name = request.form['name']
        family_names = request.form['family_names']
        contacts = request.form['contacts']
        idnumber = request.form['idnumber']
        address = request.form['address']
        address1 = request.form['address1']
        postal_code = request.form['postal_code']
        sum = request.form['sum']
        new_document = Docs(name=name, family_names=family_names, contacts=contacts, idnumber=idnumber, address=address, address1=address1, postal_code=postal_code , sum=sum)

        try:
            db.session.add(new_document)
            db.session.commit()
            return redirect('/')
        except:
            return "THE WAS A PROBLEM SAVING YOU'RE DOCUMENT PLEASE TRY AGAIN LATER!"

        
    else:
        documents = Docs.query.order_by(Docs.date_saved).all()
        return render_template('homepage.html', documents=documents)


@app.route('/delete/<int:id>')
def delete(id):
    doc_to_delete = Docs.query.get_or_404(id)

    try:
        db.session.delete(doc_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


if __name__ == "__main__":
    app.run(debug=True)
        
