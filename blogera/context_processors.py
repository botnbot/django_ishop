def user_permissions(request):
    """
    Добавляет в контекст шаблона ключи с важными правами пользователя.
    """
    user = request.user
    return {
        "can_unpublish_post": user.is_authenticated and (user.has_perm("blogera.can_unpublish_post") or user.is_staff),
        "is_staff": user.is_authenticated and user.is_staff,
    }
