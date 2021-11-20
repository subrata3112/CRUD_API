from django.shortcuts import render
import uuid
from user_forms.common_functions import encryptor,pass_verify,query_fetch,query_exec
# Create your views here.

logged_in = False
current_user = None
user_id = None

def index(request):
    return render(request, "index.html")

# def register_page(request):
#     return render(request, "register.html")

def register(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    password = encryptor(password)
    unique_id = str(uuid.uuid4())

    search_query = "SELECT * FROM user_details WHERE email = '{}'".format(email)

    result = query_fetch(search_query)

    if result is not None:
        return render(request, "register.html", {"message":"Email already exists. Please Log-in."})

    insert_query = "INSERT INTO user_details VALUES('{}','{}','{}','{}')".format(unique_id,name,email,password)

    query_exec(insert_query)

    return render(request, "index.html",{"message":"User Registered Successfully."})

def sign_in(request):
    email = request.POST['email']
    password = request.POST['password']

    search_query = "SELECT * FROM user_details WHERE email = '{}'".format(email)

    result = query_fetch(search_query)

    if result is None:
        return render(request, "index.html",{"message":"Email not registered"})

    hashed_pass = result[3]
    

    if pass_verify(password,hashed_pass):
        current_user = result[1]
        user_id = result[0]
        logged_in = True
        return render(request, "logged_index.html",{"user":current_user})
    else:
        return render(request, "index.html",{"message":"Wrong Credentials!"})

def logout(request):
    logged_in = False
    current_user = None
    return render(request, "index.html")

def update_pass(request):

    password = request.POST['password']
    password = encryptor(password)
    update_query = "UPDATE user_details SET password = '{}' WHERE id = '{}'".format(password,user_id)
    query_exec(update_query)
    return render(request, "logged_index.html",{'message':"Password updated successfully","user":current_user})