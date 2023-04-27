from user.models import UserCustom


def user_registration(
    email: str,
    username: str,
    password: str,
    is_active: bool = True,
    is_staff: bool = False,
) -> UserCustom:
    user = UserCustom.objects.create(
        email=email, username=username, is_active=is_active, is_staff=is_staff
    )
    user.set_password(password)
    user.full_clean()
    user.save()
    return user
