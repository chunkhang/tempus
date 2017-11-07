import sys; sys.path.append('../tempus')
from tempus import utils

def test_truncate():
   assert utils.truncate(1.67592, 0) == 1
   assert utils.truncate(1.67592, 1) == 1.6
   assert utils.truncate(1.67592, 2) == 1.67
   assert utils.truncate(1.67592, 3) == 1.675
   assert utils.truncate(1.67592, 4) == 1.6759
   assert utils.truncate(1.67592, 5) == 1.67592
   assert utils.truncate(1.67592, 6) == 1.67592