
def delete_by_filter(model_type, **kwargs) -> int:
    """
    Delete an entry from the given type using filters
    Return the amount of entries that have been deleted
    """
    nb_del, _ = model_type.objects.filter(**kwargs).delete()
    return nb_del

def delete_all_entries(model_type) -> int:
    """
    Delete all the entries in database from the given model
    Return the total number of entries deleted
    """
    nb_del, _ = model_type.objects.all().delete()
    return nb_del
