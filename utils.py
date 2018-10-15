import re


def valid_food_name(food_name):
    ''' validate food name '''
    regex = "^[a-zA-Z0-9_ ]{4,}$"
    return re.match(regex, food_name)


def valid_food_description(food_description):
    ''' validate food description '''
    regex = "^[a-zA-Z_ ]{5,}$"
    return re.match(regex, food_description)


def valid_person_name(customer_name):
    '''validate person's name'''
    regex = "^[a-zA-Z ]{4,}$"
    return re.match(regex, customer_name)


def valid_destination(destination):
    '''validate destination name'''
    regex = "^[a-zA-Z 0-9]{3,}$"
    return re.match(regex, destination)


def valid_username(username):
    ''' validate username '''
    regex = "^[a-zA-Z0-9]{6,20}$"
    return re.match(regex, username)


def valid_password(password):
    '''validate password , min of 6 chars'''
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]{6,}$"
    return re.match(regex, password)


def valid_email(email):
    ''' validate email '''
    regex = "^[^@]+@[^@]+\.[^@]+$"
    return re.match(regex, email)
