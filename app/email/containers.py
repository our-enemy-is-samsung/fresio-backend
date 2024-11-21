from dependency_injector import containers, providers

from app.email.services import EmailService


class EmailContainer(containers.DeclarativeContainer):
    service: "EmailService" = providers.Resource(EmailService)
