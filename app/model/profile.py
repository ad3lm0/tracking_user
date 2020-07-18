from marshmallow import Schema, fields, validate


class ProfileBody:
    def __init__(self, userId, attributes, timestampUTC):
        self.userId = userId
        self.attributes = attributes
        self.timestampUTC = timestampUTC


class ProfileBodySchema(Schema):
    userId = fields.String(
        required=True,
        error_messages={"required": {"message": "userId required", "code": 400}},
    )
    attributes = fields.Dict(
        keys=fields.Str(),
        values=fields.String(),
        required=True,
        validates=validate.Length(min=1),
        error_messages={
            "required": {"message": "At least one attributes is required", "code": 400}
        },
    )
    timestampUTC = fields.Integer(
        required=True,
        error_messages={"required": {"message": "timestampUTC required", "code": 400}},
    )
