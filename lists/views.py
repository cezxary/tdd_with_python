from django.shortcuts import render, redirect
from lists.models import Item


# TODO: support more than one list
# TODO: add unique URL for each list
# TODO: add a URL for creating a new list via POST
# TODO: add URLs for adding a new item to an existing list via POST
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list')

    items = Item.objects.all()
    return render(request, 'lists/home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})
