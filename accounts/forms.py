from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password', 'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'class':'form-control'}))
    class Meta : 
        model = Account
        fields = ['first_name','last_name','phone_number','email', 'password']



    # parent class ko override krte huye ek super class bnayege
    def __init__(self,*args, **kwargs):                                   #kwargs is keyword argument
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter last name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder']= "Enter Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password !=  confirm_password:
            raise forms.ValidationError('password does not match')
    