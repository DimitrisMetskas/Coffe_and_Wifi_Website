from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_ckeditor import CKEditor
from forms import CreatePostForm
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class CoffePost(db.Model):
    __tablename__ = "cafe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[int] = mapped_column(Integer, nullable=False)
    has_toilet: Mapped[int] = mapped_column(Integer, nullable=False)
    has_wifi: Mapped[int] = mapped_column(Integer, nullable=False)
    can_take_calls: Mapped[int] = mapped_column(Integer, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[float] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(CoffePost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/ourcoffeshops')
def get_all_coffe_shops():
    result = db.session.execute(db.select(CoffePost))
    posts = result.scalars().all()
    return render_template("ourcoffeshops.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = db.get_or_404(CoffePost, post_id)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = CoffePost(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(CoffePost, post_id)
    edit_form = CreatePostForm(
            name=post.name,
            map_url=post.map_url,
            img_url=post.img_url,
            location=post.location,
            has_sockets=post.has_sockets,
            has_toilet=post.has_toilet,
            has_wifi=post.has_wifi,
            can_take_calls=post.can_take_calls,
            seats=post.seats,
            coffee_price=post.coffee_price
        )
    if edit_form.validate_on_submit():
        post.name = edit_form.name.data
        post.map_url = edit_form.map_url.data
        post.img_url = edit_form.img_url.data
        post.location = edit_form.location.data
        post.has_sockets = edit_form.has_sockets.data
        post.has_toilet = edit_form.has_toilet.data
        post.has_wifi = edit_form.has_wifi.data
        post.can_take_calls = edit_form.can_take_calls.data
        post.seats = edit_form.seats.data
        post.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<post_id>")
def delete_post(post_id):
    requested_post = db.get_or_404(CoffePost, post_id)
    db.session.delete(requested_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
