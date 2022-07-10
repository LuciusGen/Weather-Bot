import os
from database.database_requests import DatabaseRequests

os.chdir("../database")
db_requests = DatabaseRequests()


def test_select_city():
    city = db_requests.select_city("-1")[1]

    assert city == "Spb"


def test_select_time():
    time = db_requests.select_time("-1")[1]

    assert time.hour == 7


def test_select_sites():
    sites = db_requests.select_sites("-1")

    assert sites[0] == 'rp5'
    assert sites[1] == 'meteoinfo'
    assert sites[2] == 'foreca'


def test_sites_columns():
    sites = db_requests.sites_in_table

    assert sites[0] == 'rp5'
    assert sites[1] == 'meteoinfo'
    assert sites[2] == 'foreca'


def test_insert_time():
    db_requests.insert_time("-2", "5:00:00")
    assert 5 == db_requests.select_time("-2")[1].hour


def test_insert_site():
    db_requests.insert_sites("-2")
    sites = db_requests.select_sites("-2")

    assert sites[0] == 'rp5'
    assert sites[1] == 'meteoinfo'
    assert sites[2] == 'foreca'


def test_insert_city():
    db_requests.insert_city("-2", "Msk")
    assert "Msk" == db_requests.select_city("-2")[1]


def test_update_time():
    db_requests.update_time("-2", "7:00:00")
    assert 7 == db_requests.select_time("-2")[1].hour


def test_update_city():
    db_requests.update_city("-2", "Spb")
    assert "Spb" == db_requests.select_city("-2")[1]


def test_update_site():
    db_requests.update_site("-2", ["rp5"])

    sites = db_requests.select_sites("-2")

    assert sites[0] == 'rp5'
