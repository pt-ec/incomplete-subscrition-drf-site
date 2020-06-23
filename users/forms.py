import re

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from allauth.account.forms import SignupForm

from .models import User


class UserForm(forms.ModelForm):
    """ Creates the form for user registration """
    email = forms.EmailField(label='Email:')
    first_name = forms.CharField(min_length=1, label='First Name:')
    last_name = forms.CharField(min_length=1, label='Last Name:')
    password1 = forms.CharField(label='Password:', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm Password:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

    def clean_email(self):
        """ Checks if this email is unique in the database """
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('That email is already taken')
        return email

    def clean_first_name(self):
        """ Runs some validation on the first name """
        first_name = self.cleaned_data.get('first_name')
        if re.search("[^a-zA-Z\s.]", first_name):
            raise forms.ValidationError(
                'First name can only be comprised of letters')
        elif re.search("[.]{2,}", first_name):
            raise forms.ValidationError(
                'First name can only be comprised of letters')

        return first_name

    def clean_last_name(self):
        """ Runs some validation on the last name """
        last_name = self.cleaned_data.get('last_name')
        if re.search("[^a-zA-Z\s.]", last_name):
            raise forms.ValidationError(
                'Last name can only comprised of letters')
        elif re.search("[.]{2,}", last_name):
            raise forms.ValidationError(
                'Last name can only comprised of letters')

        return last_name

    def clean_password1(self):
        """ Passes some validation on password 1 """
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError(
                'Password must be longer then 6 characters')
        elif not re.search("[A-Z]", password1):
            raise forms.ValidationError(
                'Password must contain at least an uppercase letter')
        elif not re.search("[a-z]",  password1):
            raise forms.ValidationError(
                'Password must contain at least a lowercase letter')
        elif not re.search("[0-9]", password1):
            raise forms.ValidationError(
                'Password must contain at least a number')

        return password1

    def clean_password2(self):
        """ Check that the two password entries match """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')

        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'password', 'is_active', 'is_staff',
                  'is_superuser')

    def clean_password(self):
        return self.initial["password"]
