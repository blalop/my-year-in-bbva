# My year in BBVA

A Dash application mean to show the data about your expenses, incomes...

Based on [this post from Dan Harrinson](https://towardsdatascience.com/creating-my-own-year-in-monzo-using-python-pandas-e866a17c3509) about how to implement [Monzo's useful review of the year](https://yearinmonzo.com/2020/), this [Dash](https://plotly.com/dash/) application provides a handy way to control your finances from the monthly statements that BBVA provides via its website.

The requirements can be found in the Pipfile. This app uses [bbva2pandas library](https://github.com/blalop/bbva2pandas) to extract the data from those statements.

## Running

## From docker image

```
docker run -v directory/with/monthly/statements:/documents -p 8050:8050 blalop/my-year-in-bbva
```

## From bare metal

Set up virtual env:
```
pipenv install -r requirements.txt
```

Config a .env file, and run the app:
```
DIRECTORY=directory/with/monthly/statements pipenv run python3 yearinbbva
```
