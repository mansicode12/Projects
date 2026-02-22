# from rest_framework import serializers
# from .models import Group, GroupExpense, GroupMember, Settlement


# from rest_framework import serializers
# from .models import Group, GroupExpense, GroupMember, Settlement

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['id', 'name', 'description', 'created_at']

# class GroupExpenseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupExpense
#         fields = ['id', 'group', 'user', 'description', 'category', 'amount', 'created_at']

# class GroupMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupMember
#         fields = ['id', 'group', 'user', 'joined_at']

# class SettlementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Settlement
#         fields = ['id', 'group', 'payer', 'payee', 'amount', 'razorpay_payment_id', 'is_settled', 'settled_at']

from rest_framework import serializers
from .models import Group, GroupExpense, GroupMember, Settlement

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'created_at']

class GroupExpenseSerializer(serializers.ModelSerializer):
    # Add related fields for better API responses
    paid_by_name = serializers.CharField(source='paid_by.user.username', read_only=True)
    
    class Meta:
        model = GroupExpense
        fields = ['id', 'description', 'amount', 'category', 'date', 
                 'paid_by', 'paid_by_name', 'split_members', 'split_amount']

class GroupMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = GroupMember
        fields = ['id', 'group', 'group_name', 'user', 'username', 'joined_at']

class SettlementSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.user.username', read_only=True)
    
    class Meta:
        model = Settlement
        fields = ['id', 'member', 'member_name', 'amount', 'settled']