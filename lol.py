from pydantic_settings import BaseSettings

class Human(BaseSettings):
    name: str
    agility: int

iam=Human(name="I am", agility=100)

if __name__ == '__main__':
    print(iam)