from django import forms
from EApp.models import *
import re

class SignUpForm(forms.ModelForm):
    name= forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Your Full Name"}))
    email= forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Enter Your Email"}))
    phone= forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Your Mobile Number"}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter Password"}))
    cpassword= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter Confirm Password"}))
    bot_handler= forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model= SignupModel
        exclude= ['is_admin']

    def clean(self):
        print("Validate All Signup Fields")
        total_data= super().clean()

        print("Name Validation")
        inputname= total_data['name']
        if len(inputname) < 6:
            raise forms.ValidationError("Name must be 6 chars onwords")

        print("Email Validation")
        inputemail= total_data['email']

        #check email endswith @gmail.com
        if not inputemail.endswith("@gmail.com"):
            raise forms.ValidationError("Gmail extension is '@gmail.com'")
        #check email is already exist or not
        if SignupModel.objects.filter(email=inputemail).exists():
            raise forms.ValidationError("Email already exists")

        print("Phone Number Verification")
        inputphone= total_data['phone']
        if len(inputphone) != 10:
            raise forms.ValidationError("Phone number must be 10 digits")
        if not inputphone.isdigit():
            raise forms.ValidationError("Phone Number must be digit")

        print("Password Verification")
        inputpassword= total_data['password']
        if len(inputpassword) < 8:
            raise forms.ValidationError("Password must be 8 chars onwords")
        if not re.search(r'[A-Za-z]', inputpassword):
            raise forms.ValidationError("Password must contain atleast one latter")
        if not re.search(r'\d', inputpassword):
            raise forms.ValidationError("Password must contain atleast one digit")

        #Password match
        if total_data['password'] != total_data['cpassword']:
            raise forms.ValidationError("Password didn't match")
        return total_data
    
    def save(self, commit=True):
        user= super().save(commit=False)
        user.password = self.cleaned_data['password'] #Already hashed
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    email= forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Enter Your Email"}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter Password"}))

class AdminLogin(forms.Form):
    email= forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Enter Your Email"}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter Your Password"}))

class ProductForm(forms.ModelForm):
    name= forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Sweet or snacks name", 'class': 'form-name-input'}))
    description= forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Enter your Description", 'class': 'form-desc-input'}))
    price= forms.NumberInput()
    in_stock= forms.CheckboxInput()
    image= forms.ClearableFileInput()
    bot_handler= forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model= ProductModel
        fields= '__all__'

CITY_CHOICES= [
    ('',"Select Your City"),
    ('jaleswar', 'Jaleswar'),
    ('baleswar', 'Baleswar'),
    ('bhubaneswar', 'Bhubaneswar'),
    ('cuttack', 'Cuttack'),
    ('baripada', 'Baripada'),
    ('hyderabad', "Hyderabad"),
    ('delhi', "Delhi")
]
STATE_CHOICES= [
    ('',"Select Your State"),
    ('odisha', 'Odisha'),
    ('telengana', 'Telengana')
]
class CheckoutForm(forms.ModelForm):
    name= forms.CharField(label="Full name (First and Last name)")
    phone= forms.CharField(label="Mobile Number")
    pincode= forms.CharField(label="Pincode")
    house= forms.CharField(label="Flat, House no., Building, Company, Apartment")
    area= forms.CharField(label="Area, Street, Sector, Village")
    landmark= forms.CharField(label="Landmark")
    city= forms.ChoiceField(label="Town/City", choices=CITY_CHOICES)
    state= forms.ChoiceField(label="State", choices=STATE_CHOICES)

    class Meta:
        model= DeliveryAddressModel
        fields= ['name', 'phone', 'pincode', 'house', 'area', 'landmark', 'city', 'state']
    

