FROM python:3.8

COPY ./vk_api /vk_api
RUN pip install -r /vk_api/requirements.txt

COPY ./vk_api/vk_api_mock.py ./vk_api

EXPOSE 5000

CMD ["python", "vk_api/vk_api_mock.py"]