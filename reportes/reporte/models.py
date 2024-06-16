from djongo import models

class Visit(models.Model):
    date = models.DateTimeField()
    status = models.CharField(max_length=50)
    reserved = models.BooleanField()

    class Meta:
        db_table = 'visits'  # Nombre de la colección en MongoDB
