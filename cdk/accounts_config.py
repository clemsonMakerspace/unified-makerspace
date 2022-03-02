
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
    'Dev-kellen' : {
        'account': '649319584955',
        'region': 'us-east-1'
    },

    # Joshua Little, Capstone Spring 2022
    'Dev-jlittl8': {
        'account': '577283310524',
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
