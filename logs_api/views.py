from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from django.contrib.contenttypes.models import ContentType
from logs.models import DataChangeLog
from django.apps import apps
from django.contrib.auth.models import User

class DataChangeLogView(APIView):
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            model_name = request.data.get('model_name')
            username = request.data.get('user')

            if not model_name or not username:
                return Response({'error': 'model_name and user are required fields.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user_obj = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                content_type = ContentType.objects.get(model=model_name.lower())
            except ContentType.DoesNotExist:
                return Response({'error': 'Invalid model_name'}, status=status.HTTP_400_BAD_REQUEST)
            
            logs = DataChangeLog.objects.filter(user=user_obj, content_type=content_type).order_by('-timestamp')

            data = [{
                'action': log.action,
                'timestamp': log.timestamp,
                'user': log.user.username if log.user else None,
                'object_id': log.object_id,
                'changes': log.changes,
            } for log in logs]

            return Response({'data': data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)