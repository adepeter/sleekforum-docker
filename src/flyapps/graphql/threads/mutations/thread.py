import graphene

from ..payloads.thread import (
    ThreadCreatePayload,
    ThreadDeletePayload,
    ThreadEditPayload
)


class ThreadMutation(graphene.ObjectType):
    thread_create = ThreadCreatePayload.Field()
    thread_delete = ThreadDeletePayload.Field()
    thread_edit = ThreadEditPayload.Field()
