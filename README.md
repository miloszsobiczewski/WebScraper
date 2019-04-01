# WebScraper
Web Scraping API 
## Installation
Please clone this GIT repository
```buildoutcfg
git clone https://gitlab.com/miloszsobiczewski/webscraper.git/
```
Change directory to webscraper and run
```buildoutcfg
sudo docker-compose up
```
After docker image installation is complete you can find the application 
running in you browser under following url:
```buildoutcfg
http://0.0.0.0:8000/api/
```
## How to use

### Options

Interface of the API allows to select few options:
* Site url - url that will be the target of web scraping
* Text indicator - indicates whether or not to scrap and save text to local 
system
* Image indicator - indicates whether or not site will be scanned for images 
and then saved to local system if possible

### Database 

Standard Django SQLite database was used. Following information are stored for 
scraping tasks:
* site url
* status
* text indicator
* image indicator
* text file location (if saved)
* image files locations (if saved)
* schedule date 

All data regarding scheduled tasks can be find here:
```buildoutcfg
http://0.0.0.0:8000/admin/api/task/
```
login: `new`

password: `New_12345`

Scraped files are stored in __./static/api/TAKS_ID__ directory
### Tasks

Mentioned database was also used for scraping tasks monitoring.
Additionally Task status dashboard was created under following url:
```buildoutcfg
http://0.0.0.0:8000/api/tasks/
```
Dashboard allows to check the current task status and download scraped data (
text and images ) for all completed ones. 

## Unit Tests
For all dedicated methods used in the service unit tests were written.
To run unit tests use following command with appropriate _CONTAINDER_ID_:
```buildoutcfg
sudo docker exec -it CONTAINDER_ID python unittests.py
```

## Details

### Scraping options
1. Provided site url will be checked for response availability.
2. Either text or image - one of the scraping options needs to be selected.

### Done and "to do"
1. Tested and working well on urls like:
    * https://semantive.pl/blog/
    * https://msobiczewski.pythonanywhre.com/
2. Not very effective on following ones:
    * https://www.wykop.pl/
    * https://www.wp.pl/
3. It is not 100% REST API, though it can be transformed using Django Rest 
Framework - which a did not have the opportunity to use so far.
