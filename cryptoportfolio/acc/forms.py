from django.forms import ModelForm

from .models import Portfolio, Transaction, Appeal


class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name','description']

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['name','price','amount','transType']

class AppealForm(ModelForm):
    class Meta:
        model = Appeal
        fields = ['email','text']