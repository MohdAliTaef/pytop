# pytop

To Run extraction.py first we need to have set up influxdb with the defult settings and have it running
the script will create the database with the centos_top and input the data into series centos_processes
the following arguments need to be passed when running extraction.py
        IP Address
        Port
        VM Username
        VM Password
        Intervals in seconds
   example: python extraction.py 127.0.0.1 2222 root admin 5
  
 serve.py will serve a react page at localhost:5000 and the GET API would be localhost:5000/data?ip=127.0.0.1
