#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import (
  Mapping,
  Sequence,
  Dict,
  Tuple,
  Union
)

class testAccessNestedMap:
  """Test class for utils.access_nested_map""" 
  @parameterized.expand([
    ({'a': 1}, ('a',), 1),
    ({'a': {'b': 2}}, ('a',), {'b': 2}),
    ({'a': {'b': 2}}, ('a', 'b'), 2),
  ])
  
  def test_access_nested_map(
    self,
    nested_map: Mapping,
    path: Sequence,
    expected: Union[Dict, int]
  ) -> None:
    """Test access_nested_map"""
    self.assertEqual(access_nested_map(nested_map, path), expected)
    
    @parameterized.expand([
      ({}, ('a',), KeyError),
      ({'a': 1}, ('a', 'b'), KeyError),
    ])
    
    def test_access_nested_map_exception(
      self,
      nested_map: Mapping,
      path: Sequence,
      expection: Exception
    ) -> None:
      """Test access_nested_map exceptions"""
      with self.assertRaises(expection):
        access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
  """Test class for utils.get_json"""
  @parameterized.expand([
    ("http://example.com", {"payload": True}),
    ("http://holberton.io", {"payload": False})
  ])
  def test_get_json(
    self,
    test_url: str,
    test_payload: Dict
  ) -> None:
    """Test that utils.get_json returns the expected result."""
    mock = Mock()
    mock.json.return_value = test_payload
    with patch('requests.get', return_value=mock):
      self.assertEqual(get_json(test_url), test_payload)
      mock.json.assert_called_once()

class TestMemoize(unittest.TestCase):
  """"Test class for utils.memoize"""
  def test_memoize(self) -> None:
    """tests memoize"""
    class TestClass:
      """TestClass"""
      def a_method(self):
        """a_method"""
        return 42

      @memoize
      def a_property(self):
        """a_property"""
        return self.a_method()
    with patch.object(TestClass, 'a_method', return_value=42) as mock:
      test_class = TestClass()
      self.assertEqual(test_class.a_property(), 42)
      self.assertEqual(test_class.a_property(), 42)
      mock.assert_called_once()
          