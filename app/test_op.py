import operations
def test_add():
    assert operations.add(40,50) == 90, "Add function needs fixing"
    assert operations.add(4.5,6.7) == 11.2, "Add function needs fixing"

def test_sub():
    assert operations.sub(40,50) == -10, "Subtract function needs fixing"
    assert operations.sub(9.8,3.3) == 6.5, "Subtract function needs fixing"

def test_mul():
    assert operations.mul(40,50) == 2000, "Multiplication function needs fixing"
    assert operations.mul(-0.9,5.1) == -4.59, "Multiplication function needs fixing"

def test_div():
    assert operations.div(40,50) == 0.8, "Division function needs fixing"
    assert operations.div(-8.5,-12.8) == 0.6640625, "Division function needs fixing"
