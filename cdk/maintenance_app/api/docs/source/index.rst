=========================================
The Makerspace Developer's Documentation
=========================================

Overview
=============

Introduction
-------------
This is the documentation for the Makerspace API. It is divided into sections
based on functionality. Each page documents for each endpoint, the endpoint url,
the required permissions to access, the parameters, and a brief description. The `models` page
has specifications for all the objects that will be exchanged by the api.

.. note::
    All dates should be encoded in epoch time (seconds since the start of
    January 1st, 1970).

Terminology
------------

Entities
~~~~~~~~~
There are two entities that will be using the
Makerspace: `Users` and `Visitors`.

Users
```````
`Users` are individuals
who will be using the dashboard. This includes
maintainers and administrators. This enables them, based on
their permissions to create tasks, resolve tasks, see
visitor statistics, view machine information, and
perform administrative tasks.

Visitors
`````````
`Visitors` are students who will be visiting the
Makerspace. Creating an account will at a minimum grant them
access to the Makerspace, but could facilitate deeper
interaction in the future (e.g. uploading personal works).

.. note::

    One person may have both a `User`
    and `Visitor` account with the same email address.
    The account type may not be changed after creation.


Example Usage
---------------

User
~~~~~~

Joe is a maintainer who wants to be able to view and resolve tasks created by his manager, Ivan. He finds the registration page and marks the checkbox that indicates he works at the Makerspace. He submits the registration form and is prompted for a user token on the next page. He asks Ivan, who generates a new, temporary token from his profile page. Joe enters the token, and his registration is complete. He is redirected to the login page, where he can now use his new credentials.



Visitor
~~~~~~~~

Beck’s friends constantly tell her about how amazing the Makerspace is, so she finally makes plans to visit it next week. Before going, she completes the Canvas tutorial, where she is prompted to create an account with the Makerspace. She is redirected to the login page, where she enters her email address and creates a password. Completing the form, she is asked for a few more details on the next page, such as her name, major, degree type, and the hardware id of her TigerCard. She honestly enters this information and she is asked to validate her email address on the next page. Upon validating her email address, she finishes the authentication process and can now visit the Makerspace.



Design
========


Errors
--------
Errors can propagate to the backend in a few ways:

* Client errors that bypass frontend validation (e.g. user attempts to sign up with an existing email)
* Invalid requests made by the frontend,
* Invalid requests made by an external client (e.g. a bad actor).

Regardless of the intention of bad requests, the backend should handle them robustly and return a clear response. This documentation does not provide an exhaustive list of possible errors, as that would be very difficult and unwieldy.

Instead, implementers are strongly encouraged to perform as many backend checks as possible (even those that duplicate frontend validation), and return semantically meaningful responses. Error responses should have a code, an error description, and message. See the `Models.Error` class for more information.

Example Error
~~~~~~~~~~~~~~

.. code-block:: python

    response_body = {
        'code': 400,
        'error': "EMAIL_IN_USE",
        'message': 'There is already an account '
                    'with this email address.'
    }


.. warning::

    Do not provide sensitive information in error responses. The front-end may display messages exactly as provided.


Contents
=========
.. toctree::
   :maxdepth: 3
   :caption: Contents:

   admin
   auth
   tasks
   machines
   visitors
   models
   example