from django.db import models
from django.shortcuts import get_object_or_404
from django.dispatch import receiver

class Product(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        # if self.id:
        #     existing = get_object_or_404(Product, id=self.id)
        #     if existing.icon != self.icon:
        #         existing.icon.delete(save=False)

        super(Product, self).save(*args, **kwargs)

    @receiver(models.signals.pre_save, sender="store.Product")
    def server_delete_files(sender, instance, **kwargs):

        if instance.id is not None:
            for field in instance._meta.fields:
                if field.name == "icon":
                    file = getattr(instance, field.name)
                    if file:
                        file.delete(save=False)

    def __str__(self):
        return f"{self.name}"
