from flask_restful import Resource, reqparse, abort
from flask import json
from app import app, api
from google.cloud import bigquery

# argument parsing
from app.utils import geotos2

parser = reqparse.RequestParser()
parser.add_argument('start')
parser.add_argument('end')
parser.add_argument('date')


class TotalTripsPerDay(Resource):
    def get(self):
        """

        :return:
        """
        try:
            args = parser.parse_args()
            start = args['start']
            end = args['end']
            data = []
            if start and end:
                client = bigquery.Client()
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
                # return query
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("start", "STRING", start),
                        bigquery.ScalarQueryParameter("end", "STRING", end)
                    ]
                )
                query_job = client.query(query, job_config=job_config)

                for row in query_job:
                    result = {'date': str(row['date']),
                              'total_trips': row['total_trips']}
                    data.append(result)
                status = 200
            else:
                status = 400
                data = [{'message': 'parameter missing'}]
        except:
            status = 400
            data = [{'message': 'bad request'}]

        response = app.response_class(response=json.dumps(data),
                                      status=status,
                                      mimetype='application/json')
        return response


class FareHeatMap(Resource):
    def get(self):
        """

        :return:
        """
        try:
            args = parser.parse_args()
            date = args['date']
            data = []
            if date:
                client = bigquery.Client()
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
                # return query
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("date", "STRING", date)
                    ]
                )

                query_job = client.query(query, job_config=job_config)
                for row in query_job:
                    result = {'s2id': geotos2(row['latitude'], row['longitude']),
                              'fare': round(row['fare'], 2)}
                    data.append(result)
                status = 200
            else:
                status = 400
                data = [{'message': 'parameter missing'}]
        except:
            status = 400
            data = [{'message': 'bad request'}]

        response = app.response_class(response=json.dumps(data),
                                      status=status,
                                      mimetype='application/json')
        return response


class AverageSpeed24hours(Resource):
    def get(self):
        """

        :return:
        """
        try:
            args = parser.parse_args()
            date = args['date']
            data = []
            if date:
                client = bigquery.Client()
                query = """
                    SELECT
                        ROUND((SUM(trip_miles)) /
                            (SUM(ABS(TIMESTAMP_DIFF(trip_end_timestamp,trip_start_timestamp,MINUTE)))/60),2)
                            AS average_speed_24hrs
                    FROM    `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    WHERE    EXTRACT(DATE FROM trip_start_timestamp) = @date
                """
                # return query
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("date", "STRING", date)
                    ]
                )
                query_job = client.query(query, job_config=job_config)
                data = []
                for row in query_job:
                    result = {'average_speed': row['average_speed_24hrs']}
                    data.append(result)
                status = 200
            else:
                status = 400
                data = [{'message': 'parameter missing'}]

        except:
            status = 400
            data = [{'message': 'bad request'}]

        response = app.response_class(response=json.dumps(data),
                                      status=status,
                                      mimetype='application/json')
        return response
