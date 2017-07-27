from flask import Flask, render_template, request
from sqlalchemy import create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import pandas as pd

app = Flask(__name__)
db_string = "postgres://postgres:postgres@localhost:5433/advertisement"
db = create_engine(db_string)
base = declarative_base()


class Company(base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))


class Category(base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String)
    rel = relationship('Company', backref='owner', lazy='dynamic')


#Company.__table__.drop(db)
#Category.__table__.drop(db)

Session = sessionmaker(db)
session = Session()
#base.metadata.create_all(db)

file_name = 'category.csv'
df = pd.read_csv(file_name)
#df.to_sql(con=db, index_label='id', name=Category.__tablename__, if_exists='append')


@app.route('/')
def index():
    #return "<h1>Connection established successfully</h1>"
    return render_template('index.html')


@app.route('/add_company')
def add_company():
    return render_template('add_company.html')


@app.route('/get_company_list')
def get_company_data():
    query = session.query(Company).all()
    return render_template('company_list.html', rows=query)


@app.route('/post_company_data', methods=['POST'])
def post_company_data():
    fk_id=-1
    for row in session.query(Category).filter(Category.category==request.form['category']):
        fk_id = row.id
    if fk_id > -1:
        company = Company(name=request.form['name'], category=request.form['category'], address=request.form['address'], email=request.form['email'], category_id=fk_id)
        session.add(company)
        session.commit()
        #return jsonify({'message': "Data inserted successfully!"})
        return render_template('message.html', data="Data inserted succesfully")
    else:
        return render_template('message.html', data="Incorrect data. Insertion failed")
        #return jsonify({'message': "Incorrect data. Insertion failed."})


if __name__ == "__main__": app.run()
