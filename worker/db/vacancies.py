from worker.db.models import Vacancy

async def add_vac(vac_id: int, status: bool, cause: str = ''):
    if status:
        cause = ''
    await Vacancy.update_or_create(
        id=vac_id,
        defaults={
            'status': status,
            'cause': cause
        }
    )


async def get_vac(vac_id: int) -> dict:
    vac = await Vacancy.get_or_none(id=vac_id)
    if not vac:
        return {'status': None, 'cause': None}
    
    return {
        'status': vac.status, 
        'cause': vac.cause if vac.cause else None
    }


async def get_vacs() -> dict:
    vacs = await Vacancy.all()
    result = {}
    for vac in vacs:
        result[vac.id] = {
            'status': vac.status,
            'cause': vac.cause
        }
    return result


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
