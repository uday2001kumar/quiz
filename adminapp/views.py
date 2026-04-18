# django
from django.shortcuts import render

# restframework
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

# models
from .models import SubscriptionPlan

# serializers
from .serializers import SubscriptionPlanSerializer
 
# local
from core.utils import success_response,error_response,SerializerErrorHandler

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
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        print("User",request.user)
        if not request.user.is_staff:
            return error_response(
                message="Permission denied",
                errors="Only admin can access this API",
                status_code=status.HTTP_403_FORBIDDEN
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

        name = request.data.get("name")

        #  Duplicate check
        if SubscriptionPlan.objects.filter(name__iexact=name).exists():
            return error_response(
                message="Plan already exists",
                errors=f"A plan with name '{name}' already exists",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        #  Correct serializer usage
        serializer = self.get_serializer(data=request.data)
        print("Serializer:",serializer)
        #  Validation
        if not serializer.is_valid():
            error = SerializerErrorHandler(serializer.errors)
            return error_response(
                message=error.error,
                errors="Validation failed",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        #  Save
        serializer.save()

        return success_response(
            message="Plan created",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )

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
        serializer = self.get_serializer(plan, data=request.data,partial=True)

        if not serializer.is_valid():
            error = SerializerErrorHandler(serializer.errors)
            return error_response(
                message=error.error,
                errors="Validation failed",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Updated successfully", data=serializer.data)

        return error_response(message="Validation failed", errors=serializer.errors)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        check = self.check_admin(request)
        if check:
            return check

        try:
            plan = self.get_object()  # raises 404 if not found

            plan.delete()

            return success_response(
                message="Deleted successfully",
                data={}
            )

        except Exception as e:
            return error_response(
                message="Something went wrong!",
                errors=str(e),
                status_code=status.HTTP_404_NOT_FOUND
            )