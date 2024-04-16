from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField()
    website = forms.CharField(required=False)
    notes = forms.CharField(required=False, widget=forms.Textarea)
