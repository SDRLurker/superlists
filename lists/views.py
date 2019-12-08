from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        # .objects.create is a neat shorthand for creating a new Item, without needing to call .save().
        Item.objects.create(text = request.POST['item_text'])
        # Redirect After a POST
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
