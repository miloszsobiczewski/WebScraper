from django import forms
from .models import Task
from api import utils as ut


class TaskForm(forms.ModelForm):
    url = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'style': 'width: 600px',
               'placeholder':
                   'your url: http://msobiczewski.pythonanywhere.com/'}))
    txt_ind = forms.BooleanField(required=False)
    img_ind = forms.BooleanField(required=False)

    class Meta:
        model = Task
        fields = ['url', 'txt_ind', 'img_ind']

    def clean(self, *args, **kwargs):
        txt_ind = self.cleaned_data.get('txt_ind')
        img_ind = self.cleaned_data.get('img_ind')
        if txt_ind is False and img_ind is False:
            raise forms.ValidationError('At least one scraping option (txt/img'
                                        ') needs to be selected.')
        url = self.cleaned_data.get('url')
        if ut.get_conn(url) is False:
            raise forms.ValidationError("Sorry site u're trying to reach is "
                                        "unavailable.")
        return super(TaskForm, self).clean(*args, **kwargs)
