import asyncio
import time
import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from random import randint
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        result = await response.json()
        return result

async def send_pipeline_status_get_request():
    auth = aiohttp.BasicAuth(login='', password='')
    async with aiohttp.ClientSession(auth=auth) as session:
        data = await fetch(session, 'https://api.bitbucket.org/2.0/repositories/kyokushin_hakathon_2018/kyokushin-angular/pipelines/?pagelen=100')
    return data

def cozmo_program(robot = cozmo.robot.Robot):
    # robot.say_text("Lets wrap our summer two thousand eighteen hackanda").wait_for_completed()

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(send_pipeline_status_get_request())
    status = result['values'].pop()['state']['result']['name']
    cubes = [
        robot.world.get_light_cube(LightCube1Id),
        robot.world.get_light_cube(LightCube2Id),
        robot.world.get_light_cube(LightCube3Id)
    ]
    colors = [cozmo.lights.green_light, cozmo.lights.red_light, cozmo.lights.blue_light, cozmo.lights.green_light]
    timeout = time.time() + 3
    while True:
        test = 0
        if test == 5 or time.time() > timeout:
            break
        for cube in cubes:
            cube.set_light_corners(colors[randint(0,3)], colors[randint(0,3)], colors[randint(0,3)], colors[randint(0,3)])
            time.sleep(0.03)
        test -= 1

    if(status == 'SUCCESSFUL'):
        for cube in cubes:
            cube.set_lights(cozmo.lights.green_light)
    else:
        for cube in cubes:
            cube.set_lights(cozmo.lights.red_light)

    time.sleep(30)

cozmo.run_program(cozmo_program)
