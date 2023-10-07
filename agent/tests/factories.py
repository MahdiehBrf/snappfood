from factory.django import DjangoModelFactory

from agent.models import Agent


class AgentFactory(DjangoModelFactory):
    class Meta:
        model = Agent
