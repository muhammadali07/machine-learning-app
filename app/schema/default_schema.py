from pydantic import BaseModel

# ------------------- Models ------------------- #
class User(BaseModel):
    username: str
    password: str
    email: str
    age: int
    gender: str
    height: float
    weight: float

class Login(BaseModel):
    username: str
    password: str

class InputModel(BaseModel):
    gender: str
    age: float
    height: float
    weight: float
    family_history: int
    high_calorie_food: int
    vegetable_freq: int
    meals_per_day: float
    food_between_meals: str
    smoking: int
    water_consumption: float
    calorie_monitoring: int
    physical_activity: float
    tech_usage: int
    alcohol_consumption: str
    transportation: str


class NutritionAnalyzeRequest(BaseModel):
    food_name: str
    serving_size: float
