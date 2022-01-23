from flask import render_template

from .app import app
from .forms import InputOutputTextForm
from .model import LanguageModel

model = LanguageModel()
model.predownload_data()
model.preload_model()
model.set_path_config_in_model()


last_value_dict = {
    "range": 0.55,
    "size": 2
}

@app.route('/', methods=["GET", "POST"])
def main():
    template = "index.html"
    form = InputOutputTextForm()

    form.range.data = last_value_dict["range"]
    form.max_size.data = last_value_dict["size"]

    if form.validate_on_submit():
        last_value_dict["range"] = form.range.data
        last_value_dict["size"] = form.max_size.data
        form.output_text.data = model.predict(form.input_text.data,
                                              temp=form.range.data,
                                              size=form.max_size.data)

    return render_template(template, form=form)
