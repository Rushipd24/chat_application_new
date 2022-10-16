from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import *
from .serializer import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout

@api_view(['GET'])
def get_user(request):
    try:
        userlist = User.objects.all().exclude(Status="Inactive")
        serializer_class=UserSerializer(userlist,many=True)
        return Response(status=status.HTTP_200_OK,data={"message":serializer_class.data}) 
    except Exception as e:
        print("Exception  in userlist:",e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})
     

@api_view(['POST'])
def create_user(request):
    try:
        user_obj = User.objects.get(username=request.api_user)
        if user_obj.is_superuser: 
            return Response({'message':"You are not authorized" },status=status.HTTP_403_FORBIDDEN)
        email = request.data.get("email",None)
        phone = request.data.get("phone",None)
        first_name = request.data.get("first_name",None)
        last_name = request.data.get("last_name",None)
        password = request.data.get("password",None)
        print(email,password,last_name, phone,first_name )
        if not email:
            return Response({"message":"email is not provided"},status=status.HTTP_403_FORBIDDEN)

        #!  check for duplicate email id
        if User.objects.filter(email__iexact=email).exists():
            return Response({"message":"Email id already Registered."},status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.create(
                                        username=email,
                                        email=email,
                                        first_name=first_name,
                                        last_name=last_name,
                                        phone=phone,    
                                        created_by ="Admin",
                                        )              
            user.set_password(password)
            user.save() 
        except Exception as e:
            print('Exception in user creation',e)
            return Response({"message":"User could not be created."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message":"User Created Successfully."},status=status.HTTP_200_OK)
    except Exception as e:
        print('Exception: ',e)
        return Response({"message":"Something went wrong Please Try again Later."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
@api_view(['PATCH'])
def update_user(request):
    try:
        user_obj = User.objects.get(username=request.api_user)
        if user_obj.is_superuser: 
            return Response({'message':"You are not authorized" },status=status.HTTP_403_FORBIDDEN)
        userId = request.data.get('User_ID')
        phone = request.data.get("phone",None)
        first_name = request.data.get("first_name",None)
        last_name = request.data.get("last_name",None)

        if not User.objects.filter(User_ID=userId):
            return Response({"message":"User not found."},status=status.HTTP_404_NOT_FOUND)      
        user = User.objects.get(User_ID=userId)
            
        if request.data.get('first_name'):
            user.first_name = first_name

        if request.data.get('last_name'):
            user.last_name = last_name

        if request.data.get('phone'):
            user.phone = phone
        user.save()
        return Response({"message": "User updated Succesfully." },status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong Please Try again Later."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   
@api_view(['DELETE'])
def delete_user(request,primary_key):
    try:
        if request.method == 'DELETE':
            user_obj = User.objects.get(username=request.api_user)
            if user_obj.is_superuser: 
                return Response({'message':"You are not authorized" },status=status.HTTP_403_FORBIDDEN)
            try:
                if not User.objects.filter(User_ID=primary_key,Status='Active'):
                    return Response({"message":"User not found."},status=status.HTTP_404_NOT_FOUND) 
                user = User.objects.get(User_ID=primary_key)
                user.Status = 'Inactive'
                user.save()
                return Response({"message":"User deleted successfully."},status=status.HTTP_200_OK)
            except Exception as e:
                print("Exception : ",e)
                return Response({"message":"Something went wrong Please Try again Later."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
    except Exception as e:
        print(e)
        return Response({"message":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def login_request(request):
    """
    Login API Endpoint
    input parameters: email(string),password(string)
    """
    if request.method == "POST":
        try:
            # fetch email and password from 
            email = request.data.get("email", None)
            if not User.objects.filter(username__iexact=email).exists():
                return Response({"message": "user not found."}, status=status.HTTP_404_NOT_FOUND)
            password = request.data.get("password", None)
            try:
                user_obj = User.objects.get(username=email)
                # check for organisation status
                if user_obj.Status == 'Inactive':
                    return Response({"message": "User is deactivated/blocked."}, status=status.HTTP_403_FORBIDDEN)
                username = email
            except Exception as e:
                return Response({"message": "Invalid login credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Login successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Login failed."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Error: ', e)
            return Response({"message": "Something went wrong. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@api_view(['GET'])
def user_logout(request):
  logout(request)
  return Response({"message": "Logout successfully."}, status=status.HTTP_200_OK)







class CreateGrp(APIView):
   
    def get(self, request ):
        try:
            userlist = Group.objects.all().exclude(Status="Inactive")
            serializer_class=GroupSerializer(userlist,many=True)
            return Response(status=status.HTTP_200_OK,data={"message":serializer_class.data}) 
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})
            
    def post(self, request):
        try:
            name = request.data.get("Grp_name")
            if name:
                Group.objects.create(grp_name=name)
                return Response(status=status.HTTP_200_OK,data={"message":"Group created successfully."})
            else:
                return Response(status=status.HTTP_204_NO_CONTENT,data={"message":"datanot found."})  
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})

    #@method_decorator(feature_permission_check(role_permission='update question'))
    def put(self, request):
        try:
            name = request.data.get("Grp_name")
            new_name = request.data.get("Grp_new_name")
            if name:
                if not Group.objects.filter(grp_name=name).exists():
                    return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"group not found."})
                obj = Group.objects.get(grp_name=name)
                obj.grp_name = new_name
                obj.save()
                return Response(status=status.HTTP_200_OK,data={"message":"Group name upadated successfully."})
            else:
                return Response(status=status.HTTP_204_NO_CONTENT,data={"message":"datanot found."})  
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})


        
    #@method_decorator(feature_permission_check(role_permission='delete question'))
    def delete(self, request):
        try:
            id = request.data.get("Grp_id")
            
            if id:
                if not Group.objects.filter(grp_id=id).exists():
                    return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"group not found."})
                obj = Group.objects.get(grp_id=id)
                obj.delete()
                return Response(status=status.HTTP_200_OK,data={"message":"Group deleted successfully."})
            else:
                return Response(status=status.HTTP_204_NO_CONTENT,data={"message":"datanot found."})  
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})
