from django.contrib import admin
from django import forms

from .models import User


class UserFormAdmin(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput,
                               help_text="Your password can't be too similar")
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as before, for verification")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'password', 'password2', 'groups', 'user_permissions',
                  'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active']
    list_editable = ['is_staff', 'is_active']
    form = UserFormAdmin
