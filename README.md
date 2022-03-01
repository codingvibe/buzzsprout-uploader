# buzzsprout-uploader
Simple script to upload a podcast to Buzzsprout.

## Requirements
Install via pip:

`pip install -r requirements.txt`

## Run the script

`python buzzsprout_uploader/buzzsprout_uploader.py <arguments>`

## API Key and Podcast ID

A Buzzsprout API key and the ID of your podcast are both required to run this script. You can obtain both by logging in to Buzzsprout and navigating to https://www.buzzsprout.com/my/profile/api

### Command line arguments
| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| --audio | path to audio file to upload | true | N/A |
| --title | title of the podcast | true | N/A |
| --description | description of the podcast | true | N/A |
| --tags | space separated list of tags for the podcast | false | [] |
| --publish-at-date | date to publish video (format is YYYY-MM-DD) | false | |
| --publish-at-time | time to publish video (iso format) | false | |
| --episode-number | episode number of this upload | false | If not supplied, most recent episode number + 1 |
| --season-number | season number for this upload | false | If not supplied, most recent episode number |
| --private | whether or not this upload should be private | false | false |
| --explicit | whether or not this upload is explicit | false | false |
| --email-after-process | whether or not to email after processing is done | false | true |
| --api-key | api key to use to upload | true | N/A |
| --podcast-id | ID of the podcast to upload to | true | false |

