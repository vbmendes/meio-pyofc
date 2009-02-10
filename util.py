class OfcDict(dict):
    types = {}
    _cached_types = None
    
    def __init__(self, dictionary={}):
        for key in dictionary:
            self[key] = dictionary[key]
    
    def _get_types(self, cls=None):
        if(self._cached_types):
            return self._cached_types
        all_types = {}
        if not cls and isinstance(self, OfcDict):
            cls = self.__class__
        if issubclass(cls, OfcDict) or cls == OfcDict:
            all_types.update(cls._get_types(self,cls.__mro__[1]))
            all_types.update(cls.types)
        if self.__class__ == cls:
            self._cached_types = all_types
        return all_types
    all_types = property(_get_types)
            
    
    def _get_type(self, name):
        if self.all_types and not name in self.all_types:
            raise AttributeError, "%s is not an allowed attribute of %s" % (name, self.__class__.__name__)
        if self.all_types:
            return self.all_types[name]
            # TODO! Raise a new type of exception, more descriptive
        else:
            return dict

    def __getitem__(self, key):
        _type = self._get_type(key)
        if not key in self:
            self[key] = _type()            
        return super(OfcDict, self).__getitem__(key)
    
    def __setitem__(self, key, value):
        _type = self._get_type(key)
        value = getattr(self, '_process_'+key.replace('-','_'), lambda x: x)(value)
        if value is not None:
            if not isinstance(value, _type):
                value = _type(value)
            return super(OfcDict, self).__setitem__(key, value)
    
    def __delitem__(self, key):
        self._get_type(key)
        return super(OfcDict, self).__delitem__(key)
    
    def clean_nulls(self):
        for key in self.keys():
            item = self[key]
            if isinstance(item, OfcDict):
                item.clean_nulls()
            if not item:
                del self[key]
    
    def set_attr(self, attr, value):
        if value is not None:
            self[attr] = value
