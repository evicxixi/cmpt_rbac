from stark.service.stark import site
from web import models

print("name = 'stark'")
obj = site.register(models.Customer)

ret = obj
print('site.register', type(ret), ret)
