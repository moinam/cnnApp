from google.cloud import bigquery
from google.oauth2 import service_account
from backend.helpers.configuration import BIGQUERY_CONFIG

PROJECT_NAME = BIGQUERY_CONFIG['project_name']

credentials = service_account.Credentials.from_service_account_file(
    BIGQUERY_CONFIG['credentials_path'])
client = bigquery.Client(credentials=credentials)


def get_time_spent_norm_prediction(client_id, task_type, quantity, limit=10):
    rows = client.query(
        f"SELECT \
            `{PROJECT_NAME}.Teams`.TeamId, \
            Location, \
            CAST(`{PROJECT_NAME}.PredictedTimeSpentNorm`.PredictedTimeSpentNorm * 3600 as int) as PredictedTimeSpentNorm, \
            Duration as TravelDuration, \
            Members \
        FROM \
            `{PROJECT_NAME}.PredictedTimeSpentNorm` \
        LEFT JOIN `{PROJECT_NAME}.Teams` ON `{PROJECT_NAME}.PredictedTimeSpentNorm`.TeamId = `{PROJECT_NAME}.Teams`.TeamId \
        LEFT JOIN `{PROJECT_NAME}.Clients` ON ClientId = '{client_id}' \
        LEFT JOIN `{PROJECT_NAME}.LocationDistances` ON \
            `{PROJECT_NAME}.LocationDistances`.ServicePointLocation = Location and \
            `{PROJECT_NAME}.LocationDistances`.ClientLocation = \
                CONCAT(`{PROJECT_NAME}.Clients`.PostalCode, '-', `{PROJECT_NAME}.Clients`.City) \
        LEFT JOIN ( \
            SELECT \
                TeamId, \
                STRING_AGG(Name, ', ') AS Members \
            FROM `{PROJECT_NAME}.TeamMembers` \
            LEFT JOIN `{PROJECT_NAME}.ServiceEmployees` ON \
                `{PROJECT_NAME}.TeamMembers`.ServiceEmployeeId = `{PROJECT_NAME}.ServiceEmployees`.ServiceEmployeeId \
            GROUP BY TeamId \
        ) as x ON \
            `{PROJECT_NAME}.PredictedTimeSpentNorm`.TeamId = x.TeamId \
        WHERE `TaskType`='{task_type}' \
        ORDER BY PredictedTimeSpentNorm ASC \
        LIMIT {limit}").result()
    predictions = []
    for row in rows:
        prediction = int(row.PredictedTimeSpentNorm)
        travel_duration = int(row.TravelDuration)
        predicted_working_time = prediction * int(quantity)

        predictions.append({"teamId": row.TeamId,
                            "members": row.Members,
                            "location": row.Location,
                            "prediction": prediction,
                            "travelDuration": travel_duration,
                            "predictedWorkingTime": predicted_working_time,
                            "total": predicted_working_time + travel_duration})

    return predictions


def get_clients():
    rows = client.query(
        f"SELECT \
            ClientId, \
            ClientName, \
            CONCAT(PostalCode, '-', City) as Location \
        FROM `{PROJECT_NAME}.Clients` \
        ORDER BY ClientId ASC").result()
    teams = []
    for row in rows:
        teams.append({"clientId": row.ClientId,
                      "name": row.ClientName,
                      "location": row.Location})

    return teams


def get_task_types():
    rows = client.query(
        f"SELECT \
            DISTINCT TaskType \
        FROM `{PROJECT_NAME}.CompletedTasks` \
        ORDER BY TaskType ASC").result()
    types = []
    for row in rows:
        types.append(row.TaskType)

    return types
