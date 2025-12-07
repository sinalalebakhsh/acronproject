# First steps:
    1. migrate
        ```
        python manage.py migrate
        ```

    2.create fake data:
        ```
        python manage.py setup_fake_data
        ```

## create fake data for sample:
```
python manage.py setup_fake_data
```

    ## result:
        Deleting old data...
        Creating new data...
        Adding 100 categories...DONE
        Adding 10 discounts...DONE
        Adding 1000 product...DONE
        Adding 100 customers...DONE
        Adding customers addresses...DONE
        Adding 30 orders...DONE
        Adding order items...DONE
        Adding product comments...DONE
        Adding 100 carts...DONE
        Adding cart items...DONE
        (acronproject)



### prompts
python manage.py sqlmigrate store 0001


### for delete cache
```
git rm -r --cached */__pycache__
```

### test
```
mkdir -p __pycache__
touch __pycache__/test.pyc
```


## pre installed
    ```
    https://dev.mysql.com/downloads/benchmarks.html
    ```



## Make it executable: git-automate.sh
```
chmod +x git-automate.sh
```


### Run it: 
```
./git-automate.sh
```

# MySql Workbwnch:
commends:

    DROP DATABASE store;
    CREATE DATABASE store;



