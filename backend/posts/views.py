from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from .ai_service import generate_post, suggest_subjects



class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response({'error': 'Post non trouvé'}, status=404)

        scheduled_at = request.data.get('scheduled_at')
        if not scheduled_at:
            return Response({'error': 'scheduled_at est requis'}, status=400)

        post.scheduled_at = scheduled_at
        post.status = 'scheduled'
        post.save()

        return Response(PostSerializer(post).data)
    


class SuggestSubjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        subjects = suggest_subjects(
            job_title=profile.job_title,
            industry=profile.industry,
            interests=profile.interests
        )
        return Response({'subjects': subjects})


class GeneratePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        subject = request.data.get('subject')
        tone = request.data.get('tone', 'professional')

        if not subject:
            return Response({'error': 'subject est requis'}, status=400)

        profile = request.user.profile

        content = generate_post(
            subject=subject,
            tone=tone,
            job_title=profile.job_title,
            industry=profile.industry,
            interests=profile.interests
        )

        post = Post.objects.create(
            user=request.user,
            subject=subject,
            tone=tone,
            content=content,
            status='draft'
        )

        return Response(PostSerializer(post).data)