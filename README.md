# booking_scraper

booking_scraper is a script to scrape booking.com with user input, containerised in Docker to be used on local or virtual machines.

## Usage

As a docker container:

```
docker run -it caryswilliams/booking_scraper
```

Note that using -it flags allows user input to be determined. Without these flags, default values will be used.

Input to specify:


If running on an ec2 instance, this will need to be larger than t2.micro.

The scraper is not yet available as a standalone module to install. The script makes use of uploading to an aws s3 bucket, if the script file is downloaded from this repository it will require an aws_session.py file (replacing 'XXXXX' for your credentials):

```
import boto3
session = boto3.Session(
    aws_access_key_id='XXXXXXXXXX',
    aws_secret_access_key='XXXXXXXXXXXXXXXXX',)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)