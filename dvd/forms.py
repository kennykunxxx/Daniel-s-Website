from django import forms
from .models import Order

TYPED_CHOICE = [(i, str(i)) for i in range (1, 21)]
BUY_CHOICE = ((True, 'True'), (False, 'False'),)

class dvd_forms(forms.Form):
    quantity = forms.TypedChoiceField(choices=TYPED_CHOICE, coerce=int)
    update_quantity = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class buy_form(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ('buy',)
    