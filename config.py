#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By Pedro Vapi @2015
# This python file aim is to provide all configuration necessary for using this packageI
#


class DITICConfig:
    """
    This class contains all configuration for this server
    """
    def __init__(self):
        """
        This class contains those special variables.
        All configurations for this server should be done here!
        More important variables:

            # Mapping email to user alias
            self.email_to_user = {
                'email': 'user',
                ...
            }

            # Map user alias to its Kanban limits
            self.user_limits = {
                'user': {
                    'status': value,
                    ...
                }
                ...
            }

            # System configurations (server address, username, pwd, ...)
            self.system = {
                'variable': 'value',
                ...
            }

        :return: None
        """
        self.email_to_user = {
            'pmsilva@student.uc.pt': 'pmsilva',
            'amdra@student.dei.uc.pt': 'André',
            'mcunha@student.uc.pt': 'mcunha',
            'rsaldanha@student.uc.pt': 'rsaldanha',
            'rdias@student.uc.pt': 'rdias',
            'pabreu@student.uc.pt': 'pabreu',
        }
        self.email_limits = {
            'pmsilva@student.uc.pt':{
                'new': 5,
                'open': 2,
                'rejected': 5,
            },
            'amdra@student.dei.uc.pt':{
                'new': 5,
                'open': 2,
                'rejected': 5,
            },
            'mcunha@student.uc.pt':{
                'new': 5,
                'open': 2,
                'rejected': 5,
            },
            'rsaldanha@student.uc.pt':{
                'new': 5,
                'open': 2,
                'rejected': 5,
            },
            'rdias@student.uc.pt':{
                'new': 5,
                'open': 2,
                'rejected': 5,
            },
            'pabreu@student.uc.pt':{
                'new': 5,
                'open': 2,
                'rejected': 5,
            },

        }
        self.list_status = [
            'new',
            'open',
            'stalled',
            'rejected',
            'resolved',
            'deleted',
        ]
        self.system = {
            'working_dir': '/home/andre/PycharmProjects/env/dashboard/ditic_kanban/',
            'summary_file': 'summary',
            'server': 'localhost/rt/',
            'username': 'root',
            'password': 'escuteiros',
            'statistics_file': 'statistics',
        }

    def get_email_to_user(self):
        return self.email_to_user

    def get_system(self):
        return self.system

    def get_user_from_email(self, email):
        """
        Returns the user based on its email address. This information is based on the config file

        :param email:
        :return:
        """
        return self.email_to_user[email]

    def get_email_from_user(self, user):
        """
        Returns the email based on user alias

        :param user: user alias
        :return: email address. If no alias found, return ''
        """
        for email in self.email_to_user:
            if user == self.email_to_user[email]:
                return email
        return ''

    def get_users_list(self):
        """
        Returns the list of users (not it's emails!)

        :return:
        """
        return self.email_to_user.values()

    def get_email_limits(self, email, status=''):
        """
        Get the email Kanban limits

        :return: If status is provided, then return that status limits (int).
                 If no status is required, then return the dictionary with all limits
        """
        if status:
            if email not in self.email_limits.keys() or status not in self.email_limits[email]:
                return 0
            return self.email_limits[email][status]
        else:
            if email not in self.email_to_user.keys():
                return {}
            return self.email_limits[email]

    def get_list_status(self):
        return self.list_status

    def check_if_user_exist(self, user):
        """
        Check if the user (not it's email) exist.
        The user is defined in the config file. You may add there more users

        :param user:
        :return:
        """
        return user in self.email_to_user.values()

    def check_if_email_exist(self, email):
        """
        Check if the email exist.
        The email is defined in the config file. You may add there more emails

        :param email:
        :return:
        """
        return email in self.email_to_user.keys()
