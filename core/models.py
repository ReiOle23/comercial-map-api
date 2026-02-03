from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

def default_coordinates():
    return {"lat": 0, "lon": 0}

class Business(models.Model):
    
    class meta:
        verbose_name = _('business')
        verbose_name_plural = _('businesses')
        
    name = models.CharField(max_length=100)
    iae_code = models.CharField(max_length=50, default='', blank=True)
    rentability = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    proximity_to_urban_center_m = models.IntegerField(default=0)
    coordinates = models.JSONField(default=default_coordinates)
        
    def __str__(self):
        return '%s' % self.name
    