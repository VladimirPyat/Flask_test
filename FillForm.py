from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired


class FillF(FlaskForm):
    max_score = 10
    h_name = []
    g_name = []
    

    with open('_tour.txt', 'r', encoding='utf-8') as file:
                data = ' '.join(file.readlines())
    data_split = data.split()
    round_num = (data_split[0])
    data_split.pop()
    data_split.pop(0)
    data_split.pop(0)

    for i in data_split:
        h_name.append (i.split(':')[0])
        g_name.append (i.split(':')[1])


    h_fields0 = IntegerField(h_name[0], validators=[DataRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields0 = IntegerField(g_name[0], validators=[DataRequired(), validators.NumberRange(min=0, max=max_score)])
    

    submit = SubmitField("Отправить")
    