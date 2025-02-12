
from strawberry import Schema, field
from strawberry import type as graphql_type
from strawberry.identifier import SchemaIdentifier, SupportedSchema
from strawberry import enum, enum_value
from enum import Enum

@enum
class RiskDecision(Enum):
    ACCEPT = enum_value("accept")
    REJECT = enum_value("reject", supported_schemas=[SupportedSchema(name="internal")])

@graphql_type
class Query:
    @field(name="acceptRiskDecision")
    def get_accept_risk_decision(self) -> RiskDecision:
        return RiskDecision.ACCEPT

    @field(name="rejectRiskDecision")
    def get_reject_risk_decision(self) -> RiskDecision:
        return RiskDecision.REJECT


internal_schema = Schema(
    schema_identifier=SchemaIdentifier(name="internal", version=""), query=Query
)
external_schema = Schema(
    schema_identifier=SchemaIdentifier(name="external", version=""), query=Query
)
plain_schema = Schema(query=Query)


def test_supported_enum_values_by_schema():
    # Internal schemas can select the `debugMessage` but not the external schema
    result = internal_schema.execute_sync("{ acceptRiskDecision }", root_value=Query())
    assert not result.errors
    assert result.data["acceptRiskDecision"] == RiskDecision.ACCEPT.name

    result = internal_schema.execute_sync("{ rejectRiskDecision }", root_value=Query())
    assert not result.errors
    assert result.data["rejectRiskDecision"] == RiskDecision.REJECT.name

    result = external_schema.execute_sync("{ acceptRiskDecision }", root_value=Query())
    assert not result.errors
    assert result.data["acceptRiskDecision"] == RiskDecision.ACCEPT.name

    result = plain_schema.execute_sync("{ rejectRiskDecision }", root_value=Query())
    assert result.errors



