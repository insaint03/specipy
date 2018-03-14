import unittest
from specipy import accepts

class test_accepts(unittest.TestCase) :
    # values
    VALUES_TO_TEST = (
        True, False, 10, 11, 0.1, 
        'hello world', 'insaint03@gmail.com', 'lookslikeanemail.butwow@.com', 'v1.0.0', 'v1',
        (1,2,3),['a','b','c'],set((1,2,3)),{'a':1,'b':2}
    )
    # accept, expecteds
    TYPES_TO_TEST = (
        ('primitive', 
            (str(True), str(False), str(10), str(11), str(0.1), 
            None, None, None, None, None, 
            TypeError, TypeError,TypeError,TypeError)),
        ('integer', 
            (int(True), int(False), None, None, int(0.1), 
            TypeError, TypeError, TypeError, TypeError, TypeError, 
            TypeError, TypeError, TypeError, TypeError)),
        ('string',
            (str(True), str(False), str(10), str(11), str(0.1), 
            None, None, None, None, None, 
            TypeError, TypeError,TypeError,TypeError)),
        ('email',
            (ValueError, ValueError, ValueError, ValueError, ValueError, 
            ValueError, None, ValueError, ValueError, ValueError, 
            TypeError, TypeError,TypeError,TypeError))
    )

    def test_encodes(self) :
        for aname,expects in self.TYPES_TO_TEST :
            acc = getattr(accepts, aname)
            self.assertIsNotNone(acc)
            for i in range(0, len(self.VALUES_TO_TEST)) :
                v = self.VALUES_TO_TEST[i]
                e = expects[i]
                print('%s, %s expected: %s'%(aname, str(v), str(e)))
                if e in (TypeError, ValueError) :
                    with self.assertRaises(e) :
                        acc.encode(v)
                else :
                    if e is None : e = v
                    self.assertEqual(acc.encode(v), e)
                    
    
