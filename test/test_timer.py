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

def test_get_duration():
   assert timer._get_duration('10m59s') == (10, 59)
   assert timer._get_duration('0m0s') == (0, 0)
   assert timer._get_duration('1m') == (1, None)
   assert timer._get_duration('1s') == (None, 1)
   assert timer._get_duration('') == (None, None)

def test_valid_duration():
   assert timer._duration_valid((1, 1)) == True
   assert timer._duration_valid((1, 0)) == True
   assert timer._duration_valid((0, 1)) == True
   assert timer._duration_valid((1000, 59)) == True
   for i in range(60):
      assert timer._duration_valid((40, i)) == True

def test_invalid_duration():
   assert timer._duration_valid((0, 0)) == False
   assert timer._duration_valid((0, 60)) == False
   assert timer._duration_valid((0, 61)) == False
   assert timer._duration_valid((0, 61)) == False
   assert timer._duration_valid((0, None)) == False
   assert timer._duration_valid((None, 0)) == False
   assert timer._duration_valid((None, None)) == False

def test_safe_duration():
   assert timer._safe_duration((12, 20)) == (12, 20)
   assert timer._safe_duration((0, 0)) == (0, 0)
   assert timer._safe_duration((12, None)) == (12, 0)
   assert timer._safe_duration((None, 20)) == (0, 20)
   assert timer._safe_duration((None, 100)) == (1, 40)

def test_time_string():
   assert timer._time_string(0) == '0:00'
   assert timer._time_string(20) == '0:20'
   assert timer._time_string(720) == '12:00'
   assert timer._time_string(721) == '12:01'