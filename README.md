# video_membership
Creating a Video Membership app using FastAPI &amp; NoSQL 
## Features
- User registration and login
- User subscription management
- Video management (uploading, deleting, updating)
- Video access control
- Saving Secure, Hashed, Passwords
- Video Analytics & Resumable Videos
- Search Engine
## Dependencies
- fastapi
- uvicorn 
- cassandra-driver
- python-dotenv
- email-validator
- argon2-cffi
- pytest
- jinja2
- python-multipart
- python-jose[cryptography]
- algoliasearch


## Installation

1. Clone the repository

```bash
 $ https://github.com/obaraelijah/video_membership.git
 $ cd video_membership
```
2. Install the dependencies:

```bash
 $ pip install -r requirements.txt or pip3 install -r requirements.txt
```
3. Set up the environment variables:
Create a .env file in the project's root directory with the following variables:

```bash
CASSANDRA_HOST=your_cassandra_host
CASSANDRA_KEYSPACE=your_keyspace_name
SECRET_KEY=your_secret_key
ALGOLIA_APP_ID=your_algolia_app_id
ALGOLIA_API_KEY=your_algolia_api_key
```