server {
	server_name api.readiteasy.com;

	location = /favicon.ico { access_log off; log_not_found off; }
        location /staticfiles/ {
            root /var/www/readiteasy/readiteasy-backend/staticfiles;
        }
	
	location / {
            include proxy_params;
            proxy_pass http://unix:/var/www/readiteasy/readiteasy-backend/ReadItEasy.sock;
        }	

}


