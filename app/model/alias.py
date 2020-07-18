from marshmallow import Schema, fields, validate


class AliasBody:
    def __init__(self, newUserId, originalUserId, timestampUTC):
        self.newUserId = newUserId
        self.originalUserId = originalUserId
        self.timestampUTC = timestampUTC


class AliasBodySchema(Schema):
    newUserId = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Field should not be empty."),
    )
    originalUserId = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Field should not be empty."),
    )
    timestampUTC = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Field should not be empty."),
    )
