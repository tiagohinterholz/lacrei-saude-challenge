from django.db import models
from django.shortcuts import get_object_or_404


class CommonRepository:

    def __init__(self, model: models.Model):
        self.model = model

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def get_all(self, **filters):
        filters.setdefault("is_active", True)
        return self.model.objects.filter(**filters)

    def get_by_id(self, obj_id):
        return get_object_or_404(self.model, id=obj_id, is_active=True)

    def get_one(self, **filters):
        filters.setdefault("is_active", True)
        return get_object_or_404(self.model, **filters)

    def update(self, obj_id, **kwargs):
        instance = self.get_by_id(obj_id)
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def update_by_filter(self, filters: dict, **kwargs):
        return self.model.objects.filter(**filters).update(**kwargs)

    def delete(self, obj_id):
        instance = self.get_by_id(obj_id)
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        return True
