## This project is build for fetching data from Stack overflow using its api. The project is build using flask and redis.


## System Flow

1. Postman hits the api for getting the data
2. Api perform following task

      1. Api calls the function with unique id as parameter which checks the redis status
      2. Function first check whether the unique id of user is present in redis or not 
      3. If unique id is not present then unique id, count, current time is added in redis and send True status with a meassage of remaining hit count as a response to api .
      4. If unique id is found in redis, then.
           
           1. Function fetch the data with that unique id
           2. The difference is checked between current time and the time stored in redis
           3. If the difference is less than 60 seconds then it checks the hit count, if hit count is less than 5 , then the count is incremented by 1, and True status with a message of remaining hit count is sended as response to the api .
           4. If the difference is less than 60 seconds and hit count is more than 5 then it send status as False and message as wait for some time as response to api
           5. If difference is more then 60 seconds then count and time in redis is updated and True status with a message of remaining hit count is sended as response to the api
           
      4. After getting response from redis if response is True then.
       
           1. It check whether that data is present in redis or not, if that data is present then it is ended as response
           2. If data is not in redis than, the stack overflow url is hit and the response is saved to redis and that response is sended by the api as response to the postman
           
      5. If response from redis is false then api passes the same message as a response to the postman
          
## Api

* get_stack_overflow_data- this api is used to hit to the stack overflow to get the data as response

      curl --location --request GET 'http://127.0.0.1:5000/stack?q=convert%20String%20to%20dict%20python&answers=1&body=String%20to%20dict&nottagged=json;list&     
      tagged=python&title=&views=10&uid=20'

## Function

* check - this is the function which is checking the hit limit within one minute.
