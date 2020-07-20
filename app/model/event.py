from marshmallow import Schema, fields, validate


class EventBody:
    def __init__(self, eventName, metadata, timestampUTC):
        self.eventName = eventName
        self.metadata = metadata
        self.timestampUTC = timestampUTC


class EventSchema(Schema):
    eventName = fields.String(
        required=True,
        error_messages={"required": {"message": "eventName required", "code": 400}},
    )
    metadata = fields.List(
        fields.String(),
        required=True,
        validates=validate.Length(min=1),
        error_messages={
            "required": {"message": "At least one metadata is required", "code": 400}
        },
    )
    timestampUTC = fields.Integer(
        required=True,
        error_messages={"required": {"message": "timestampUTC required", "code": 400}},
    )
