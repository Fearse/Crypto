from django.forms import ModelForm

from .models import Portfolio, Transaction


class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name','creation_date','description']

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['name','price','amount','transType','date']