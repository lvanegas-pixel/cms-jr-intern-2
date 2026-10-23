# Reto 1

This one was already implemented with commentary included
in code.

# Reto 2

## Fase 1

Authentication and pagination were both included on
`settings.py` in the installed apps and rest framework
section. Then filters and search were added in `views.py`
after taking in consideration both were needed for 
different attributes of Projects and Assets.

## Fase 2

In phase 2, I created multiple postman tests and added them
in `postman/` in json format. Then I proceed to correct
some errors like pagination not ordered or code not having
logs for endpoints. Included also an url for the swagger
auto generated view of the documentation. I'm still 
considering if I should add to the code my already
implemented code in a branch to register users.

## Fase 3

In phase 3, I've added a simple interface to interact with
in index.html and the logic behind in app.js. I've also 
modified the setting.py to change the CORS so that it
doesn't block my attempts to try the frontend.

I've had to implement another filter so that I can get
the assets corresponding to one project directly from a
petition. I'm going to proceed and add another four buttons
to the frontend so that I can show all the projects and
assets, because the pagination limits them on every 
petition.