#### Installing Dependencies
```bash
pip install -r requirements.txt
```

#### Initializing Database
First, you need to install PSQL. Then you need to create proper database. When you're ready, proceed to create tables. Open up your python shell and continue.
```python
from main import db
db.create_all()
```

#### Running Server
```bash
python main.py
```