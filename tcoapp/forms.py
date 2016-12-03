from django import forms

class UpdateProfile(forms.Form):
    username = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("First Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control","placeholder":'abc'}),
        label='First Name'
    )
                                
    mobile = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_message = ("Phone number must be 10 digits."),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'123-456-8911',"max-length" :10}))

    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'test@abc.com'}))
   
    
class DocumentForm(forms.ModelForm):
    class Meta:
        fields = ('description', 'document', )

class Profilepic(forms.Form):
    file = forms.FileField()  