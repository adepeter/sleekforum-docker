from ....miscs.models.activity import Action

from ...viewmixins.post import UpDownVotePostMixin


class UpVotePost(UpDownVotePostMixin):
    activity_action = Action.UP_VOTE


class DownVotePost(UpDownVotePostMixin):
    activity_action = Action.DOWN_VOTE
