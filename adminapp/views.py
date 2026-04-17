# django
from django.shortcuts import render

# restframework
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# models
from .models import SubscriptionPlan

# serializers
from .serializers import SubscriptionPlanSerializer
 
# local
from core.utils import success_response,error_response

class SubscriptionPlanViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

    def check_admin(self, request):
        if not request.user or not request.user.is_authenticated:
            return error_response(
                message="Authentication failed",
                errors="User not logged in",
                status_code=401
            )

        if not request.user.is_staff:
            return error_response(
                message="Permission denied",
                errors="Only admin can access this API",
                status_code=403
            )

        return None  # means allowed

    # LIST
    def list(self, request, *args, **kwargs):
        check = self.check_admin(request)
        if check:
            return check

        plans = self.get_queryset()
        serializer = self.get_serializer(plans, many=True)

        return success_response("Plans fetched", serializer.data)

    # CREATE
    def create(self, request, *args, **kwargs):
        check = self.check_admin(request)
        if check:
            return check

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return success_response("Plan created", serializer.data, 201)

        return error_response("Validation failed", serializer.errors)

    # RETRIEVE
    def retrieve(self, request, *args, **kwargs):
        check = self.check_admin(request)
        if check:
            return check

        plan = self.get_object()
        serializer = self.get_serializer(plan)

        return success_response("Plan fetched", serializer.data)

    # UPDATE
    def update(self, request, *args, **kwargs):
        check = self.check_admin(request)
        if check:
            return check

        plan = self.get_object()
        serializer = self.get_serializer(plan, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return success_response("Updated successfully", serializer.data)

        return error_response("Validation failed", serializer.errors)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        check = self.check_admin(request)
        if check:
            return check

        plan = self.get_object()
        plan.delete()

        return success_response("Deleted successfully")