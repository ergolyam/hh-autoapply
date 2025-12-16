from worker.db.models import Vacancy


async def add_vac(vac_id: int, status: bool):
    await Vacancy.update_or_create(
        id=vac_id,
        defaults={
            'status': status
        }
    )


async def get_vac(vac_id: int) -> dict:
    vac = await Vacancy.get_or_none(id=vac_id)
    if not vac:
        return {'status': None}
    
    return {
        'status': vac.status
    }


async def get_vacs() -> dict:
    vacs = await Vacancy.all()
    result = {}
    for vac in vacs:
        result[vac.id] = {
            'status': vac.status
        }
    return result


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
