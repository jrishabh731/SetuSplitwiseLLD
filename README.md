# Setu SplitWise LLD

## Objectives:
- Add users; Define groups and assign people to group. One user can be part of multiple groups.
- User can add an expense related to a specific group
   1.Equal split – Expense 100 Rs, 10 ppl pay 10 rs
   2.Exact split – Expense 100 Rs, A - 20 rs, B pay 18 rs, C–M pay 6 rs
- User should be able to view all transactions along with pending amount
    1. Tagged to group
    2. Filtered to specific period
- [Bonus] User can settle with another user
   1. Be group specific
   2. Full settlement of pending amount

## Endpoint:
   * Users
     - POST : /users/
     - GET: /users?userID=a

### Steps to run:
1. Git clone the repo.
2. Ensure docker is installed and working.
3. From SetuSplitwiseLLD directory, do docker-compose up -d --build
4. docker-compose ps to check if services are running
5. Credentials for postgres
   - Username : postgres
   - password : postgres
   - DB : test_db
6. Swagger page can be accessed at http://localhost:80/docs
7. For API usage and sample data please import Setu.postman_collection.json in postman



### Schema for the Splitwise
##### Users
UserID, UserName 
##### Groups
groupID, groupName, groupMembers
##### GroupMembership - Stores the mapping for groupId and userID
groupID, UserID
##### Expenses - Stored an individual expense which is further divided into multiple transactions 
expenseID, userID, groupID, amountPaid, splitType, expenseTimestamp
##### Transactions - Each trans is part of an expense and denoted amount borrowed by userBorrower from userLender
transactionID,transactionTimestamp, expenseID, groupID, userBorrower, userLender, amountPaid, settlementTimestamp,SettlementStatus
##### Overview
userIDLender, userIDBorrower, groupID, amount

Approach:
As we have to calculate the amount owed by an user to another user very frequently, I have created 
another table Overview. It stores total amount pending between Lender and Borrower. This table is updated 
when someone adds an expense and respective lending and borrowers trans amounts are updated.

1. We can query for UserID and fetch total amount owed to them by other users
Select userIDLender, Sum(amount) From Overview where userIDLender='a';
2. We can query for UserID and fetch total amount they owe other users
Select userIDBorrower, Sum(amount) From Overview where userIDBorrower='a';
3. We can query for total amount owed between two users.
Select userIDLender, userIDBorrower, Sum(amount) From Overview where userIDBorrower='a' and userIDLender='b';;
4. All above queries can be also filtered on groupID.

Project Structure:
```
├── database
│   └── postgres
├── postgres-data
└── services
    ├── source
    │ ├── config
    │ ├── handlers
    │ ├── models
    │ ├── schema
    │ ├── service
    │ ├── main.py
    └── unittest
        ├── testcase
        └── testdata

```
 - Config folder has the db related functions. 
 - Handlers are specific files to handle api requests and route them to responsible service
 - Models stores the ORM model.
 - Schema has the pydantic models
 - Service has interfaces and services(implemented through interfaces). These interfaces cab be used to implement
    new services.
 - Unittest has testcase and testdata.
 - Database can have database related scripts or configs, not used currently.

## Sample Outputs:
1. GET Expenses
 Request: 10.61.21.144:80/expenses?userID=b
```
{
    "transactions": [
        {
            "transactionTimestamp": "2022-07-27T09:07:26.060742",
            "amountPaid": 20.0,
            "expenseAmount": 100.0,
            "group": "office"
        },
        {
            "transactionTimestamp": "2022-07-27T09:06:03.157931",
            "amountPaid": -80.0,
            "expenseAmount": 100.0,
            "group": "office"
        },
        {
            "transactionTimestamp": "2022-07-27T09:05:49.977635",
            "amountPaid": -50.0,
            "expenseAmount": 100.0,
            "group": "office"
        },
        {
            "transactionTimestamp": "2022-07-27T09:07:26.056060",
            "amountPaid": -80.0,
            "expenseAmount": 100.0,
            "group": "office"
        }
    ],
    "detail": {
        "borrowed": -130.0,
        "lend": 20.0,
        "self": -80.0
    }
}
```
------------------------------------------------------------------------------------
Request: 10.61.21.144:80/expenses?userID=b
Response: 
```
{
    "transactions": [
        {
            "transactionTimestamp": "2022-07-27T09:06:03.157931",
            "amountPaid": 80.0,
            "expenseAmount": 100.0,
            "group": "office"
        },
        {
            "transactionTimestamp": "2022-07-27T09:05:49.977635",
            "amountPaid": 50.0,
            "expenseAmount": 100.0,
            "group": "office"
        },
        {
            "transactionTimestamp": "2022-07-27T09:05:49.971588",
            "amountPaid": -50.0,
            "expenseAmount": 100.0,
            "group": "office"
        },
        {
            "transactionTimestamp": "2022-07-27T09:06:03.153088",
            "amountPaid": -20.0,
            "expenseAmount": 100.0,
            "group": "office"
        }
    ],
    "detail": {
        "borrowed": 0,
        "lend": 130.0,
        "self": -70.0
    }
}
```

------------------------------------------------------------------------------------
## Users
Request: GET 10.61.21.144:80/users?userID=a 
Response:
```
{
    "record": {
        "userName": "a",
        "userID": "a"
    }
}
```

Request: POST 10.61.21.144:80/users?userID=a 
Payload:
```
{
    "userName": "b",
    "userID": "b"
}
```
Response:
```
{
    "status": true
}
```

------------------------------------------------------------------------------------
## Groups 
Request: GET 10.61.21.144:80/groups?groupID=2
Response:
```
{
    "record": {
        "groupName": "office",
        "groupID": 2
    }
}
```

Request: POST 10.61.21.144:80/groups
Payload:
```
{
    "groupName": "office",
    "groupMembers": ["b", "c"]
}
```
Response:
```
{
    "groupID": [
        2
    ]
}
```

------------------------------------------------------------------------------------
## Expenses - Equal
Request: POST 10.61.21.144:80/expenses
Payload:
```
{
    "userID": "a",
    "groupID": 1,
    "amountPaid": 100,
    "splitType": "equal",
    "splitMap": {}
}
```
Response:
```
{
    "status": true
}
```

## Expenses - Exact
Request: POST 10.61.21.144:80/expenses
Payload:
```
{
    "userID": "b",
    "groupID": 2,
    "amountPaid": 100,
    "splitType": "exact",
    "splitMap": {
            "c": 20,
            "b": 80
        }
}
```
Response:
```
{
    "status": true
}
```
