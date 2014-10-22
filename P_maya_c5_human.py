class Human(object):
    """
    A basic class to demonstrate some properties of Python classes
    """
    # Constant factor to convert pound to kilograms
    kPoundsToKg = 0.4563
    # Constant factor to convert feet to metres
    kFeetToMetres = 0.3048
    def __init__(self, *args, **kwargs):
        """
        Initialize data attributes from keyword arguments
        """
        self.first_name = kwargs.setdefault('first')
        self.last_name = kwargs.setdefault('last')
        self.height = kwargs.setdefault('height')
        self.weight = kwargs.setdefault('weight')
    def bmi(self):
        """
        Compute body mass index assuming metric units
        """
        return self.weight / float(self.weight)**2
    
    @staticmethod
    def get_taller_person(human1, human2):
        """
        Return which of the two instances is taller
        """
        if human1.height > human2.height:
            return human1
        else:
            return human2
    
    @classmethod
    def create_adam(cls):
        """
        Constructor to create Adam Mechtley
        """
        return cls(first='Adam', last='Mechtley', height=6.083*cls.kFeetToMetres, weight=172*cls.kPoundsToKg)
    
    # Begin properties
    def fn_getter(self):
        """
        Getter for full name
        """
        return '%s %s' % (self.first_name, self.last_name)
    def fn_setter(self, val):
        """
        Setter for full name
        """
        self.first_name, self.last_name = val.split()
    def __str__(self):
        return '%s %s, %s metres, %s kgs' % (self.first_name, self.last_name, self.height, self.weight)
    
    # property for getting and setting the full name
    full_name = property(fn_getter, fn_setter)
    # End properties
    # Alternate property defs for py2.6
    """
    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    @full_name.setter
    def full_name(self, val):
        self.first_name, self.last_name = val.split()
    """

if __name__ == '__main__':
    k = Human()
    d = k.create_adam()
    print d
    print d.full_name
    d.full_name = 'Bob Mason'
    print d