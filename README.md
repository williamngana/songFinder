# songFinder

This is a simple flask app that will return you tracks based on the parameters that you give it. 
## Steps to Run:

1. Create a python3 virtual environment 
2. Navigate into that directory an run 'pip install -r requirements.txt'
3. run 'export FLASK_APP=flaskr' and 'export FLASK_ENV=development'
4. then finally 'flask run' and the dev servere  will be found [here](http://127.0.0.1:5000/) 

## Endpoints
There is only one endpoint which is /playlist/
required arguments 
category(Str) -> for now the list of categories that are supported are Acoustic Blues,Chicago Blues,Blues, and Rap
songno(int) -> this is what song on the playlist we are on
alreadyplayed(List) -> a list of track_ids that have already been played
token(str) -> api token

### example call:
playlist?category=Blues&songno=2&alreadyplayed=75175204,50184104&token=Token :
- this will return one song with similar lyrics to the last song just played

playlist?category=Blues&songno=0&alreadyplayed=[]&token=Token
- this will return 2 songs with from the category specified as it is the start of the playlist

