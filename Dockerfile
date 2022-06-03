FROM python:3.10

WORKDIR /usr/src/app

# Optimization step. This will be cached and then downstream steps will see nothing 
# has changed and will also use the cache
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# This step comes after because we will likely change the source code between builds.
# We dont want to rerun the longest step of the build which is the prior step to this.
COPY . .

# Host 0.0.0.0 = any ip address assigned by host
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]