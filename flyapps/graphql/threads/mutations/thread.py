import graphene

from ..payloads.thread import ThreadCreatePayload


class ThreadMutation(graphene.ObjectType):
    thread_create = ThreadCreatePayload.Field()
