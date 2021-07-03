def ajax_redirect_to_login():
    from django.http import HttpResponseRedirect
    from django.urls import reverse

    redirect = HttpResponseRedirect(reverse('login'))
    redirect.status_code = 278
    return redirect