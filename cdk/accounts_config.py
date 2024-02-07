
from aws_cdk import core

accounts = {
    'Dns': {
        'account': '366442540808',
        'region': 'us-east-1'
    },
    'Prod': {
        'account': '366442540808',
        'region': 'us-east-1'
    },
    'Beta': {
        'account': '944207523762',
        'region': 'us-east-1'
    },
    # Brandy Barfield, Capstone Spring 2022
    'Dev-bbarfie': {
        'account': '658042180345',
        'region': 'us-east-1'
    },
    # Joshua Little, Capstone Spring 2022
    'Dev-jlittl8': {
        'account': '577283310524',
        'region': 'us-east-1'
    },
    # Jonathan Daniel, Capstone Spring 2022
    'Dev-jmdanie': {
        'account': '293923494964',
        'region': 'us-east-1'
    },
    # Kellen James, Capstone Spring 2022
    'Dev-kellen': {
        'account': '649319584955',
        'region': 'us-east-1'
    },
    # Mike Brandin, Capstone Spring 2022
    'Dev-mbrandi': {
        'account': '123330062850',
        'region': 'us-east-1'
    },
    # Dillon Ranwala, Capstone Fall 2022
    'Dev-dranwal': {
        'account': '149497240198',
        'region': 'us-east-1'
    },
    # Le Nguyen, Capstone Fall 2022
    'Dev-ltn': {
        'account': '446249877359',
        'region': 'us-east-1'
    },
    # John Pascoe, Capstone Fall 2022
    'Dev-jepasco': {
        'account': '810878154118',
        'region': 'us-east-1'
    },
    # Aaron Gonzales, Capstone Fall 2022
    'Dev-awgonza': {
        'account': '684082786745',
        'region': 'us-east-1'
    },
    'Dev-soll': {
        'account': '104308618712',
        'region': 'us-east-1'
    },
    'Dev-lrboyer': {
        'account': '744918461173',
        'region': 'us-east-1'
    },
}

accounts = {
    domain: core.Environment(
        account=accounts[domain]['account'],
        region=accounts[domain]['region'],
    )

    for domain in accounts
}
