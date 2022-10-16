from rest_framework.response import Response
from rest_framework import status
from app.models import *
from .serializer import *
from rest_framework.views import APIView



class User_messages(APIView):
   
    def get(self, request ):
        """"To get message"""
        try:
            user_obj= User.objects.get(user_id = request.api_user)
            masg_obj = Message.objects.filter(user_id=user_obj)
            list_masg = []
            for msg in masg_obj:
                mass_user = msg.msg_desc 
                list_masg.append(mass_user)
            return Response(status=status.HTTP_200_OK,data={"message":list_masg}) 
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})
            
    def post(self, request):
        """To create message"""
        try:
            masg_des = request.data.get("message")
            if masg_des :
                return Response(status=status.HTTP_200_OK,data={"message":"Plese add message."})
            Message.objects.create(user_id=request.api_user,msg_desc=masg_des)
            return Response(status=status.HTTP_204_NO_CONTENT,data={"message":"Messages send successfully."})  
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})

    def delete(self, request):
        '''To delete message'''
        try:
            id = request.data.get("msg_id")
            
            if id:
                if not Message.objects.filter(msg_id=id).exists():
                    return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"plese add valid msg id."})
                obj = Message.objects.get(msg_id=id)
                obj.delete()
                return Response(status=status.HTTP_200_OK,data={"message":"Message deleted successfully."}) 
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})
