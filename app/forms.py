from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_query = StringField("Search Query: ",validators=[DataRequired()])
    search = SubmitField("Submit")
    