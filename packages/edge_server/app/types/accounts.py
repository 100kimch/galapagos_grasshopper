import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models.accounts import Accounts as AccountsModel


class Accounts(SQLAlchemyObjectType):
    class Meta:
        model = AccountsModel
        interfaces = (graphene.relay.Node,)


class AccountAttribute:
    name = graphene.String()
    alias = graphene.String()


class CreateAccountInput(graphene.InputObjectType, AccountAttribute):
    pass
