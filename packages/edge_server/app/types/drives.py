import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models.drives import Drives as DrivesModel


class Drives(SQLAlchemyObjectType):
    class Meta:
        model = DrivesModel
        interfaces = (graphene.relay.node,)


class DriveAttribute:
    name = graphene.String()
    alias = graphene.String()


class CreateDriveInput(graphene.InputObjectType, DriveAttribute):
    pass
