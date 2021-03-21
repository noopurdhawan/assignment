from app import api
from .views import TotalTripsPerDay, FareHeatMap, AverageSpeed24hours

api.add_resource(TotalTripsPerDay, '/total_trips')
api.add_resource(FareHeatMap, '/average_fare_heatmap')
api.add_resource(AverageSpeed24hours, '/average_speed_24hrs')
