from django.shortcuts import render


def test_view(request):
    context = {
        'uri': request.path,
    }
    return render(request, 'base.html', context)
