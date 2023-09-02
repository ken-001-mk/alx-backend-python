#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from requests import HTTPError
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from typing import Dict

class TestGithubOrgClient(unittest.TestCase):
  """Tests GithubOrgClient"""
  @parameterized.expand([
    ("google", {"google": True}),
    ("abc", {"abc": True})
  ])
  @patch(
    'client.get_json',
  )
  
  def test_org(self, org: str, resp: Dict, mocked_fxn: MagicMock) -> None:
    """Test that GithubOrgClient.org returns the correct value."""
    mocked_fxn.return_value = resp
    client = GithubOrgClient(org)
    self.assertEqual(client.org, resp)
    mocked_fxn.assert_called_once_with(
      "https://api.github.com/orgs/{}".format(org)
    )
    
  def test_public_repos_url(self) -> None:
    """Test that the result of _public_repos_url is the expected one."""
    with patch(
      'client.GithubOrgClient.org',
      new_callable=PropertyMock
    ) as mocked_org:
      mocked_org.return_value = {
        "repos_url": "https://api.github.com/orgs/google/repos",
      }
      self.assertEqual(GithubOrgClient("google")._public_repos_url,
                       "https://api.github.com/orgs/google/repos")
  @patch("client.get_json")
  
  def test_public_repos(self, mocked_get_json: MagicMock) -> None:
    """tests that the list of repos is what you expect from the chosen payload."""
    test_payload = {
      'repos_url': 'https://api.github.com/orgs/google/repos',
      'repos': [
        {
          "id": 335035109,
          "name": "ssh-chat",
          "private": False,
          "owner": {
            "login": "google",
            "id": 23423423,
          },
          "fork": False,
          "url": "https://api.github.com/repos/google/ssh-chat",
          "created_at": "2021-01-26T20:38:37Z",
          "updated_at": "2021-01-26T20:38:39Z",
          "has_issues": True,
          "forks": 18,
          "default_branch": "main",
        },
        {
          "id": 335035110,
          "name": "kubernetes",
          "private": False,
          "owner": {
            "login": "google",
            "id": 23423423,
          },
          "fork": False,
          "url": "https://api.github.com/repos/google/kubernetes",
          "created_at": "2021-01-26T20:38:37Z",
          "updated_at": "2021-01-26T20:38:39Z",
          "has_issues": True,
          "forks": 20,
          "default_branch": "main",
          },
      ]
    }
    mock_get_json.return_value = test_payload["repos"]
    with patch(
      "client.GithubOrgClient._public_repos_url",
      new_callable=PropertyMock,
      ) as mock_public_repos_url:
      mock_public_repos_url.return_value = test_payload["repos_url"]
      self.assertEqual(
        GithubOrgClient("google").public_repos()
        [
          "ssh-chat", "kubernetes"
        ]
      )
      mock_public_repos_url.assert_called_once()
    mock_get_json.assert_called_once()
  @parameterized.expand([
    ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
    ({'license': {'key': "apache-2.0"}}, "bsd-3-clause", False),
  ])
  
  def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
    """Test that the result of has_license is the expected one."""
    githubOrgClient = GithubOrgClient("google")
    client_has_license = githubOrgClient.has_license(repo, license_key)
    self.assertEqual(client_has_license, expected)

@parameterized_class([
  {
    'org_payload': TEST_PAYLOAD[0][0],
    'repos_payload': TEST_PAYLOAD[0][1],
    'expected_repos': TEST_PAYLOAD[0][2],
    'apache2_repos': TEST_PAYLOAD[0][3],
  },
])

class TestIntegrationGithubOrgClient(unittest.TestCase):
  """test perform integretion requests"""
  @classmethod
  def setUpClass(cls) -> None:
    """setup class"""
    route_payload = {
     "https://api.github.com/orgs/google": cls.org_payload,
      "https://api.github.com/orgs/google/repos": cls.repos_payload,
    }
   
    def get_payload(url):
      if url in route_payload:
        return Mock(**{"json.return_value": route_payload[url]})
      return HTTPError
    cls.get_patcher = patch('requests.get', side_effect=get_payload)
    cls.get_patcher.start()
    
  def test_public_repos(self) -> None:
    """Test public repos"""
    self.assertEqual(
      GithubOrgClient("google").public_repos(),
      self.expected_repos,
      )
    
  def test_public_repos_with_license(self) -> None:
    """Test public repos with license"""
    self.assertEqual(
      GithubOrgClient("google").public_repos("apache-2.0"),
      self.apache2_repos,
    )
  
  @classmethod
  def tearDownClass(cls) -> None:
    """teardown class"""
    cls.get_patcher.stop()