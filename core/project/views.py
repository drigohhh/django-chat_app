import logging

from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader

from .models import Message, Response
from .utils import langchainGptApi as api

log = logging.getLogger(__name__)


def index(request):
    latest_messages_list = Message.objects.order_by("pub_date")

    template = loader.get_template("index.html")
    context = {
        "latest_messages_list": latest_messages_list,
    }
    return HttpResponse(template.render(context, request))


def sendMessage(request):
    if request.method == "POST":
        log.info(f'mensagem enviada: {request.POST['message']}')

        if not request.POST["message"]:
            log.error("EMPTY MESSAGE!")
            # since page 404 doesn't exist this is just to return
            # a 404 response
            raise Http404("EMPTY MESSAGE!")

        try:
            data = api.getResponseFromApi(request.POST["message"])

            message = Message(
                message_text=request.POST["message"],
            )
            message.save()

            # This will be changed to another view function
            # for a smoother user experience, since I would
            # put too much responsability on the AJAX already
            # made for the user sent message

            # reload the page to see the actual api response
            response = Response(
                question=message,
                response_text=data["response_text"],
                completion_tokens=data["completion_tokens"],
                prompt_tokens=data["prompt_tokens"],
                total_price=data["total_price"],
            )
            response.save()
        except Exception as e:
            log.error(f"ERROR: {e}")

        # AJAX will parse this JSON in the frontend
        return JsonResponse(
            {
                "sucess": True,
                "message_text": message.message_text,
            }
        )
    else:
        return JsonResponse({"sucess": False})
