from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm




class UserCreateForm(forms.ModelForm):
    password2 = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['email','username','first_name','last_name','password','password2', 'profile_picture']  # otp 
        labels = {'username':'Enter Your Full Name', 'email':'Enter Your Email', 'profile_picture':'Upload your image'}
        help_text = {'username':'Enter Your full name'}
        error_messages ={'username':{'required':'You cannot leave this place as blank', 
                                 'max_length':'name should not exceed 20 charecters'}, 
                                 'password':{'required':'Password is necessary'}}
        widgets = {'email': forms.EmailInput(attrs={'class':'form-control'}),
                   'password': forms.PasswordInput(attrs={'class':'form-control'}),
                   'username': forms.TextInput(attrs={'class':'form-control'}),
                   'first_name': forms.TextInput(attrs={'class':'form-control'}),
                   'last_name': forms.TextInput(attrs={'class':'form-control'}),
                   'profile_picture': forms.FileInput(attrs={'class':'form-control'})
                   }
        



class VerifyForm(forms.Form):
    email = forms.EmailField(label= "Your email", label_suffix=" ",
                             required=True, help_text="Enter your name", widget=forms.EmailInput(attrs={'class':'form-control',
                                                                                                        'id':'uniq'}))
    otp = forms.CharField(label= "Enter you 6 digit OTP", label_suffix=" ",
                          required=False,help_text="Enter your name", widget=forms.TextInput(attrs={'class':'form-control'}))
    


# class CustomAuthenticationForm(AuthenticationForm):
#     email = forms.EmailField(label='Email')
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'] = self.fields.pop('email')



class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})



class UserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['email','username','first_name','last_name','profile_picture']
        labels = {'email':'Email'}
        widgets = {'email': forms.EmailInput(attrs={'class':'form-control'}),
                   'username': forms.TextInput(attrs={'class':'form-control'}),
                   'first_name': forms.TextInput(attrs={'class':'form-control'}),
                   'last_name': forms.TextInput(attrs={'class':'form-control'}),
                   'profile_picture': forms.FileInput(attrs={'class':'form-control'})
                   }




class AdminProfileForm(UserChangeForm):
    is_verified = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget= forms.Select(attrs={'class':'form-select'}))
    is_active = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget= forms.Select(attrs={'class':'form-select'}))
    is_admin = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')), widget= forms.Select(attrs={'class':'form-select'}))
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['otp', 'password', 'password2']
        labels = {'email':'Email'}
        widgets = {'email': forms.EmailInput(attrs={'class':'form-control'}),
                   'username': forms.TextInput(attrs={'class':'form-control'}),
                   'first_name': forms.TextInput(attrs={'class':'form-control'}),
                   'last_name': forms.TextInput(attrs={'class':'form-control'}),
                   'profile_picture': forms.FileInput(attrs={'class':'form-control'}),
                #    'is_verified': forms.Select(attrs={'class':'form-control'}),
                #    'is_active': forms.Select(attrs={'class':'form-control'}),
                #    'is_admin': forms.Select(attrs={'class':'form-control'}),
                   'created_at': forms.DateInput(attrs={'class':'form-control'}),
                   'updated_at': forms.DateInput(attrs={'class':'form-control'}),
                   'last_login': forms.DateInput(attrs={'class':'form-control'}),
                   }



# Define your custom form class, inheriting from PasswordChangeForm
class StyledPasswordChangeForm(PasswordChangeForm):
    # Define any custom styling or behavior here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom Bootstrap classes to form fields
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})  # Add 'form-control' class for Bootstrap styling






class ForgotPassForm(forms.Form):
    email = forms.EmailField(label= "Your email", label_suffix=" ",
                             required=True, help_text="Enter your name", 
                             widget=forms.EmailInput(attrs={'class':'form-control'}))


class ResetPassForm(forms.Form):
    email = forms.EmailField(label= "Your email", label_suffix=" ",
                             required=True, help_text="Enter your name", widget=forms.EmailInput(attrs={'class':'form-control'}))
    otp = forms.CharField(label= "OTP", label_suffix=" ",
                             required=True, help_text="Enter your OTP", widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control'}))


