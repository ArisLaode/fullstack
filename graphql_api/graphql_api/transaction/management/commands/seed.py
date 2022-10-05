import random
from datetime import timedelta

from graphql_api.transaction.models import Transaction, TransactionCategory

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument("--mode", type=str, help="Mode")

    def handle(self, *args, **options):
        print("Starting seed process...")
        run_seed(options["mode"])
        print("Done")


def run_seed(mode):
    Transaction.objects.all().delete()

    end_date = timezone.now()

    def get_amount():
        return random.randrange(1_000_000, 10_000_000)

    # Transfer fund
    transactions = []
    for i in range(50):
        amount = get_amount()
        created_at = end_date - timedelta(days=i)
        category = random.choice([
            TransactionCategory.MARKETING,
            TransactionCategory.ENGINEERING,
            TransactionCategory.GROWTH,
            TransactionCategory.PRODUCT
        ])

        transactions.append(
            Transaction(
                amount=amount,
                created_at=created_at,
                category=category
            )
        )

    Transaction.objects.bulk_create(transactions)
