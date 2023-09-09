from flask import Flask
from flask import url_for
from flask import request

from potions import get_all_propertys
from potions import Property
from potions import create_recipe, create_recipe_table

app = Flask(__name__)

@app.route("/")
def main():
    result = ""
    with open("test.html", "r") as f:
        result = f.readlines()
    return "".join(result)

@app.route("/get_answer")
def get_answer():
    print("Get Answer !")

    property1=Property(name=request.args.get('property1'), effectType="EffectPos")
    property2=Property(name=request.args.get('property2'), effectType="EffectPos")
    property3=Property(name=request.args.get('property3'), effectType="EffectPos")

    all=request.args.get("all", type=bool)

    arg_set = set()

    if not property1.empty():
        arg_set.add(property1)

    if not property2.empty():
        arg_set.add(property2)

    if not property3.empty():
        arg_set.add(property3)

    return "Test"
    # return create_recipe_table(create_recipe(arg_set, all=all), all=all)
    


result = ""
i = 0
for p in get_all_propertys():
    result += result + f"<option value=\"{p.name}\">{p.name}</option>\n"
    i = i + 1
    if i > 10:
        break

@app.route("/list_of_ingrediens")
def set_ingrediens_options():
    global result
    return result


