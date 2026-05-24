from rest_framework import viewsets, permissions
from .models import Complaint
from .serializers import ComplaintSerializer

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all().order_by('-created_at')
    serializer_class = ComplaintSerializer
    
    # For Phase 2, we will allow anyone to post/view complaints
    # In Phase 3, we can restrict this using IsAuthenticatedOrReadOnly
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # If user is authenticated, attach them to the complaint
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
