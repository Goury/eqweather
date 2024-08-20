from django.db import models


class GridCell(models.Model):
	grid_id      = models.CharField(max_length=10)
	grid_x       = models.PositiveSmallIntegerField()
	grid_y       = models.PositiveSmallIntegerField()
	polygon_json = models.TextField(default='')

	class Meta:
		unique_together = ('grid_id', 'grid_x', 'grid_y')


class WeatherForecast(models.Model):
	when         = models.DateTimeField()
	temperature  = models.DecimalField(max_digits=4, decimal_places=1)
	humidity     = models.DecimalField(max_digits=4, decimal_places=1)
	cell         = models.ForeignKey(GridCell, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('cell', 'when')
