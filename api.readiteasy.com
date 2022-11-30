server {
	server_name api.readiteasy.com;

	location = /favicon.ico { access_log off; log_not_found off; }
        location /staticfiles/ {
            root /home/webadmin/readiteasy-backend/staticfiles;
        }
	
	location / {
            include proxy_params;
            proxy_pass http://unix:/home/webadmin/readiteasy-backend/ReadItEasy.sock;
        }	

}


