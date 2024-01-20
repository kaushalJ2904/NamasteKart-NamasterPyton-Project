# NamasteKart-NamasterPyton-Project

#### This is a project demonstration an ETL process in python

Note - Default behavious is to copy files from incoming_files folder to success_files and rejected_files folder based on business logic but this can be chagned to moving files from source to destination by making minor changes to code

Just comment the shutil.copy and uncomment shutil.move to change default copy behaviour to move

```python
#copy the rejected file to rejected folder
shutil.copy(csv_filepath, rejected_filepath)

#move the rejected file to rejected folder
shutil.move(csv_filepath, rejected_filepath)
```
