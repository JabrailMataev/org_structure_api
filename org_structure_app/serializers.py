from rest_framework import serializers
from .models import Department, Employee
from typing import Optional, Dict, Any, List

def validate_functional(value : str, Error_name : str) -> str:
    if not value or len(value.strip()) == 0:
        raise serializers.ValidationError(f'{Error_name}')
    elif len(value) > 200:
        raise serializers.ValidationError('Максимальное количество символов 200')
    return value.strip()

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_full_name(self, value : str) -> str:
        return validate_functional(value, Error_name='Поле "ФИО" не может быть пустым')
    
    def validate_position(self,value : str) -> str:
        return validate_functional(value, Error_name='Поле "Должность" не может быть пустым')

class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent_id', 'created_at', 'employees', 'children']

    def get_employees(self, obj) -> List[Dict[str,Any]]:
        include_employees = self.context.get('include_employees', True)
        if not include_employees:
            return []
        employees = obj.employee_set.all().order_by('created_at')
        return EmployeeSerializer(employees, many=True).data

    def get_children(self, obj) -> List[Dict[str,Any]]:
        depth = self.context.get('depth', 1)
        if depth <= 0 or depth > 5:
            return []
        children = obj.department_set.all()
        return DepartmentSerializer(
            children, 
            many=True,
            context={
                'depth': depth - 1, 
                'include_employees': self.context.get('include_employees', True)
                }
        ).data

    def validate_name(self,value : str) -> str:
        return validate_functional(value, Error_name='Ошибка поле не может быть пустым')
        
    
    def validate(self, data : Dict[str, Any]) -> Dict[str, Any]:
        parent_id = data.get('parent_id')
        name = data.get('name')
        if parent_id and self.instance:
            current = parent_id
            while current:
                if current == self.instance:
                    raise serializers.ValidationError(
                        "Нельзя переместить отдел внутрь своего поддерева"
                    )
                current = current.parent
        elif parent_id and Department.objects.filter(parent_id=parent_id, name=name).exists():
            raise serializers.ValidationError('Название уже есть в этом подразделе')
        return data