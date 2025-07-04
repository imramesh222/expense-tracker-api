from django.contrib import admin
from .models import ExpenseIncome

@admin.register(ExpenseIncome)
class ExpenseIncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'amount', 'transaction_type', 'tax', 'tax_type', 'total', 'created_at')
    search_fields = ('title', 'user__username','transaction_type')
    list_filter = ('transaction_type', 'tax_type', 'created_at')