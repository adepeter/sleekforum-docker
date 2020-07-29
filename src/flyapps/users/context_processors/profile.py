from ..forms.profile import UserProfileEditForm


def edit_profile_form(request):
    if request.user.is_authenticated:
        form = UserProfileEditForm(instance=request.user)
    form = None
    return {'edit_profile_form': form}
