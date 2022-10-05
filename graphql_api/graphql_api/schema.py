from graphql_api.transaction.schema import TransactionQueries
import graphene

from graphene_django.debug import DjangoDebug


class Query(
    TransactionQueries,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query)
