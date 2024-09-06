from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/zeyne/pythonExercise/ORM-Sqlite-Flask/todo.db"

db = SQLAlchemy(app)    #Flask uygulama nesnesi SQLAlchemy'ye geçirilir ve bu sayede SQLAlchemy, Flask uygulaması ile entegre olur. Bu entegrasyon, veritabanı bağlantılarını, oturumları ve diğer ORM işlevlerini Flask uygulaması ile birlikte kullanmanızı sağlar.

@app.route("/")
def index():
    todos=Todo.query.all()    #veritabanındaki bütün todo lar gelecek
    return render_template("index.html" , todos=todos)

@app.route("/add", methods=['POST'])
def add():
    title=request.form.get('title')
    newTodo=Todo(title=title, complate=False ) 
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complate/<string:id>")
def complate(id):
    todo=Todo.query.filter_by(id=id).first()
    todo.complate = not todo.complate
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    complate=db.Column(db.Boolean) 

if __name__=="__main__":
    with app.app_context():
        db.create_all()         #zaten oluşturulmuş tabloları create_all tekrar oluşturmuyor, bundan uygulama her çalıştığında çalışan bu yere koyabiliriz
    app.run(debug=True)