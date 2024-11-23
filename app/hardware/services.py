from uuid import uuid4
from app.hardware.entities import Hardware
from app.user.entities import User
from app.utils.stringutil import generate_secret_token


class HardwareService:

    @staticmethod
    async def register_display(user: User, device_id: str) -> str:
        new_device_token = generate_secret_token()
        new_entity = await Hardware.create(
            id=uuid4(),
            device_id=device_id,
            token=new_device_token,
            device_type="display",
            user_id=user.id,
        )
        user.display_hardware = new_entity
        await user.save()

        return new_device_token

    @staticmethod
    async def register_camera(user: User, device_id: str) -> str:
        new_device_token = generate_secret_token()
        new_entity = await Hardware.create(
            id=uuid4(),
            device_id=device_id,
            token=new_device_token,
            device_type="camera",
            user_id=user.id,
        )
        user.camera_hardware = new_entity
        await user.save()

        return new_device_token
