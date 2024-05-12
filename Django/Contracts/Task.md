> Level: Easy 
## Contract RestAPI.

### Data Models
#### Profile

A profile can be either a `client` or a `contractor`.
clients create contracts with contractors. contractor does jobs for clients and get paid.
Each profile has a balance property.

- First Name
- Last Name
- Profession
- Balance
- Type [ `Client` or `Contractor` ]
- UserName
- Password

#### Contract

A contract between and client and a contractor.
Contracts have 3 statuses, `new`, `in_progress`, `terminated`. contracts are considered active only when in status `in_progress`
Contracts group jobs within them.

- Terms
- Status [ `new`, `in_progress`, `terminated` ]
- Client
- Contractor 

#### Job

Contractors get paid for jobs by clients under a certain contract.

- Description
- Price
- Paid
- Payment Date
- Contract

## Requirements 

- Use **Django Rest Framework** to implement this API  https://www.django-rest-framework.org/
- Use Sqlite as DB
- Create User System Login/SignUp/Auth
- Use Token Auth to implement authentication.
- Use Swagger or another Doc generator.
- Create Unit-Tests for all APIs.
- Create Seeds to fill DB.
- Create Async API CLI client utilizer ( optinal ).

   

## APIs To Implement

Below is a list of the required API's for the application.

1. **_GET_** `/contracts/:id` - it should return the contract only if it belongs to the profile calling.

1. **_GET_** `/contracts` - Returns a list of contracts belonging to a user (client or contractor), the list should only contain non-terminated contracts by default. can receive other statuses via url params.

1. **_GET_** `/Profile` - Returns only the current user (client or contractor).

1. **_GET_** `/jobs` - Get all jobs for a user (**_either_** a client or contractor).

1. **_GET_** `/jobs/unpaid` - Get all unpaid jobs for a user (**_either_** a client or contractor), for **_active contracts only_**.

1. **_POST_** `/jobs/:job_id/pay` - Pay for a job, a client can only pay if his balance >= the amount to pay. The amount should be moved from the client's balance to the contractor's balance.

1. **_POST_** `/balances/deposit/:userId` - Deposits money into the balance of a client, a client can't deposit more than 25% of his total of jobs to pay. (at the deposit moment)

1. **_GET_** `/jobs/best-profession?start=<date>&end=<date>` - Returns the profession that earned the most money (sum of jobs paid) for any contractor that worked in the query time range.

1. **_GET_** `/jobs/best-clients?start=<date>&end=<date>&limit=<integer>` - returns the clients who paid the most for jobs in the query time period. limit query parameter should be applied, the default limit is 2.

```
 [
    {
        "id": 1,
        "fullName": "Reece Moyer",
        "paid" : 100.3
    },
    {
        "id": 200,
        "fullName": "Debora Martin",
        "paid" : 99
    },
    {
        "id": 22,
        "fullName": "Debora Martin",
        "paid" : 21
    }
]
```

---- 
## Google Sheets Integrations

1. Setup and collect Auth needed data.
2. Store the transactions only into Sheet.
    - when Client pay for a job.
    - when Client deposit money.
    - Shape the data to make sense.
3. If pay or deposit happens from the sheet it should be respected ( Optional ).
4. if there is external code needed, include it in the repo.


## Required Files
1. Requirements file
2. Docs
3. UnitTesting
4. Achievement file
5. PyLint
   
