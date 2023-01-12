from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# Enumeration


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/direction/{directionName}")
async def getDirection(directionName: DirectionName):
    if directionName == DirectionName.north:
        return {"direction": directionName, "subject": "up"}
    if directionName == DirectionName.south:
        return {"direction": directionName, "subject": "down"}
    if directionName == DirectionName.west:
        return {"direction": directionName, "subject": "left"}
    return {"direction": directionName, "subject": "right"}
