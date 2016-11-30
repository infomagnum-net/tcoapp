from django import forms

class Loginform(forms.Form):    
    email = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'username'}))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control","placeholder":'password'}),
        label='Password'
    )



class Registrationform(forms.Form):
    username = forms.RegexField(regex=r'^[A-Za-z][A-Za-z0-9]{2,}$',
        error_messages={'invalid':("First Letter Must be Character and Minimum of 3 Characters")},
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control","placeholder":'username'}),
        label='First Name'
    )
                                
    phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_messages={'invalid':("Phone Must be 10 digits")},
                                widget=forms.TextInput(attrs={'class': "form-control","placeholder":'phonenumber',"max-length" :10}))

    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'email'}))
    password = forms.RegexField(regex=r'^[A-Za-z0-9\w@%._-]{6,15}$',
        error_messages={'invalid':("Password Minimum 6 Letters Maximum 15 Letters")},
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control","placeholder":'password'}),
        label='Password'
    )
    terms = forms.BooleanField(
       error_messages={'required': 'You must accept the terms and conditions'},
       label="Terms&Conditions"
       )



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