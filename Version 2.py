
# import dotenv
# dotenv.load_dotenv()

DATABASE_ID = 'DATABASE_ID'
IN_ACTIVE = "IN_ACTIVE"

TOTAL = 'total'
ID = "$id"
TEAM_ID = "teamId"
MEMBERSHIPS = "memberships"
SUCCESS = "success"
JOINED = "joined"
FALSE = "false"
TRUE = "true"

def createClient():
    from appwrite.client import Client
    import os
    client = (
        Client()
            .set_endpoint(os.environ['ENDPOINT'])
            .set_project(os.environ['PROJECT_ID'])
            .set_key(os.environ['API_KEY'])
    )
    return client

def fail(context):
    return context.res.json({SUCCESS:FALSE})

def isDatabaseActive(tables, database: str):
    from appwrite.services.tables_db import TablesDB
    from appwrite.query import Query
    tables: TablesDB = tables
    result = tables.list_rows(
        database_id="MANAGEMENT",
        table_id="USERS",
        queries=[Query.equal(DATABASE_ID, database)]
    )

    if result[TOTAL] == 0:
        return False

    return result["rows"][0]["IS_ACTIVE"]

def hasNotUserJoined(membership) -> bool:
    from datetime import datetime as dt
    from datetime import timezone
    if len(membership["joined"]) == 0:
        return True
    joinDate = dt.fromisoformat(membership["joined"])

    if (dt.now(tz=timezone.utc) > joinDate):
        return False
    
    return True

def main(context):
    try:
        client = createClient()
        from appwrite.services.users import Users
        import json
        users = Users(client)

        context.log(context.req.body)
        info = context.req.body.replace("'", "\"")
        info = json.loads(info)
        uid = info[ID]

        memberships = users.list_memberships(user_id=uid)

        if (memberships[TOTAL] == 0):
            return fail(context)
        
        from appwrite.services.tables_db import TablesDB
        tables = TablesDB(client)
        
        if (memberships[TOTAL] == 1):
            dbid = memberships[MEMBERSHIPS][0][TEAM_ID]

            if hasNotUserJoined(memberships[MEMBERSHIPS][0]):
                return context.res.json({SUCCESS:FALSE, JOINED:FALSE})

            isActive = isDatabaseActive(tables, dbid)
            if isActive:
                return context.res.json({SUCCESS:TRUE, DATABASE_ID:dbid})
            return context.res.json({SUCCESS:FALSE, IN_ACTIVE:1})
        
        databases = []

        for membership in memberships[MEMBERSHIPS]:
            if hasNotUserJoined(membership):
                continue
            databases.append(membership[TEAM_ID])

        active_databases = []
        inactive = 0

        for database in databases:
            isActive = isDatabaseActive(tables, database)
            if isActive:
                active_databases.append(database)
            inactive += 1

        if len(active_databases) == 0:
            return context.res.json({SUCCESS:FALSE, IN_ACTIVE:inactive})
        
        if (len(active_databases) == 1):
            active_databases = active_databases[0]

        return context.res.json({SUCCESS:TRUE, DATABASE_ID:active_databases})

    except Exception as e:
        context.log("Error getting membership: " + str(e))
        return fail(context)

# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     load_dotenv()
#     client = createClient()
#     users = Users(client)
#     memberships = users.list_memberships(user_id="695c7e392942d4130ee5")
#     print(memberships)
#     try:
#         if len(memberships["memberships"][0]["joined"]) == 0:
#             print("A. Not joined")
#             exit()
#         join = dt.fromisoformat(memberships["memberships"][0]["joined"])
#         print(f"Joined: {join}")
#         print(f"joined utc: {join.utcoffset()}")
#         print(f"joined utc: {join.tzinfo}")
#         print(f"now: {dt.now()}")
#         print(f"now: {dt.now(tz=ZoneInfo('UTC'))}")
#         if (dt.now(tz=ZoneInfo('UTC')) > join):
#             print("joined in the past")
#         print("joined: ", join)

#     except Exception as e:
#         print(e)
#         print("B. Not joined")