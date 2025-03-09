from django import forms
from event.models import *


class EventForm(forms.Form):
    name = forms.CharField(max_length=120, required=False)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    date = forms.DateField(widget=forms.SelectDateWidget, label="Date")
    time = forms.TimeField(widget=forms.TimeInput, required=False)
    location = forms.CharField(max_length=120)
    
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Category"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()


class StyledFormMixin:
    """Mixin to apply styles to form fields"""

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}",
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": f"{self.default_classes} resize-none",
                    "placeholder": f"Enter {field.label.lower()}",
                    "rows": 5,
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({"class": "space-y-2"})
            else:
                field.widget.attrs.update({"class": self.default_classes})


class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "date": forms.SelectDateWidget,
        
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:  # Fixed `Meta` capitalization
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
