from django.shortcuts import redirect


def editdetails_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.id == kwargs['pid1'] or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')

    return wrapper_func
