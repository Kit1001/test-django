from django import template
from django.urls import resolve
from django_test.models import *

register = template.Library()


# define an inclusion tag with the name "draw_menu"
@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    # define a raw SQL query to fetch menu items that belong to the specified menu name
    my_query = """
    SELECT
        *
    FROM
        django_test_menuitem
    WHERE menu_id =
          (SELECT id FROM django_test_menu WHERE name = %s);
    """

    # execute the raw SQL query with the menu name parameter
    menus_raw = MenuItem.objects.raw(my_query, [menu_name])
    request = context.request

    menus = []    # initialize an empty list for menu tree

    # iterate over the raw query result and add the root menu items to the menus tree
    for menu in menus_raw:
        if menu.parent_id is None:
            menu_dict = {
                'id': menu.id,
                'url': menu.url,
                'expanded': False,
                'parent': None,
                'children': [],
            }
            menus.append(menu_dict)

    # iterate over the menus list and recursively build the menu tree
    for menu_item in menus:
        build_tree(menus_raw, menu_item)

    # mark the expanded menu item based on the current URL
    mark_expanded(menus, request)

    # return a dictionary of the menus list for the 'menu.html' template to use
    return {"menu_list": menus}


# a helper function to build the menu tree recursively
def build_tree(menu_list_raw, parent):
    for menu_item in menu_list_raw:
        if menu_item.parent_id == parent['id']:
            menu_item_dict = {
                'id': menu_item.id,
                'url': menu_item.url,
                'expanded': False,
                'parent': parent,
                'children': [],
            }
            parent['children'].append(menu_item_dict)
            # recursive call to populate 'children' field for new element
            build_tree(menu_list_raw, menu_item_dict)


# a helper function to find the matching URL in the menu tree
def find_matching_url(menu_list, url):
    for menu_item in menu_list:
        if menu_item['url'] == url:
            # if the menu item's URL matches the provided URL, return the menu item
            return menu_item
        else:
            # recursively search for the matching URL in the menu item's children
            result = find_matching_url(menu_item['children'], url)
            if result:
                return result


# a helper function to mark the expanded menu item based on the current URL,
# so we can expand  corresponding elements of menu later in template
def mark_expanded(menu_list, request):
    path = request.path
    named_url = resolve(path).url_name
    url = named_url if named_url else path
    url = url.strip('/')
    matched_menu_item = find_matching_url(menu_list, url)    # find the matching URL in the menu tree
    if matched_menu_item:
        matched_menu_item['expanded'] = True    # mark the matching menu item as expanded
        matched_menu_item['active'] = True
        parent = matched_menu_item['parent']
        while parent:
            parent['expanded'] = True
            parent = parent['parent']
