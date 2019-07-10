from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
	fullname = forms.CharField(
		widget=forms.TextInput(
			attrs={
				"class": "form-control", 
				"placeholder": "Your Full Name",
			}
		)
	)
	email    = forms.EmailField(
		widget=forms.EmailInput(
			attrs={
				"class": "form-control", 
				"placeholder": "Your Email",
			}
		)
	)
	content  = forms.CharField(
		widget=forms.Textarea(
			attrs={
				"class": "form-control", 
				"placeholder": "Your Content",
			}
		)
	)

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if not "@" in email:
			raise forms.ValidationError("Not a valid email")
		if not ".com" or ".edu" or ".gov" in email:
			raise forms.ValidationError("Not a valid email")
		return email


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
	username = forms.CharField()
	email    = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("Username is taken.")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("Email is taken.")

		return email

	def clean(self):
		data = self.cleaned_data
		password = self.cleaned_data.get('password')
		if len(password) < 8:
			raise forms.ValidationError("Password must be at least 8 characters")
		password2 = self.cleaned_data.get('password2')
		if password2 != password:
			raise forms.ValidationError("Passwords must match.")
		return data






