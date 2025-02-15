from functools import update_wrapper

from django.utils.decorators import classonlymethod
from django.views import View as _View
from django.views.generic import CreateView as _CreateView
from django.views.generic import DeleteView as _DeleteView
from django.views.generic import DetailView as _DetailView
from django.views.generic import FormView as _FormView
from django.views.generic import ListView as _ListView
from django.views.generic import TemplateView as _TemplateView
from django.views.generic import UpdateView as _UpdateView


class View(_View):
    """extends View of Django 2.2."""

    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class."
                                % (cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.setup(request, *args, **kwargs)
            if not hasattr(self, 'request'):
                raise AttributeError(
                    "%s instance has no 'request' attribute. Did you override "
                    "setup() and forget to call super()?" % cls.__name__
                )
            response = self.dispatch(request, *args, **kwargs)
            return self.after_view_process(request, response, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def after_view_process(self, request, response, *args, **kwargs):
        return response


class TemplateView(View, _TemplateView):
    pass


class FormView(View, _FormView):
    pass


class CreateView(View, _CreateView):
    pass


class ListView(View, _ListView):
    pass


class DetailView(View, _DetailView):
    pass


class UpdateView(View, _UpdateView):
    pass


class DeleteView(View, _DeleteView):
    pass
