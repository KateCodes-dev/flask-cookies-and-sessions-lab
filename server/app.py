
from flask import Flask, make_response, session
from flask_migrate import Migrate
from models import db, Article, ArticleSchema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/clear_session')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200


@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(article) for article in Article.query.all()]
    return make_response(articles, 200)


@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] > 3:
        return {'message': 'Maximum pageview limit reached'}, 401

    article = Article.query.filter_by(id=id).first()

    if article is None:
        return {'message': 'Article not found'}, 404

    return make_response(ArticleSchema().dump(article), 200)


if __name__ == '__main__':
    app.run(port=5555)
