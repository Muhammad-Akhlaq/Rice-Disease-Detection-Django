from django.shortcuts import render, HttpResponse,redirect, get_object_or_404,HttpResponseRedirect,reverse
from .models import prediction
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render (request, 'home.html')


def result(request):
    context = {}
    if request.method == 'POST':
        print("abcd")
        test_image = request.FILES['picture']
        ins = prediction(files=test_image)
        ins.save()
        print(test_image)
        test_image = image.load_img("media/"+str(test_image), target_size = (256, 256))
        print(test_image)
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        print("end")
        model = load_model("model.h5")
        result = model.predict_classes(test_image)
        print(result)
        if result[0] == 0:
            pred = 'Bacterial leaf blight'
        elif result[0] == 1:
            pred = 'Brown spot'
        else:
            pred = 'Leaf smut'
        print(pred)
        context = {"pred":pred}
    return render (request, 'result.html', context)






def signup(request):
    if request.method=='POST':
        username= request.POST['username']
        fname= request.POST['fname']
        lname= request.POST['lname']
        email= request.POST['email']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']
        #checks
        if len(username) > 10 or len(username) < 5:
            messages.error(request,"Username must be under 5 to 10 characters")
            return redirect('/')
        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('/')
        if pass1 != pass2:
            messages.error(request,"Passwords do not match")
        #create user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save() 
        messages.success(request,"Your Account is successfully created")
        return redirect("/")
    return render(request,'signup.html')



def Login(request):
    if request.method=='POST':
        loginusername= request.POST['loginusername']
        password= request.POST['pass']
        #authenticate
        user=authenticate(username=loginusername,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged in")
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect("/")
    return render(request,'login.html')



def Logout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect("/")
