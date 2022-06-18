from django.shortcuts import render, redirect
from lists.models import Item, List


# TODO: support more than one list
# TODO: add unique URL for each list
# TODO: add URLs for adding a new item to an existing list via POST
def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list')
