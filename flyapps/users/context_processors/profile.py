from ..forms.profile import UserProfileEditForm


def edit_profile_form(request):
    form = UserProfileEditForm(instance=request.user)
    return {'edit_profile_form': form}
