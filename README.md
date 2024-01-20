# NamasteKart-NamasterPyton-Project

#### This is a project demonstration of an ETL process in python

Note - Default behavior is to copy files from the incoming_files folder to the success_files and rejected_files folder based on business logic but this can be changed to moving files from source to destination by making minor changes to the code

Just comment the shutil.copy and uncomment shutil.move to change default copy behavior to move

```python
#copy the rejected file to rejected folder
shutil.copy(csv_filepath, rejected_filepath)

#move the rejected file to rejected folder
shutil.move(csv_filepath, rejected_filepath)
```
