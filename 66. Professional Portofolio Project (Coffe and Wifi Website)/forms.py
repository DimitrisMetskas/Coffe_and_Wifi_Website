from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    name = StringField("Coffee Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = StringField("has sockets", validators=[DataRequired()])
    has_toilet = StringField("has toilet", validators=[DataRequired()])
    has_wifi = StringField("has wifi", validators=[DataRequired()])
    can_take_calls = StringField("can take calls", validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    body = CKEditorField("Content")
    submit = SubmitField("Submit Post")
