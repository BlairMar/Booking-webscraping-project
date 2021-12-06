# booking_scraper

booking_scraper is a script to scrape booking.com with user input, containerised in Docker to be used on local or virtual machines.

## Usage

As a docker container:

```
docker run -it caryswilliams/booking_scraper
```

Note that using -it flags allows user input to be determined. Without these flags, default values will be used (1st Jan check-in, 10th Jan check-out; Spain; 2 adults; 0 children; 1 room).

Input to specify:

```
Enter Travel date (yyyy-mm-dd): 2022-01-01 #check-in date
Enter Travel date (yyyy-mm-dd): 2022-01-10 #check-out date
Enter the desitnation of your choice : Spain #can enter any country or city, defining which it is in the next input
Is this a country? [Y/N]:Y 
How many adults are travelling? (max = 30): 2 
How many children are travelling?(max = 10): 2
Please input the age of child 1:  1 #if more children are inputted, use is asked for each child's age
Please input the age of child 2:  5
How many rooms do you need?: 2
```


If running on an ec2 instance, this will need to be more powerful than t2.micro.

The scraper is not yet available as a standalone module to install. The script makes use of uploading to an aws s3 bucket, if the script file is downloaded from this repository it will require an aws_session.py file (replacing 'XXXXX' for your credentials):

```
import boto3
session = boto3.Session(
    aws_access_key_id='XXXXXXXXXX',
    aws_secret_access_key='XXXXXXXXXXXXXXXXX',)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)