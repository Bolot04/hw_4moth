from django import forms

class RegisterForm(forms.Form):
    age = forms.IntegerField()
    photo = forms.ImageField()
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=18)
    confirm_password = forms.CharField(max_length=18) 


    def clean_confirm_password(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["confirm_password"]:
            raise forms.ValidationError("Password do not match")
        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)