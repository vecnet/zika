# Copyright (C) 2015, University of Notre Dame
# All rights reserved
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from website.apps.big_brother.models import PageVisit, TrackingCode
from django.utils.translation import ugettext_lazy as _


class MacedFilter(SimpleListFilter):
    title = _("S.O.B.E.R items")
    parameter_name = "shoe_maced_items"

    def lookups(self, request, model_admin):
        return ("Yes", "Yes"), ("No", "No")

    def queryset(self, request, queryset):
        if self.value() == "Yes":
            return queryset.exclude(url__icontains="maced").exclude(url__icontains="/admin/")


class PageVisitAdmin(admin.ModelAdmin):
    list_display = ("url", "action", "user", "timestamp", "ip", "http_code")
    search_fields = ("url", "user__username", "user__first_name", "user__last_name")
    list_filter = ("user", MacedFilter, "http_code")

admin.site.register(PageVisit, PageVisitAdmin)


class TrackingCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "action", "timestamp", "ip", )
    search_fields = ("code", "ip")

admin.site.register(TrackingCode, TrackingCodeAdmin)
