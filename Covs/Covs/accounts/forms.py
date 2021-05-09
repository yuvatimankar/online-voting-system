from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(forms.Form):
    username  = forms.CharField(
                           label='Username', 
                           max_length=100,  
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )
    email     = forms.EmailField(
                           widget=forms.EmailInput(attrs={'class': 'form-control'})
                           )
    password1 = forms.CharField(
                           label='Password',
                           max_length=100, 
                           min_length=5, 
                           widget=forms.PasswordInput(attrs={'class': 'form-control'})
                           )
    password2 = forms.CharField(
                           label='Confirm Password', 
                           max_length=100, 
                           min_length=5, 
                           widget=forms.PasswordInput(attrs={'class': 'form-control'})
                           )
    
#cleaning the email
    def clean_email(self):
        email = self.cleaned_data['email']
        qs    = User.objects.filter(email=email)
#checking the weather email is already registerd if it is the throgh an Error
        if qs.exists():
            raise ValidationError('Email is already registered')
        return email

#cleaning the password
    def clean_password2(self):
        #we checking password2 after password1 has been validated 
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']
        #make sure paaswords match
        if p1 != p2:
             raise ValidationError('Passwords do not Match')
        return p1

# def clean(self):
#     cleaned_data = super().clean()
#     p1 = cleaned_data.get('password1')
#     p2 = cleaned_data.get('password2')

#     if p1 and p2:
#         if p1 != p2:
#             raise ValidationError('Passwords do not Match')