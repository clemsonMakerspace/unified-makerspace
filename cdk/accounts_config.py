
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
    'Dev-mhall6': {
        'account': '832276593114',
        'region': 'us-east-2'
    },
    'Dev-ddejesu': {
        'account': '531821635194',
        'region': 'us-east-1'
    },
    'Dev-dwball': {
        'account': '404054142041',
        'region': 'us-east-1'
    },
    'Dev-kejiax': {
        'account': '110911207619',
        'region': 'us-east-1'
    },
    'Dev-weiminl': {
        'account': '616834645561',
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
