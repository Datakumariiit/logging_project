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

    def get(self, request, app_label, model_name, user):
        try:
            # Dynamically get model
            model = apps.get_model(app_label, model_name)
            if not model:
                return Response({'error': 'Invalid model'}, status=status.HTTP_400_BAD_REQUEST)

            # Convert username to user object
            try:
                user_obj = User.objects.get(username=user)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Fetch logs for this user and model name
            print(user_obj)
            print(model_name)
            logs = DataChangeLog.objects.filter(user=user_obj).order_by('-timestamp')
            print(logs)

            data = []
            for log in logs:
                data.append({
                    'action': log.action,
                    'timestamp': log.timestamp,
                    'user': log.user.username if log.user else None,
                    'object_id': log.object_id,
                    'changes': log.changes,
                })

            return Response({'data': data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
