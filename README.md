Very Silly Service for tracking NYT mini game times
-

Run service: `$ docker-compose up`

API Documentation at: <http://localhost:8080/swagger>

Get into a sandbox with all dependencies: `$ ./scripts/interact.sh`

Unit tests from within sandbox environment: `$ pytest -v test`

Unit tests from outside: `$ ./scripts/test.sh`

End-to-end tests: `$ ./scripts/e2e.sh`



### Explanation for my new developer bud:

 - We're using a lot of `docker` and `docker-compose` for testing and development - read up on these!
 - The routing and logic of the API's different endpoints (i.e., the different urls) is written
 in `app.py` using a microframework called `sanic` which is modeled after the very popular `Flask`.
 Sanic is special in that it is set up for asynchronous ("async") coding (though we're not really
 taking advantage of this in this project).
 - The rest of the real code is in `src/`
 - We're using `sqlalchemy` to model and interact with relational data.
 - `alembic` is for "schema migration". If this service gets heavily used for the next 5 years and a
 bunch of data gets put in it, and then we need to change our data model for a new feature, we would
 have to be very careful not to mess up data when we change our model. Alembic does this for us.
 - `pytest` is our testing framework. It's the best; no one uses the other ones any more. You can
 check how much of our source code is "covered" by our tests by running `$ pytest --cov test`.
 - We're using **environment variables** to configure our application. In `docker-compose.yml`
 there is a section called "environment" where these variables are defined for our development
 environment. These variables are things that we might want to change when deploying this app in 
 different environments (like on a test server vs a production server). Here we are mostly using them
 to point us at the database we want to use (which, since we are in a development environment, is a 
 postgres DB in a container on your machine).
 - `swagger` generates documentation for web APIs.
 - We're using `poetry` instead of `pip` to manage dependencies. Poetry is the sexiest dependency
 manager.