from typing import Optional
from pydantic._internal import _model_construction

class AllOptional(_model_construction.ModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):
        annotations = namespace.get('__annotations__', {})
        
        for base in bases:
            if hasattr(base, '__annotations__'):
                annotations.update(base.__annotations__)
        
        for field_name, field_type in annotations.items():
            if not field_name.startswith('__'):
                if getattr(field_type, '__origin__', None) is Optional:
                    continue
                annotations[field_name] = Optional[field_type]
        
        namespace['__annotations__'] = annotations
        
        return super().__new__(mcs, name, bases, namespace, **kwargs)