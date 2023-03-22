from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
import json
from django.forms.models import model_to_dict


@api_view(['GET'])
def test_api(request):
    return Response({"message": "App is running..."})


@api_view(['GET'])
def blogs_api(request):
    blogs = Blog.objects.all().order_by('-posted_at')
    serializedData = BlogSerializer(blogs, many=True)
    return Response(serializedData.data)


@api_view(['GET'])
def categories_api(request):
    categories = Category.objects.all()
    serializedData = CategorySerializer(categories, many=True)
    return Response(serializedData.data)


class MyBlogView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        blogs = Blog.objects.filter(author=user).order_by('-posted_at')
        serializedData = BlogSerializer(blogs, many=True)
        return Response(serializedData.data)

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
        user = request.user

        try:
            category_id = serializer.data['category']
            category = Category.objects.get(id=category_id)
        except Exception as e:
            print(e)
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Please enter a valid category ID'})

        single_blog = Blog.objects.create(
            author=user, title=serializer.data['title'], content=serializer.data['content'], category=category)
        single_blog.save()
        new_blog_dict = model_to_dict(single_blog)
        new_blog_serialized = json.dumps(new_blog_dict)
        return Response({'status': 200, 'payload': new_blog_serialized, 'message': 'Your blog is successfully created!'})

    def delete(self, request):
        blogId = request.data['blog_id']
        blog = Blog.objects.filter(id=blogId).first()
        if blog is None: 
            return Response({'status': 403, 'errors': 'Object not found', 'message': 'Blog ID does not exist'})
        
        blog.delete()
        return Response({'status': 200, 'message': 'Your blog is successfully deleted!'})


class UpdateBlogView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        blogId = request.data['blog_id']
        user = request.user
        blog = Blog.objects.filter(author=user, id=blogId).first()
        try:
            title = request.data['title']
        except:
            title = None

        try:
            content = request.data['content']
        except:
            content = None

        try:
            category = Category.objects.filter(
                id=request.data['category']).first()
        except:
            category = None

        if blog is not None:
            if title != None and title != "":
                blog.title = title
            if content != None and content != "":
                blog.content = content
            if category != None:
                blog.category = category
        blog.save()
        updated_blog_dict = model_to_dict(blog)
        updated_blog_serialized = json.dumps(updated_blog_dict)
        return Response({'status': 200, 'payload': updated_blog_serialized, 'message': 'Your blog is successfully updated!'})


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj), 'message': 'Successfully registered'})
