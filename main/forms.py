from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import ProductReview,UserAddressBook



class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')


#Review add Form

class ReviewAdd(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields=('review_text','review_rating')

class AdressBookForm(forms.ModelForm):
    class Meta:
        model = UserAddressBook
        fields=('address','mobile','status')

class ProfileForm(UserChangeForm):
      class Meta:
        model = User
        fields = ('first_name','last_name','username','email')