import tortoise.models
from tortoise import fields


class Vacancy(tortoise.models.Model):
    id = fields.IntField(pk=True) 
    status = fields.BooleanField(default=True)
    cause = fields.TextField(null=True)

    class Meta(tortoise.models.Model.Meta):
        table = 'vacancies'


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
