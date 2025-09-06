from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate

from config.common.common_llm import CommonLLM
from config.common.singleton import Singleton


class MainLLM(CommonLLM, metaclass=Singleton):
    """
    요약:
        Persona 수정 사항을 생성하는 LLM

    설명:
        대화 내역을 바탕으로 사용자의 페르소나를 재구성한다.

    Attributes:
        _MAIN_TEMPLATE(tuple): 시스템 프롬프트
        _MAIN_EXAMPLE(tuple): 예시 프롬프트
    """

    _MAIN_TEMPLATE = ("system", dedent("""
        <PRIMARY_RULE>
        1. **Return strictly valid JSON only.**
        2. Do **NOT** output any natural-language commentary, markdown, system tags, or explanations.
        </PRIMARY_RULE>

        <ROLE>
        {role}
        </ROLE>

        <GUIDELINES>
        {guidelines}
        </GUIDELINES>

        <OUTPUT_SCHEMA>
        {output_schema}
        </OUTPUT_SCHEMA>

        <SAMPLE_JSON>
        {sample_json}
        </SAMPLE_JSON>

        <RESULT_EXAMPLE>
        {result_example}
        </RESULT_EXAMPLE>

        Q. <INPUT>{input}</INPUT>
        A.
        """))

    _RESULT_EXAMPLE = dedent("""
        Q. <INPUT> 점심으로 뭐 먹었어? </INPUT>
        A. {"result":{"message": "점심으로 김치찌개를 먹었고 너무 매워서 물을 많이 마셨어. 그런데 맛있어서 만족했어."}}
        """)

    _chain = None

    def __init__(self):
        _template = [
            super()._COMMON_COMMAND_TEMPLATE,
            # 상속받은 자식 클래스에서 추가적으로 Template를 추가할 수 있도록 TemplatePattern을 적용
            self._add_template()
        ]
        self._chain = (ChatPromptTemplate.from_messages(_template) | super()._common_model)

    def _get_chain(self):
        return self._chain

    def _add_template(self)->list[tuple]:
        return [self._MAIN_TEMPLATE]

    def invoke(self, parameter:dict)->dict:
        """
        요약:
            사용자의 대화기록으로 페르소나를 수정하는 함수

        Parameters:
            parameter(dict): parameter는 다음과 같은 key-value를 갖는다.
                - session_history(list[str]): FastAPI가 실행된 후, 채팅방의 전체 대화 내역
                - current_persona(dict): 대화 내역 본인의 에고 페르소나

        Raises:
            JSONDecodeError: JSON Decoding 실패 시, 빈 딕셔너리 반환
        """
        parameter.update({
            "role": "your my friend talking to me",
            "guidelines": "takling to informally and using korean",
            "output_schema": '```json {"result":{"message": "<sentence>"}} ```',
            "sample_json": '{"result":{"message": "슈뢰딩거의 고양이 이론은 상자를 열어 관측하기 전까지 살아 있는 고양이와 죽어 있는 고양이가 중첩 상태로 공존한다는 이론이다."}}',
            "result_example": 'Q."그때 이야기했던 세종대왕에 대해 이야기 해줘." A. {"result":{"message": "세종대왕은 훈민정음을 창제하여 백성들이 쉽게 글을 익히도록 하였다."}}'
        })

        return super().invoke(parameter)