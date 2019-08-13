# check are we going to the correct url
# check if the correct template is being used

from django.test import TestCase
from .models import Item
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404


class TestView(TestCase):

    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'todo_list.html')

    def test_get_add_item_page(self):
        page = self.client.get("/add")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'item_form.html')

    def test_get_edit_item_page(self):
        """need to create instance of the Item Model to get the item.id value below.
        Once the Item(name='Create a Test') is instanceiated and saved
        Django will auto create an id for it."""
        item = Item(name='Create a Test')
        item.save()

        page = self.client.get("/edit/{0}".format(item.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'item_form.html')

    def test_get_edit_page_for_item_that_does_not_exist(self):
        page = self.client.get("/edit/not_a_page")
        self.assertEqual(page.status_code, 404)


    def test_post_create_an_item(self):
        response = self.client.post("/add", {"name": "Create a Test"})
        item = get_object_or_404(Item, pk=1)
        self.assertEqual(item.done, False)

    def test_post_edit_an_item(self):
        item = Item(name="Create a Test")
        item.save()
        id = item.id 

        response = self.client.post("/edit/{0}".format(id), {"name": "A different name"})
        item = get_object_or_404(Item, pk=id)

        self.assertEqual("A different name", item.name)

    def test_toggle_status_self(self):
        item = Item(name="Create a Test")
        item.save()
        id = item.id

        response = self.client.post("/toggle/{0}".format(id))

        item = get_object_or_404(Item, pk=1)
        self.assertEqual(item.done, True)