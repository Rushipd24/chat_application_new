from rest_framework.response import Response
from rest_framework import status
from app.models import *
from .serializer import *
from rest_framework.views import APIView


class Mapping_user(APIView):
   
    def get(self, request ):
        """To get user, group and there massages"""
        try:
            name = request.data.get("Grp_name")
            if name == False:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Plese add a group name."})
            if not Group.objects.filter(grp_name=name).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Group not found. Please add a valid group."})
            grp_obj = Group.objects.get(grp_name=name)
            if not Mapping.objects.filter(grp_id=grp_obj).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Group not found."})
            mapp_obj = Mapping.objects.get(grp_id=grp_obj)
            user_list_masg = []
            for obj in mapp_obj:
                if obj.user_id:
                    data={}
                    data_user = obj.user_id
                    user_obj = User.objects.get(user_id = data_user)
                    masg_obj = Message.objects.filter(user_id=user_obj)
                    list_masg = []
                    for msg in masg_obj:
                        mass_user = msg.msg_desc 
                        list_masg.append(mass_user)
                    data[obj.user_name]=list_masg
                    user_list_masg.append(data)
            return Response(status=status.HTTP_200_OK,data={"message":user_list_masg}) 
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})
            
    def post(self, request):
        """ Add user in group """
        try:
            name = request.data.get("Grp_name")
            user_name = request.data.get("user_name",None)
            if name == False:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Plese add a group name."})
            if user_name == False:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Plese add a user name."})
            if not Group.objects.filter(grp_name=name).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Group not found. Please add a valid group."})
            if not User.objects.filter(user_name=user_name).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"User not found. Please add a valid user."})
            user_obj = User.objects.get(user_name=user_name)
            grp_obj = Group.objects.get(grp_name=name)
            if not Mapping.objects.filter(user_id=user_obj,grp_id=grp_obj).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"User already exist in group."})
            Mapping.objects.create(user_id=user_obj,grp_id=grp_obj)
            return Response(status=status.HTTP_200_OK,data={"message":"User successfully added in group."})  
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})

    
    def delete(self, request):
        """ Remove user from Group"""
        try:
            name = request.data.get("Grp_name")
            user_name = request.data.get("user_name",None)
            if name == False:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Plese add a group name."})
            if user_name == False:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Plese add a user name."})
            if not Group.objects.filter(grp_name=name).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Group not found. Please add a valid group."})
            if not User.objects.filter(user_name=user_name).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"User not found. Please add a valid user."})
            user_obj = User.objects.get(user_name=user_name)
            grp_obj = Group.objects.get(grp_name=name)
            if not Mapping.objects.filter(user_id=user_obj,grp_id=grp_obj).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"User or Group is not exists."})
            obj = Mapping.objects.get(user_id=user_obj,grp_id=grp_obj)
            obj.delete()
            return Response(status=status.HTTP_200_OK,data={"message":"User Remove successfully."}) 
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})
