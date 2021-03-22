from flask_restful import Resource, reqparse
from flask import json
from app import app
from app.utils import geotos2

# import bigquery
from google.cloud import bigquery

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('start')
parser.add_argument('end')
parser.add_argument('date')


class TotalTripsPerDay(Resource):
    @staticmethod
    def get():
        """ Total number of trips per day in the date range, based on the pickup time of the trip.

        :return: Response 200 and result in json
       """
        try:
            # parse the arguments
            args = parser.parse_args()
            # start and end date in ISO format
            start = args['start']
            end = args['end']
            data = []
            # check the Parameter missing or not
            if start and end:
                # Construct a BigQuery client object.
                client = bigquery.Client()

                # Query to counts the total_trips date_wise
                query = """
                    SELECT
                      EXTRACT(DATE FROM trip_start_timestamp) AS date,
                      
                      COUNT(*) AS total_trips 
                    FROM
                      `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    GROUP BY date
                    HAVING date BETWEEN @start AND @end
                    ORDER BY date
                """
                # set the parameter for query
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("start", "STRING", start),
                        bigquery.ScalarQueryParameter("end", "STRING", end)
                    ]
                )
                # Start the query, passing in the extra configuration. Make an API request.
                query_job = client.query(query, job_config=job_config)

                # Fetch jobs created by the SQL script.
                for row in query_job:
                    result = {'date': str(row['date']),
                              'total_trips': row['total_trips']}
                    data.append(result)
                # Set the status code 200 if task is completed
                status = 200
            else:
                # Set the status code 400 if Parameter missing
                status = 400
                data = [{'message': 'Parameter Missing'}]
        except:
            # Set the status code 400 if Bad Request
            status = 400
            data = [{'message': 'Bad Request'}]

        # return the response with status code and data in json format
        response = app.response_class(response=json.dumps(data),
                                      status=status,
                                      mimetype='application/json')
        return response


class AverageFareHeatMap(Resource):
    @staticmethod
    def get():
        """
        The average fare per pick up location S2 ID at level 16 for the given date, based on the pickup time of the trip.
        :return: :return: Response 200 and result in json
        """
        try:
            # parse the arguments
            args = parser.parse_args()

            # start and end date in ISO format
            date = args['date']
            data = []
            if date:
                # Construct a BigQuery client object.
                client = bigquery.Client()
                # Query to get average fare per pick up location
                query = """
                            SELECT
                              pickup_latitude as latitude, 
                              pickup_longitude as longitude,
                              AVG(fare) as fare
                            FROM
                              `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                            WHERE
                              EXTRACT(DATE FROM trip_start_timestamp) = @date 
                              AND pickup_location IS NOT NULL
                              GROUP BY latitude,longitude
                        """
                # Set the parameter for query
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("date", "STRING", date)
                    ]
                )
                # Start the query, passing in the extra configuration. Make an API request.
                query_job = client.query(query, job_config=job_config)

                # Fetch jobs created by the SQL script.
                for row in query_job:
                    result = {'s2id': geotos2(row['latitude'], row['longitude']),  # convert location S2 ID at level 16
                              'fare': round(row['fare'], 2)}  # rounding to 2 decimal places
                    data.append(result)
                # Set the status code 200 if task is completed
                status = 200
            else:
                # Set the status code 400 if Parameter missing
                status = 400
                data = [{'message': 'Parameter Missing'}]
        except:
            # Set the status code 400 if Bad Request
            status = 400
            data = [{'message': 'Bad request'}]

        # return the response with status code and data in json format
        response = app.response_class(response=json.dumps(data),
                                      status=status,
                                      mimetype='application/json')
        return response


class AverageSpeed24hours(Resource):
    @staticmethod
    def get():
        """
        Average speed in miles per hour (trip_distance / (dropoff_datetime - pickup_datetime)) of trips
        that ended in the past 24 hours from the provided date.
        :return:
        """
        try:
            args = parser.parse_args()
            # date in ISO format
            date = args['date']
            data = []
            if date:
                # Construct a BigQuery client object.
                client = bigquery.Client()

                # Query to calculate average speed in miles per hour of trips
                #  that ended in the past 24 hours from the provided date.
                query = """
                    SELECT
                        ROUND((SUM(trip_miles)) /
                            (SUM(ABS(TIMESTAMP_DIFF(trip_end_timestamp,
                            trip_start_timestamp,MINUTE)))/60),2)
                            AS average_speed_24hrs
                    FROM    `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    WHERE    EXTRACT(DATE FROM trip_start_timestamp) = @date
                """

                # Set the parameter for query
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("date", "STRING", date)
                    ]
                )

                # Start the query, passing in the extra configuration. Make an API request.
                query_job = client.query(query, job_config=job_config)

                # Fetch jobs created by the SQL script.
                for row in query_job:
                    result = {'average_speed': row['average_speed_24hrs']}
                    data.append(result)

                # Set the status code 200 if task is completed
                status = 200
            else:
                # Set the status code 400 if Parameter missing
                status = 400
                data = [{'message': 'Parameter missing'}]

        except:
            # Set the status code 400 if Bad Request
            status = 400
            data = [{'message': 'Bad request'}]

        # return the response with status code and data in json format
        response = app.response_class(response=json.dumps(data),
                                      status=status,
                                      mimetype='application/json')
        return response
