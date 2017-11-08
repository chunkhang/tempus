import sys; sys.path.append('../tempus')
from tempus.commands import timer

def test_valid_syntax():
   assert timer._syntax_valid('1m2s') == True
   assert timer._syntax_valid('10m59s') == True
   assert timer._syntax_valid('1m2s') == True
   assert timer._syntax_valid('0m2s') == True
   assert timer._syntax_valid('1m0s') == True
   assert timer._syntax_valid('0m0s') == True
   assert timer._syntax_valid('1000m2s') == True
   for i in range(60):
      assert timer._syntax_valid('{}s'.format(i)) == True

def test_invalid_syntax():
   assert timer._syntax_valid('10') == False
   assert timer._syntax_valid('1M') == False
   assert timer._syntax_valid('2S') == False
   assert timer._syntax_valid('1m10s10') == False
   assert timer._syntax_valid('-1m-2s') == False
   assert timer._syntax_valid('-1m') == False
   assert timer._syntax_valid('-2s') == False

def test_to_duration():
   assert timer._to_duration('10m59s') == (10, 59)
   assert timer._to_duration('0m0s') == (0, 0)
   assert timer._to_duration('1m') == (1, None)
   assert timer._to_duration('1s') == (None, 1)
   assert timer._to_duration('') == (None, None)

def test_valid_duration():
   assert timer._values_valid((1, 1)) == True
   assert timer._values_valid((1, 0)) == True
   assert timer._values_valid((0, 1)) == True
   assert timer._values_valid((1000, 59)) == True
   for i in range(60):
      assert timer._values_valid((40, i)) == True

def test_invalid_duration():
   assert timer._values_valid((0, 0)) == False
   assert timer._values_valid((0, 60)) == False
   assert timer._values_valid((0, 61)) == False
   assert timer._values_valid((0, 61)) == False
   assert timer._values_valid((0, None)) == False
   assert timer._values_valid((None, 0)) == False
   assert timer._values_valid((None, None)) == False

def test_time_string():
   assert timer.Bar.Timer(0, None)._to_string(0) == '0:00'
   assert timer.Bar.Timer(20, None)._to_string(20) == '0:20'
   assert timer.Bar.Timer(720, None)._to_string(720) == '12:00'
   assert timer.Bar.Timer(721, None)._to_string(721) == '12:01'