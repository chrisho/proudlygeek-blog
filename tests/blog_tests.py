# -*- coding: utf-8 -*-
"""

	Blog Tests
	~~~~~~~~~~


	Tests the blog application.

	:copyright: © 2010 by Gianluca Bargelli.
	:license: MIT, see LICENSE for more details.
"""

import os
import unittest
import tempfile
from proudlygeek import blog

class BlogTestCase(unittest.TestCase):
	def setUp(self):
		"""Before each test, set up a sample database"""
		self.db_fd, blog.app.config['DATABASE'] = tempfile.mkstemp()
		self.app = blog.app.test_client()
		blog.init_db(testdb = True)
	
	def tearDown(self):
		"""Get rid of the database again after each test."""
		os.close(self.db_fd)
		os.unlink(blog.app.config['DATABASE'])

	# Helper Functions
	def login(self, username, password):
		"""Helper function for user login."""
		return self.app.post('/login', data = {'username':username,
											   'password':password
											  }, follow_redirects = True)
	def logout(self):
		"""Helper function for user logout."""
		return self.app.get('/logout', follow_redirects = True)

	def test_empty_db(self):
		"""Tests if an initial database is empty."""
		rv = self.app.get("/")
		assert 'No entries here so far' in rv.data
	
	def test_login_logout(self):
		"""Tests if login and logout works correctly."""
		# Testing GOOD username, GOOD password	 
		rv = self.login('test','test')
		assert 'You were logged in' in rv.data
		# Testing logout after a successful login
		rv = self.logout()
		assert 'You were logged out' in rv.data
		# Testing GOOD username, BAD password
		rv = self.login('test','rest')
		assert 'Invalid password' in rv.data
		# Testing BAD username, BAD password
		rv = self.login('pest','rest')
		assert 'Invalid username' in rv.data
		# Testing logout without a login


if __name__ == '__main__':
	unittest.main()