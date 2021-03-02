from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import ForeignObjectRel, OneToOneRel, OneToOneField
from rest_framework.filters import OrderingFilter

import re


class RelatedOrderingFilter(OrderingFilter):
    """
    Extends OrderingFilter to support ordering by fields in related models
    using the Django ORM __ notation
    """
    def is_valid_field(self, model, field):
        """
        Return true if the field exists within the model (or in the related
        model specified using the Django ORM __ notation)
        """
        components = field.split('__', 1)
        try:

            field = model._meta.get_field(components[0])

            if isinstance(field, OneToOneField):
                return True

            if isinstance(field, OneToOneRel):
                return self.is_valid_field(field.related_model, components[1])

            # reverse relation
            if isinstance(field, ForeignObjectRel):
                return self.is_valid_field(field.model, components[1])

            # foreign key
            if field.rel and len(components) == 2:
                return self.is_valid_field(field.rel.to, components[1])
            return True
        except FieldDoesNotExist:
            return False
    
    def remove_invalid_fields(self, queryset, fields, view, request):
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        fields = [pattern.sub('_', field.replace(".", "__")).lower() for field in fields ]
        return [term for term in fields if self.is_valid_field(queryset.model, term.lstrip('-'))]
