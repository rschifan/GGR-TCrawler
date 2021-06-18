# GGR-TCrawler

Template for a simple Twitter API crawler (v2). 

Clone the repository:

    git clone https://github.com/rschifan/GGR-TCrawler.git
    cd GGR-TCrawler

Copy the **config.ini.default** file in a new **config.ini** document and edit the different sections according to your credentials and preferences. 

The current implementation of **MongoDBTCrawler** stores the results of the API calls in a MongoDB instance (you should set up a running MongoDB server independently and update the section MONGODB of the config.ini file top reflect your settings). Edit the file **MongoDBTCrawler.py** to change the name of the mongodb collection according to your preferences.

To customize this behavior the results of the API calls you shoud extends the class **TCrawler** and customize the method **save()** for exmaple allowing to stores the tweets in a textual file.

The parameters of the API calls can be set using the config.ini configuraiton file or through the methods **set_params()**, **set_api_url()** and **set_query()**
