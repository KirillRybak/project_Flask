from flask import Flask , render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id



@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/info')
def info():
    articles = Article.query.order_by(Article.data.desc()).all()
    return render_template('info.html',articles=articles)


@app.route('/info/<int:id>')
def info_detal(id):
    article = Article.query.get(id)
    return render_template('info_detal.html',article=article)



@app.route('/info/<int:id>/del')
def info_del(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/info')
    except:
        return 'При удалении статьи возникла ошибка'


@app.route('/info/<int:id>/update')
def info_update(id):
    article = Article.query.order_by()
    return render_template('info_detal.html',article=article)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/info/<int:id>/create_update', methods=['POST','GET'])
def create_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/info')
        except:
            return 'При добавлении статьи произошла ошибка'

    else:
        article = Article.query.get(id)
        return render_template('update.html', article=article)


@app.route('/create_article', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title,intro=intro,text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/info')
        except:
            return 'При добавлении статьи произошла ошибка'

    else:
        return render_template('create_articles.html')


if __name__ == '__main__':
    app.run()