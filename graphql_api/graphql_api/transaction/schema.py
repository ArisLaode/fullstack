from datetime import datetime, timedelta
from django.utils.timezone import utc
import graphene
from graphql_api.transaction.models import Transaction
from graphene import Node
from graphene_django.types import DjangoObjectType
from django.db.models import Sum, F


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = []

    pk = graphene.String()

class TransactionTotalNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = ("amount", "category")
        filter_fields = []

    pk = graphene.String()

class TransactionTimeSeriesNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = ("amount", "created_at")
        filter_fields = []
    pk = graphene.String()

class TransactionQueries(graphene.ObjectType):
    transactions = graphene.List(TransactionNode)
    transactions_by_category = graphene.List(TransactionTotalNode, preset_range=graphene.String(required=True))
    transactions_by_timeseries = graphene.List(TransactionTimeSeriesNode, preset_range=graphene.String(required=True))
    category = graphene.String()
    amount = graphene.Int()

    def resolve_transactions(self, info):
        try:
            return Transaction.objects.all().order_by("-created_at")
        except Transaction.DoesNotExist:
            return None

    def resolve_transactions_by_category(self, info, preset_range):
        try:
            if preset_range == "LAST_7_DAYS":
                seven_days = datetime.utcnow().replace(tzinfo=utc) - timedelta(days=7)

                data_seven_days = Transaction.objects.filter(created_at__gte=seven_days).values('category').values_list('category', 'amount', 'created_at')
                data_seven_days_sum = data_seven_days.values('category').order_by('category').annotate(amount_=Sum('amount'))
                return [TransactionTotalNode(category = result_day_sum['category'], amount = result_day_sum['amount_']) for result_day_sum in data_seven_days_sum]
            elif preset_range == "LAST_7_WEEKS":
                seven_weeks = datetime.utcnow().replace(tzinfo=utc) - timedelta(weeks=7)

                data_seven_weeks = Transaction.objects.filter(created_at__gte=seven_weeks).values('category').values_list('category', 'amount', 'created_at')
                data_seven_weeks_sum = data_seven_weeks.values('category').order_by('category').annotate(amount_=Sum('amount'))
                return [TransactionTotalNode(category = result_weeks_sum['category'], amount = result_weeks_sum['amount_']) for result_weeks_sum in data_seven_weeks_sum]
            elif preset_range == "LAST_7_MONTHS":
                current_date = datetime.utcnow().replace(tzinfo=utc)
                months_ago = 7
                seven_months = current_date - timedelta(days=(months_ago * 365 / 12))
                data_seven_months = Transaction.objects.filter(created_at__gte=seven_months).values('category').values_list('category', 'amount', 'created_at')
                data_seven_months_sum = data_seven_months.values('category').order_by('category').annotate(amount_=Sum('amount'))
                return [TransactionTotalNode(category = result_months_sum['category'], amount = result_months_sum['amount_']) for result_months_sum in data_seven_months_sum]
            else:
                return None
        except Transaction.DoesNotExist:
            return None

    def resolve_transactions_by_timeseries(self, info, preset_range):
        try:
            if preset_range == "LAST_7_DAYS":
                seven_days = datetime.today() - timedelta(days=7)
                print(seven_days)

                data_seven_days = Transaction.objects.filter(created_at__gte=seven_days).values_list('created_at','amount').order_by('-created_at').annotate(key=F('created_at'))
                return [TransactionTimeSeriesNode(created_at = result_day[0].date(), amount = result_day[1]) for result_day in data_seven_days]
            elif preset_range == "LAST_7_WEEKS":
                data_seven_weeks = Transaction.objects.filter(created_at__week_day=7).values_list('created_at','amount').order_by('-created_at')
                return [TransactionTimeSeriesNode(created_at = result_weeks[0].date(), amount = result_weeks[1]) for result_weeks in data_seven_weeks]
            elif preset_range == "LAST_7_MONTHS":

                data_seven_months = Transaction.objects.raw('''select DISTINCT strftime('%m-%Y', created_at) as a,amount, id, created_at  from transaction_transaction tt  group by a''')
                data = []
                for data_month in data_seven_months:
                   data.append({'key' : data_month.created_at, 'amount': data_month.amount})
                return [TransactionTimeSeriesNode(created_at = result_months.created_at.date(), amount = result_months.amount) for result_months in data_seven_months]

            else:
                return None
        except Transaction.DoesNotExist:
            return None