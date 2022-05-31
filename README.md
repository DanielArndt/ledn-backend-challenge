# ledn-backend-challenge

## Notes

I tried to focus on a few priorities
- Code readability
    - Including auto formatting to keep everything consistent: `black`, `isort`
- API structure / readability
    - Including auto generated documentation (see `/docs` in the browser)
- Portability / ease of development
    - Docker for a reproducible environment
    - Dev environment with auto reload on code change for quick iteration
    - No external dependencies required (beyond docker)
        - Can run the platform and tests without installing anything except docker
        - Should run on any OS and machine without conflicts
    - Very simple integration tests
        - Allows quick iteration, with a reasonable chance of not breaking things
        - However, the tests are not exhaustive. They do not catch all edge cases, but should address the main requirements
        - Some tests depend on the sample data. They are not idempotent.
    
## Compromises / notable omissions

Many compromises were made to limit the time spent, and scope.

- I used Python instead of Typescript due to familiarity. I have dabbled in Typescript, but have not used it extensively.
- In an attempt to achieve a middle ground on familiarity, I used Mongo DB (which I am also unfamiliar with). Therefore, my approach on some database related tasks may be lacking.
    - I did not make use of any indexing, for example.
- Lacks extensive error handling such as database insert errors
- Tests are not exhaustive of all edge cases and lack rigidity (see priorities above)
- No unit tests
- Basic auth for security. 
    - The wording in the README ("the admin user") suggested some level of security, but I didn't want to spend too much time on authentication.

## Architecture

The `docker-compose.yml` file defines two services, the database (Mongo DB), and the Python API. See the corresponding directories (`mongodb`, `python-api`).

### Mongo DB
On first launch, Mongo DB will load some data from the `seed-data` directory (see `mongodb/import-data.sh`). This container is only accessible via the Python API, and is not exposed externally.

### Python API
The Python API connects to the database using the credentials in `backend.env`. The Python API uses HTTP Basic Auth for security, and allows only a single user: the `admin` user. The password (default: `ledn_admin`) can be configured in `backend.env`. A rebuild of the docker containers is required for any changes to the environment variables. 

## Requirements

- `docker`
- `docker compose`

## Build and run the platform

```bash
docker compose up --build
```

The API will be exposed on port `8000`. See http://localhost:8000/docs

## Run integration tests

Note: These tests will only pass sucessfully with the small data set pre-seeded (default). They are not idempotent, and were designed for a developer to iterate quickly more than they were designed for well tested code. 

While the docker compose instance is up and running, run the following

```bash
docker compose exec -it python_api sh -c "pytest test/test_api.py"
```

An additional test exists in `test/test_large_data.py` which is a very basic test that creates 150000 new transactions, and then checks the balance of the user has updated accordingly. This is simply to validate the API works with large data sets and is not robust in any sense. It takes several minutes to run since no optimization was done here.

## Requirements

Using HTTP Basic Authentication (username: `admin`, password: `ledn_admin`), the user should be able to make the following requests to meet the requirements:

> The admin user should be able to get an account and its current balance (the data provided may contain negative balances).

* `GET /accounts/{email}`
* `GET /accounts/{email}/balance`

> The admin user should be able to debit and credit an account;

* `POST /transactions/` with `type` of `credit` or `debit`
    
    Example body: 
    ```json
    {
        "userEmail": "user@email.com",
        "amount": 10,
        "type": "credit",
        "createdAt": "2022-05-31T18:08:57.752Z"
    }
    ```

> The admin user should be able to make an amount transfer from one user to another.

* `POST /transfers/`

    Example body:
    ```json
    {
        "fromEmail": "fromuser@email.com",
        "toEmail": "touser@email.com",
        "amount": 10,
        "createdAt": "2022-05-31T18:13:32.374Z"
    }
    ```

The docs located at http://localhost:8000/docs will provide more details along with sample JSON. See the tests in `python-api/test/tests_api.py` for more realisitic examples.