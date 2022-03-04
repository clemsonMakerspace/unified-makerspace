
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
}

accounts = {
    domain: core.Environment(
        account=accounts[domain]['account'],
        region=accounts[domain]['region'],
    )

    for domain in accounts
}
