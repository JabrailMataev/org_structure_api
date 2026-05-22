from rest_framework.viewsets import ModelViewSet
from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



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