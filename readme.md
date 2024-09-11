1.  install virtual environment
    $   python3 -m venv venv

2.  activate virtual environment
	linux
    $   source venv/bin/activate
    	windows
    $	venv\Scripts\activate ( klo ganemu cari sendiri file activatenya ada dimana, aku lupa ) wkwk
    
3.  install requirement
    $   pip install requirements.txt

4.  run scraper to get json file
    $   python scraper.py

5.  get api
    $   python app.py
    $   GET http://localhost:5000/api/posts/your_username
        or
        http://localhost:5000/api/posts/username (browser)
