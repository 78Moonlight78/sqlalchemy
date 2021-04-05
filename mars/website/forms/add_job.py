from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('id главного', validators=[DataRequired()])
    work_size = StringField('Объём работ', validators=[DataRequired()])
    collaborators = StringField('Работники', validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена?')

    submit = SubmitField('Отправить')
