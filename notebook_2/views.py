from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Container, Item, ItemTag
from .forms import ContainerForm

LoginRequiredMixin.login_url = reverse_lazy('notebook_2:login')

def divide_querysets_by_tag(tuple_list,  tag):
    """receives a list of tuples where each tuple has a list of tags and a queryset (filtered by those tags)
    thus, every Item in queryset is related to every Tag in the list.
    [([tag_1, tag_2, ...], queryset), ...]
    returns a list of tuples in the same format."""
    end_list = list()
    for tup in tuple_list:
        # a new queryset is created filtering original by the tag. the new tag is added to the list of tags.
        end_list.append((tup[0] + [tag], tup[1].filter(tags=tag)))
        # we keep elements excluded from filter above. no tag needs to be added to list.
        end_list.append((tup[0], tup[1].exclude(tags=tag)))
    return end_list


def divide_querysets_by_tag_list(tuple_list, tags_list):
    """runs divide_querysets_by_tag on tuple_list,
    then runs it again on that output with next Tag in tags_list and so on."""
    for tag in tags_list:
        tuple_list = divide_querysets_by_tag(tuple_list, tag)
    return tuple_list


def containerChangeTab(request, pk):
    """called with htmx from a div, returns html section. renders itemList.html"""

    c = get_object_or_404(Container, pk=pk, owner=request.user)

    # template button clicked sends get parameter that tells us what tab inside container we are in:
    if request.GET.get('on_actionables_tab') == "True":
        # updates container field that tells us what tab we are in:
        c.seeingActionables = True
        # asks for queryset of items that belong in the tab we are in:
        initial_queryset = c.item_set.filter(actionable=True)
    else:
        # same as above but opposite case.
        c.seeingActionables = False
        initial_queryset = c.item_set.filter(actionable=False)
    # saves model with 'seeingActionables' field changed above:
    c.save()

    # selecting tags by primary keys passed as parameters on get request:
    # tags = [Tag.objects.get(pk=i) for i in request.GET.getlist('tag')]

    # selecting all Tag instances:
    tags = ItemTag.objects.all()

    # filtering the initial_queryset a little bit more.
    initial_queryset = initial_queryset.exclude(done=True).order_by('created_at')
    # generating the list of tuples where tuple = (tag_list, queryset).
    querysets = divide_querysets_by_tag_list([([], initial_queryset)], tags)
    # ignoring querysets that ended up empty (a queryset is empty if no item satisfied filters like having two tags at the same time).
    querysets = [tup for tup in querysets if len(tup[1])]
    
    return render(request, 'notebook_2/itemList.html', {'querysets': querysets, 'container': c})


def itemDone(request, pk):
    i = Item.objects.get(pk=pk, owner=request.user)
    i.toggleDone()
    return render(request, 'notebook_2/item.html', {'container':i.parentContainer, 'item':i})


def containerCollapse(request, pk):
    """toggles collapsed or not on containersView"""
    c = Container.objects.get(pk=pk, owner=request.user)
    c.toggleCollapsed()
    return render(request, 'notebook_2/containersList.html', {'container_list':[c,]})

class loginView(LoginView):
    template_name = "notebook_2/login.html"
    next_page = reverse_lazy('notebook_2:containers')
    redirect_authenticated_user = True


class logoutView(LogoutView):
    next_page = reverse_lazy('notebook_2:login')


class registerView(FormView):
    form_class = UserCreationForm
    template_name = "notebook_2/register.html"
    success_url = reverse_lazy('notebook_2:containers')
    redirect_authenticated_user = True

    def form_valid(self, form):
        User = form.save() #creates and saves user to database.
        if User is not None:
            login(self.request, User)
        return super(registerView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        #page title that is rendered to main.html on <title> tag.
        ctx["view_title"] = "Registration"
        return ctx

    def get(self, *args, **kwargs):
        """redirects authenticated user to 'home'"""
        if self.request.user.is_authenticated:
            return redirect('notebook_2:containers')
        return super(registerView, self).get(self)


class searchView(LoginRequiredMixin, generic.TemplateView):
    template_name = "notebook_2/searchView.html"

    def get_context_data(self):
        searchInput = self.request.GET.get('search_query')

        cqs = Container.objects.all()
        iqs = Item.objects.all()
        cqs = cqs.filter(Q(Q(name__icontains=searchInput) | Q(description__icontains=searchInput)), owner=self.request.user)
        iqs = iqs.filter(Q(statement__icontains=searchInput), owner=self.request.user)

        return {"container_list":cqs, "item_list":iqs, "view_title": "Search"}


class containersView(LoginRequiredMixin, generic.TemplateView):
    model = Container
    template_name = 'notebook_2/containers.html'
    context_object_name = 'container_list'
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        #returns containers that don't have parents sorted by -timesOpened. so the most recently opened go on top.
        ctx["container_list"] = Container.objects.filter(parentContainer=None, owner=self.request.user).order_by('-timesOpened')
        return ctx


class containerDetailView(LoginRequiredMixin, generic.ListView):
    model = Container
    template_name = 'notebook_2/containerDetail.html'
    context_object_name = 'item_list'

    def get_context_data(self, **kwargs):
        container_pk = self.kwargs['pk']
        c = Container.objects.get(pk=container_pk, owner=self.request.user)
        c.add_lastOpened()
        c.add_timesOpened()
        #container needed to retrieve information on container detail view.
        #item_list corresponding to container, see get_queryset method above this one.
        return {"container": c}


class containerCreateView(LoginRequiredMixin, CreateView):
    # Custom form that inherits from ModelForm, check forms.py
    form_class = ContainerForm
    template_name = 'notebook_2/containerCreate.html'
    success_url = reverse_lazy('notebook_2:containers')

    # Open Ai's chatgpt made this.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form(self):
        form = super(containerCreateView, self).get_form()

        #make parent container not required. but appear.
        form.fields["parentContainer"].required = False
        #limit Container foreignkey options to pick from to containers the user owns.
        form.fields["parentContainer"].queryset = Container.objects.filter(owner=self.request.user)

        form.fields["name"].widget.attrs['placeholder'] = "Container name"
        form.fields["description"].widget.attrs['placeholder'] = "Container description"

        return form

    def form_valid(self, form):
        a_container = form.save(commit=False)

        #save container with owner foreignkey to user who was logged in on its creation.
        a_container.owner = self.request.user
        a_container.save()
        return super(containerCreateView, self).form_valid(form)


class containerUpdateView(LoginRequiredMixin, UpdateView):
    model = Container
    template_name = 'notebook_2/containerUpdate.html'
    context_object_name = 'container_list'
    fields = ["name", "description", "parentContainer"]
    success_url = reverse_lazy('notebook_2:containers')

    def get_context_data(self, **kwargs):
        ctx = super(containerUpdateView, self).get_context_data()
        ctx['container'] = get_object_or_404(Container, owner=self.request.user, pk=self.kwargs['pk'])
        return ctx

    def get_form(self):
        form = super(containerUpdateView, self).get_form()
        a_field = form.fields["parentContainer"]
        a_field.required = False
        #excludes itself as option from queryset to select from -because a container shouldn't be a subcontainer of itself. 
        a_field.queryset = Container.objects.filter(owner=self.request.user).exclude(pk=self.kwargs['pk'])
        return form


class containerDeleteView(LoginRequiredMixin, DeleteView):
    model = Container
    template_name = 'notebook_2/containerDelete.html'
    context_object_name = 'container_list'
    success_url = reverse_lazy("notebook_2:containers")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        #only to pass container in context to render template with container name.
        #checking it is the user's.
        ctx['container'] = Container.objects.get(pk=self.kwargs['pk'], owner=self.request.user).name
        return ctx

    def get_object(self):
        """limits queryset to user owned containers only."""
        queryset = Container.objects.filter(owner=self.request.user)
        return super().get_object(queryset)


class itemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'notebook_2/itemCreate.html'
    fields = ["done", "parentContainer", "parentItem", "statement", "actionable"]
    
    def get_success_url(self):
        container_pk = self.request.GET.get('container_pk')
        #if container_pk is passed on get request as query, and such entry exists for currently logged in user...
        if container_pk != "" and Container.objects.filter(pk=container_pk, owner=self.request.user).exists():
            #we set success_url as the one to its containerDetailView
            return reverse_lazy("notebook_2:container_detail", kwargs={'pk': container_pk})
        #or the containersView's otherwise.
        return reverse_lazy("notebook_2:containers") 
    
    def get_context_data(self, *args, **kwargs):
        ctx = super(itemCreateView, self).get_context_data( *args,**kwargs)

        container_pk = self.request.GET.get('container_pk')
        if container_pk != "": #handling case where there is no container_pk passed on get request.
            ctx['container'] = Container.objects.get(pk=container_pk, owner=self.request.user) #user-owned container to populate themplate.

        return ctx

    def get_form(self):
        f = super(itemCreateView, self).get_form()
        
        #limiting queryset to user-owned Containers.
        f.fields["parentContainer"].queryset = Container.objects.filter(owner=self.request.user)
        #field is not prepopulated if 'container_pk' value is not valid.
        f.fields['parentContainer'].initial = self.request.GET.get('container_pk')

        f.fields['parentItem'].required = False
        #field is just not prepopulated if value is not valid.
        f.fields['parentItem'].initial = self.request.GET.get("item_inspiring")
        f.fields['parentItem'].widget = forms.HiddenInput()
        f.fields['parentItem'].queryset = Item.objects.filter(owner=self.request.user)

        f.fields['statement'].widget.attrs['placeholder'] = "Item statement"

        #prepopulate actionable field with what's on query.
        f.fields['actionable'].initial = True if self.request.GET.get('on_actionables_tab') == "True" else False

        return f

    def form_valid(self, form):
        i = form.save(commit=False)
        #set item as owned by the user who was logged in on creation.
        i.owner = self.request.user
        i.save()
        return super(itemCreateView, self).form_valid(form)


class itemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'notebook_2/itemUpdate.html'
    fields = ["done", "parentContainer", "parentItem", "statement", "actionable", "tags"]

    def get_success_url(self):
        #as you can only see items from containers, container must exist.
        #so we use that Container's detail view as succes_url.
        success_url = reverse_lazy("notebook_2:container_detail", kwargs={'pk': self.request.GET.get('container_pk')})
        return success_url

    def get_context_data(self, *args, **kwargs):
        ctx = super(itemUpdateView, self).get_context_data(*args,**kwargs)
        #getting item we want to update.
        item = Item.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        #using the item to pass the container to populate some stuff on form template.
        ctx['container'] = item.parentContainer
        return ctx

    def get_form(self):
        f = super(itemUpdateView, self).get_form()

        #limiting queryset to user-owned Containers.
        f.fields["parentContainer"].queryset = Container.objects.filter(owner=self.request.user)
        
        f.fields['parentItem'].required = False #hiddes parentitem input.
        f.fields['parentItem'].widget = forms.HiddenInput() #and sets it as not required (user has to delete and create a different instance to change it)
        f.fields['parentItem'].queryset = Item.objects.filter(owner=self.request.user)

        f.fields['tags'].required = False
        f.fields['tags'].queryset = ItemTag.objects.filter(owner=self.request.user)

        return f


class itemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'notebook_2/itemDelete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(itemDeleteView, self).get_context_data(*args,**kwargs)
        item = Item.objects.get(pk=self.kwargs['pk'], owner=self.request.user) #using pk on link, making sure it is owned by user.
        ctx['container'] = item.parentContainer #passin container to populate form.

        return ctx
    
    def get_success_url(self):
        item = Item.objects.get(pk=self.kwargs['pk'], owner=self.request.user) #using pk on link. making sure it is owned by user.
        return reverse_lazy('notebook_2:container_detail', kwargs={'pk': item.parentContainer.id}) #an item is deleted from container, so there must be a container.

    def get_object(self):
        queryset = Item.objects.filter(owner=self.request.user)
        return super().get_object(queryset)