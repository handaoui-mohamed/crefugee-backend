## Installation Commands

1- Install python 2.7.*

2- Install pip : https://docs.python.org/2/installing/

3- Install virtualenv: 
    
        pip install virtualenv

4- Go inside the project folder, create a virtual environment: 

        virtualenv flask

5- To go into the virtual environment:

        Linux: source bin/activate

        Windows: .\flask\Scripts\activate

6- Install project requirements:

        pip install -r requirements.txt

7- Create DataBase: 
    
        python db_create.py

8- Add Tags to DB: 
    
        python db_add_tags.py

9- Run server on dev mode: 

        python run.py

10- Run server on prod mode: 

        python runp.py




## Git

1- Clone repo

2- Work in dev branch: 

        git checkout develop

3- Push: 
    
        git push origin develop

4- Pill: 

        git pull --rebase

