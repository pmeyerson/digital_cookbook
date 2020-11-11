from flask_wtf import FlaskForm
from wtforms import (
    TextField,
    IntegerField,
    SubmitField,
    DecimalField,
    SelectField,
    FormField,
)


class MeasuredIngredient(FlaskForm):
    key = TextField("Recipe ID")
    title = TextField("Recipe Title")
    amount = DecimalField("Amount")
    unit = SelectField("Unit", choices=[("cup", "cup"), ("oz", "oz"), ("lbs", "lbs")])
    ingredient = TextField("Ingredient")
    update = SubmitField("Add")


class CreateRecipe(FlaskForm):
    title = TextField("Title")
    shortdesc = TextField("Description")
    amount = DecimalField("Amount")
    unit = SelectField("Unit", choices=[("cup", "cup"), ("oz", "oz"), ("lbs", "lbs")])
    ingredient_list = TextField("Ingredient")
    create = SubmitField("Create")
    # ingredient = FormField(MeasuredIngredient)


class DeleteRecipe(FlaskForm):
    key = TextField("Recipe ID")
    title = TextField("Recipe Title")
    delete = SubmitField("Delete")


class ResetRecipe(FlaskForm):
    reset = SubmitField("Reset")


class GetShoppingList(FlaskForm):
    keys = TextField("Recipe IDs")
    create = SubmitField("Create List")
