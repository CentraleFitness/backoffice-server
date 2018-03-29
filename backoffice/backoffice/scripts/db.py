from django.db import models

def delete_by_filter(model_type: models.Model, **kwargs) -> int:
    """
    Delete an entry from the given type using filters
    Return the amount of entries that have been deleted
    """
    nb_del, _ = model_type.objects.filter(**kwargs).delete()
    return nb_del
