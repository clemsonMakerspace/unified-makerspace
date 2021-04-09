=========================================
The MakerSpace Developer's Documentation
=========================================

Overview
=============

Introduction
-------------
This is the documentation for the MakerSpace API. It is divided into sections
based on functionality. Each page documents for each endpoint, the endpoint url,
the permissions, the parameters, and a brief description. The `models` page
has specifications for all the objects that will be exchanged by the api.

Terminology
------------

Entities
~~~~~~~~~
There are two entities that will be using the
MakerSpace: `Users` and `Visitors`.

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
MakerSpace. Creating an account will at a minimum grant them
access to the MakerSpace, but could facilitate deeper
interaction in the future (e.g. uploading personal works).

.. note::

    One person may have both a `User`
    and `Visitor` account with the same email address.
    The account type may not be changed after creation.


Example Usage
---------------

User
~~~~~~

Joe is a maintainer who wants to be able to view and resolve tasks created by his manager, Ivan. He finds the registration page and marks the checkbox that indicates he works at the MakerSpace. He submits the registration form and is prompted for a user token on the next page. He asks Ivan, who generates a new, temporary token from his profile page. Joe enters the token, and his registration is complete. He is redirected to the login page, where he can now use his new credentials.



Visitor
~~~~~~~~

Beck’s friends constantly tell her about how amazing the MakerSpace is, so she finally makes plans to visit it next week. Before going, she completes the Canvas tutorial, where she is prompted to create an account with the MakerSpace. She is redirected to the login page, where she enters her email address and creates a password. Completing the form, she is asked for a few more details on the next page, such as her name, major, degree type, and the hardware id of her TigerCard. She honestly enters this information and she is asked to validate her email address on the next page. Upon validating her email address, she finishes the authentication process and can now visit the MakerSpace.


Contents
=========
.. toctree::
   :maxdepth: 5
   :caption: Contents:

   admin
   auth
   tasks
   machines
   visitors
   models
   example