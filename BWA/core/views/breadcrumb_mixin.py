''' Class pour la création du fil d'arianne '''


class HappyFamBreadcrumbMixin:
    breadcrumb = []

    def get_breadcrumb(self, **kwargs):
        return self.breadcrumb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = self.get_breadcrumb(**kwargs)
        if breadcrumb:
            context['breadcrumb'] = breadcrumb
        return context
