
import re
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from random import choice


class NewTextForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={'name': 'title', 'placeholder': 'type the title', 'cols': '5'}))
    body = forms.CharField(label='', widget=forms.Textarea(
        attrs={'name': 'body', 'placeholder': 'type your text', 'rows': '3', 'cols': '5'}))
    # title.label = ''
    # body.label = ''


class EditTextForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
                            'name': 'title', 'placeholder': 'type the title', 'cols': '5', 'readonly': 'readonly'}))
    body = forms.CharField(label='', widget=forms.Textarea(
        attrs={'name': 'body', 'placeholder': 'type your text', 'rows': '3', 'cols': '5'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "header": "All Pages"
    })


def page(request, entry):
    entry_text = util.get_entry(entry)
    if entry_text == None:
        entry_text = f"Page {entry} is not found."
    else:
        entry_text = convert_markdown_to_html(entry_text)

    return render(request, "wiki/page.html", {
        "entry_text": entry_text,
        "entry_name": entry
    })


def new(request):
    if request.method == "POST":
        form = NewTextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            edit = request.POST.get('edit')
            if edit != "True":
                entries = util.list_entries()
                for entry in entries:
                    if entry.lower() == title.lower():
                        return render(request, "wiki/page.html", {
                            "entry_text": f"Page {entry} already exists.",
                            "entry_name": entry
                        })
            util.save_entry(title, body)
            return render(request, "wiki/page.html", {
                "entry_text": convert_markdown_to_html(body),
                "entry_name": title
            })
    return render(request, "wiki/newpage.html", {
        "form": NewTextForm()
    })


def edit(request):
    if request.method == "POST":
        title = request.POST.get('title')
        form = EditTextForm()
        form.fields['title'].initial = title
        form.fields['body'].initial = util.get_entry(title)
        return render(request, "wiki/newpage.html", {
            "form": form,
            "edit": True
        })


def convert_markdown_to_html(markdown_text):
    markdowner = Markdown()
    try:
        return markdowner.convert(markdown_text)
    except:
        return markdown_text


def search(request):
    q = request.GET.get("q")
    entry_text = util.get_entry(q)
    if entry_text == None:
        entries = util.list_entries()
        search_entries = []
        for i in entries:
            if i.lower().find(q.lower()) != -1:
                search_entries.append(i)
        if len(search_entries) == 0:
            page_header = "No search results"
        else:
            page_header = "Search results"
        return render(request, "encyclopedia/index.html", {
            "entries": search_entries,
            "header": page_header
        })
    else:
        return render(request, "wiki/page.html", {
            "entry_text": convert_markdown_to_html(entry_text),
            "entry_name": q,
            "edit": True
        })


def random_page(request):
    entries = util.list_entries()
    entry = choice(entries)
    entry_text = convert_markdown_to_html(util.get_entry(entry))
    return render(request, "wiki/page.html", {
        "entry_text": entry_text,
        "entry_name": entry
    })
