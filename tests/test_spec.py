import unittest
from specipy import spec, expect, accepts

class sample_model(spec) :
    def __init__(self) :
        super().__init__()
        self._given_name = None
        self._family_name = None
        self._email = None
        self._phone = None
        self._year_of_birth = None


    @expect(accepts.string, True)
    def given_name(self, v=None) :
        if v is not None : self._given_name = v
        return self._given_name

    @expect(accepts.string, True)
    def family_name(self, v=None) :
        if v is not None : self._family_name = v
        return self._family_name
    
    @expect(accepts.email)
    def email(self, v=None) :
        if v is not None : self._email = v
        return self._email

    @expect(accepts.string)
    def phone(self, v=None) :
        if v is not None : self._phone = v
        return self._phone
    
    @expect(accepts.integer)
    def year_of_birth(self, v=None) :
        if v is not None : self._year_of_birth = v
        return self._year_of_birth

sample_model_data = (
    # ALL GOOD SO FAR
    ({'given_name': 'John', 'family_name': 'Smith', 'email': 'john.smith@email.com', 'phone': 'unknown', 'year_of_birth': 1984}, None),
    # no phone no email
    ({'given_name': 'John', 'family_name': 'Smith', 'year_of_birth': 1984}, None),
    # name exception: validation fail
    ({'family_name': 'Smith', 'email': 'john.smith@email.com', 'phone': 'unknown', 'year_of_birth': 1984}, AttributeError),
    # year of birth mismatch: insertion fail
    ({'given_name': 'John', 'family_name': 'Smith', 'email': 'john.smith', 'phone': 'unknown', 'year_of_birth': '1Q84'}, TypeError),
    # email mismatch: insertion fail
    ({'given_name': 'John', 'family_name': 'Smith', 'email': 'john.smith', 'phone': 'unknown', 'year_of_birth': 1984}, ValueError)
)

class test_model(unittest.TestCase) :
    def test_model_creation(self) :
        model = sample_model()
        (data, err) = sample_model_data[0]
        model.populate(data)

        self.assertEqual(data['given_name'], model.given_name)
        self.assertEqual(data['family_name'], model.family_name)
        self.assertEqual(data['email'], model.email)
        self.assertEqual(data['phone'], model.phone)
        self.assertEqual(data['year_of_birth'], model.year_of_birth)

        self.assertTrue(model.validate())

    def test_model_validation(self) :
        model = sample_model()        

        for data,err in sample_model_data :
            if err is None :
                model.populate(data)
                self.assertTrue(model.validate())

    def test_model_exception(self) :
        model = sample_model()
        for data,err in sample_model_data :
            if err is None : continue
            with self.assertRaises(err) :
                model.populate(data)
                self.assertFalse(model.validation())

        

    def test_model_error(self) :
        model = sample_model()
        with self.assertRaises(TypeError) :
            model.year_of_birth = (1,'Q',8,4)

        