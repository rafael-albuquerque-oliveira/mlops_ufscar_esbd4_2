from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    """
    Render the home page.

    This view function handles requests to the home page (typically at the root URL).
    It renders and returns the 'home.html' template.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.
    """
    return render(request, 'home.html')


def view_list(request, list_id):
    """
    Display a specific list and its items.

    This view function retrieves a List instance using the provided list_id.
    It then renders the 'list.html' template and passes the list instance 
    to the template via the context dictionary.

    Parameters:
        request (HttpRequest): The HTTP request object.
        list_id (int): The unique identifier for the list to be displayed.

    Returns:
        HttpResponse: The rendered list page with the list object in context.
    """
    # Retrieve the list with the specified ID from the database.
    list_ = List.objects.get(id=list_id)
    
    # Render the list template with the retrieved list object.
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """
    Create a new list with an initial item and redirect to the list page.

    This view function creates a new List object and then creates an associated
    Item using the text submitted via a POST request. After saving the new objects,
    it redirects the user to the new list's page.

    Parameters:
        request (HttpRequest): The HTTP request object, expected to include POST data 
                               with the key 'item_text'.

    Returns:
        HttpResponseRedirect: A redirect response to the URL of the newly created list.
    """
    # Create a new list object in the database.
    list_ = List.objects.create()
    
    # Create a new item with text from the POST data and associate it with the new list.
    Item.objects.create(text=request.POST['item_text'], list=list_)
    
    # Redirect the user to the newly created list's page.
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    """
    Add a new item to an existing list and redirect to that list's page.

    This view function retrieves an existing List using the provided list_id.
    It then creates a new Item, using the submitted text from a POST request,
    and associates it with the retrieved list. Finally, the user is redirected back
    to the list's page.

    Parameters:
        request (HttpRequest): The HTTP request object, expected to include POST data 
                               with the key 'item_text'.
        list_id (int): The unique identifier for the list to which the new item will be added.

    Returns:
        HttpResponseRedirect: A redirect response to the URL of the updated list.
    """
    # Retrieve the list object with the given ID.
    list_ = List.objects.get(id=list_id)
    
    # Create a new item for the list with text from the POST data.
    Item.objects.create(text=request.POST['item_text'], list=list_)
    
    # Redirect back to the list's page.
    return redirect(f'/lists/{list_.id}/')
