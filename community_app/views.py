from django.shortcuts import render
from rest_framework import viewsets
from .models import LoginModel, UserModel
from .serializers import LoginSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
import os
import json
from django.http import JsonResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Define the base class with common create logic
class BulkCreate(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # single-object creation
        return super().create(request, *args, **kwargs)

class LoginCreateView(BulkCreate):
    queryset = LoginModel.objects.all()
    serializer_class = LoginSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    #permission_classes = [AllowAny]  # Allow unauthenticated users to access this view

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        #user = authenticate(username=username, password=password)

        try:
            user = LoginModel.objects.get(username=username)
            if check_password(password, user.password):
                return Response({'message': 'Login successful', 'username': username}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except LoginModel.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserCreateView(BulkCreate):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        # Log the raw incoming data for debugging
        logger.debug(f"Raw request data: {request.data}")
        
        data = request.data
        
        # Check if data is a QueryDict and if it contains stringified JSON
        if isinstance(data, dict) and len(data) == 1:
            try:
                # The data might be wrapped in a string key, try parsing it
                parsed_data = json.loads(list(data.keys())[0])  # Get the first (and only) key's value
                logger.debug(f"Parsed data: {parsed_data}")  # Log the parsed data for debugging
                data = parsed_data  # Use the parsed data for further processing
            except json.JSONDecodeError:
                # If we can't parse the JSON, return an error
                logger.error("Invalid JSON format in the request data.")
                return Response({"error": "Invalid JSON format."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure the data is a dictionary before proceeding with serialization
        if isinstance(data, dict):
            # Initialize the serializer with the parsed data
            serializer = UserSerializer(data=data)
        else:
            # If the data is not a dictionary, return an error response
            logger.error(f"Invalid request format: {data}")
            return Response({"error": "Invalid request format."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the serialized data
        if serializer.is_valid():
            # Save the new user to the database and return the created data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If the data is not valid, return the validation errors
        logger.error(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        try:
            users = UserModel.objects.all()  # Fetch all users
            serializer = UserSerializer(users, many=True)  # Serialize the data
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'  # Use `user_id` as the lookup field in URLs

    def retrieve(self, request, *args, **kwargs):
        # Retrieve the user object based on user_id using get_object
        user = self.get_object()  # Retrieve the user using the default method
        try:
            user_serializer = UserSerializer(user)
            return Response({
                'user': user_serializer.data,
            })
        except UserModel.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        user = self.get_object()  # Retrieve the user instance

        # Deserialize request data
        user_serializer = UserSerializer(user, data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()  
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
