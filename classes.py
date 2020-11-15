from flask_wtf import FlaskForm
from wtforms import (
    TextField,
    IntegerField,
    SubmitField,
    DecimalField,
    SelectField,
    FormField,
    BooleanField,
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
    cook_tim = IntegerField("Cooking Time (min)")
    prep_time = IntegerField("Prep Time (min)")
    amount = DecimalField("Amount")
    unit = SelectField("Unit", choices=[("cup", "cup"), ("oz", "oz"), ("lbs", "lbs")])
    ingredient = TextField("Ingredient")
    ingredient_list = TextField("Ingredient")
    selected = BooleanField("Selected")
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
