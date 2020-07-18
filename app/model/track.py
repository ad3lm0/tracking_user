from marshmallow import Schema, fields
from model.event import Events, EventsSchema


class TrackBody:
    def __init__(self, userId, events):
        self.userId = userId
        self.events = events


class TrackBodySchema(Schema):
    userId = fields.String(
        required=True,
        error_messages={"required": {"message": "userId required", "code": 400}},
    )
    events = fields.Nested(
        EventsSchema,
        required=True,
        error_messages={
            "required": {"message": "originalUserId required", "code": 400}
        },
    )
