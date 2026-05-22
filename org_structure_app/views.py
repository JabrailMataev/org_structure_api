from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.transaction import atomic



class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=True, methods=['post'])
    def employees(self, request, pk=None):
        department = self.get_object()
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(department=department)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @atomic
    def destroy(self, request, *args, **kwargs):
        department = self.get_object()
        mode = request.query_params.get("mode", "cascade")
        
        if mode == "cascade":
            department.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif mode == "reassign":
            reassign_to = request.query_params.get("reassign_to_department_id")
            if not reassign_to:
                return Response(
                    {"error": "reassign_to_department_id is required for mode=reassign"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                new_parent = Department.objects.get(id=reassign_to)
            except Department.DoesNotExist:
                return Response(
                    {"error": "Department not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            department.employee_set.update(department=new_parent)

            department.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "mode must be 'cascade' or 'reassign'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

    def retrieve(self, request, *args, **kwargs):
        department = self.get_object()

        depth = request.query_params.get('depth', 1)
        include_employees = request.query_params.get('include_employees', 'true').lower() == 'true'

        serializer = DepartmentSerializer(
            department,
            context={
                'depth': int(depth),
                'include_employees': include_employees,
                'request': request
            }
            )
        return Response(serializer.data)


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer