# HOW TO RUN

First the 'export_env.sh' must be converted to an executable to do this run the following command.
`chmod +x export_env.sh`

Now the script will  log you onto the MST Campus VPN so that you can connect to our Database in DBeaver. Be sure to add the DBeaver username and password in the file before running. 

`./export_env.sh`

Then simply run the following command to start up the backend server.

`./rest_api.py`

Now the backend should be running on your computer, if you're using a Linux machine then the VPN connection the campus must be open for the rest server to work.

<br/>
You also need to install the following files in pip3

`pip3 install Flask --user`
<br/>

`pip3 install Flask-Cors --user`
<br/>

`pip3 install Flask-RESTful --user`
<br/>

`pip3 install cx_Oracle --user`
<br/>

`pip3 install pandas --user`
<br/>
