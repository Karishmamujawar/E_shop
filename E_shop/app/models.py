from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

from django import forms
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Sub_Category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length = 288)

    def __str__(self):
        return self.name


class Product(models.Model):
    Availability = (('In Stock', 'In Stock'),('Out of Stock','Out of Stock'))

    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=False,default='')
    subcategory = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,null=False,default='')
    brand  = models.ForeignKey(Brand, on_delete = models.CASCADE, null=True)
    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    Availability =  models.CharField(choices=Availability,null=True,max_length=188)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True,label="email",error_messages={'exist' : 'This is already exists'})

    class Meta:
        model = User
        fields = {'username','email','password1','password2'}

    def __init__(self,*args, **kwargs):
        super(UserCreateForm,self).__init__(*args, **kwargs)


        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

    def save(self,commit=True):
        user = super(UserCreateForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exist'])
        return self.cleaned_data['email']



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    image = models.ImageField(upload_to = 'ecommerce/order/image')
    product = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    quantity = models.CharField(max_length=5)
    price = models.IntegerField()
    address = models.CharField(max_length= 255)
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    total = models.CharField(max_length=1000, default='')
    date = models.DateField(default = datetime.datetime.today)

  #name is taken from Product model and product is from Order model
    def __str__(self):
        return self.product