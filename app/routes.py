#
from app import api
from .views import TotalTripsPerDay, AverageFareHeatMap, AverageSpeed24hours

# create the urls of the services and add to the api
api.add_resource(TotalTripsPerDay, '/total_trips')
api.add_resource(AverageFareHeatMap, '/average_fare_heatmap')
api.add_resource(AverageSpeed24hours, '/average_speed_24hrs')
