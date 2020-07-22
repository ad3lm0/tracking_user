from marshmallow import Schema, fields
from model.event import EventBody, EventSchema


class TrackBody:
    def __init__(self, userId, events):
        self.userId = userId
        self.events = self.events_object_list(events)

    def events_object_list(self, events):
        event_list = []
        for event in events:
            event_object = EventBody(**event)
            event_list.append(event)

        return event_list


class TrackBodySchema(Schema):
    userId = fields.String(
        required=True,
        error_messages={"required": {"message": "userId required", "code": 400}},
    )
    events = fields.List(
        fields.Nested(EventSchema),
        required=True,
        error_messages={
            "required": {"message": "At least one event is required", "code": 400}
        },
    )
