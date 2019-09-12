# evaluate

# $conda create -n evaluateme django

# $source activate evaluateme

# $pip install -r requirements.txt

# $mkdir -p static_cdn
# $mkdir -p media_cdn


# #########################################################
# ##### COMMANDS FOR MANAGING DJANGO APPLICATION ##########
# #########################################################

# #make migrations
# $python manage.py makemigrations [APPNAME]
# $python manage.py migrate
#
# #collect static
# $python manage.py collectstatic
#
# #To populate database with prepared fixture file:
# $python manage.py loaddata fixture /path/to/fixture/file
#
# # Run server on localhost 
# $python manage.py runserver
#
# # Run server on remote machine (in local network) 
# $python manage.py runserver 0.0.0.0:8000
