from typing import Optional, Any
from sqlalchemy.orm import Session

from genai_stack.genai_server.schemas.components import ETLJob
from genai_stack.genai_platform.services.base_service import BaseService
from genai_stack.genai_server.models.etl_models import ETLJobResponseType
from genai_stack.genai_server.utils import get_current_stack, get_stack_session
from genai_stack.genai_server.utils.components import ETLUtil, get_etl_platform
from genai_stack.genai_server.settings.config import stack_config


class ETLService(BaseService):
    def submit_job(self, data: Any, stack_session_id: Optional[int] = None) -> ETLJobResponseType:
        with Session(self.engine, expire_on_commit=False) as session:
            stack_session = get_stack_session(session, stack_session_id=stack_session_id)

            etl_job = ETLJob(stack_session=stack_session.id)
            session.add(etl_job)
            session.commit()

            data = ETLUtil(data).save_request(etl_job.id)

            stack = get_current_stack(config=stack_config, engine=session, session=stack_session)
            get_etl_platform(stack=stack).handle_job(**data)

            etl_job.data = data
            session.commit()

            response = ETLJobResponseType(
                id=etl_job.id,
                session_id=etl_job.stack_session,
                status=etl_job.status.value,
                metadata=etl_job.meta_data,
            )
            return response
