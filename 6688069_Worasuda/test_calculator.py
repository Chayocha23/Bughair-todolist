"""
Tests for the calculator module.
"""

import pytest
from calculator import Calculator


def test_add():
    """Test addition operation."""
    assert Calculator.add(5, 3) == 8
    assert Calculator.add(-5, 3) == -2
    assert Calculator.add(0, 0) == 0
    assert Calculator.add(1.5, 2.5) == 4.0


def test_subtract():
    """Test subtraction operation."""
    assert Calculator.subtract(5, 3) == 2
    assert Calculator.subtract(3, 5) == -2
    assert Calculator.subtract(0, 0) == 0
    assert Calculator.subtract(10.5, 3.5) == 7.0


def test_multiply():
    """Test multiplication operation."""
    assert Calculator.multiply(5, 3) == 15
    assert Calculator.multiply(-5, 3) == -15
    assert Calculator.multiply(0, 100) == 0
    assert Calculator.multiply(2.5, 4) == 10.0


def test_divide():
    """Test division operation."""
    assert Calculator.divide(6, 2) == 3
    assert Calculator.divide(10, 4) == 2.5
    assert Calculator.divide(-8, 2) == -4


def test_divide_by_zero():
    """Test that dividing by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Calculator.divide(5, 0)
