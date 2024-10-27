import logging

from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader

from .models import Message, Response
from .utils.langchainGptApi import getResponseFromApi

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
        log.info(f'sent message: {request.POST['message']}')

        if not request.POST["message"]:
            log.error("EMPTY MESSAGE!")
            # since page 404 doesn't exist this is just to return
            # a 404 response
            raise Http404("EMPTY MESSAGE!")

        # AJAX will parse this JSON in the frontend
        return JsonResponse(
            {
                "sucess": True,
                "message_text": request.POST["message"],
            }
        )
    else:
        return JsonResponse({"sucess": False})


def receiveResponse(request):
    if request.method == "POST":
        responseText = ""
        try:
            message = Message(
                message_text=request.POST["message"],
            )
            message.save()

            # reminder that this DOES NOT keep the context of the main conversation,
            # working on that later, as well Markdown linting support
            data = getResponseFromApi(request.POST["message"])
            responseText = data["response_text"]

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

        return JsonResponse(
            {
                "sucess": True,
                "message_text": responseText,
            }
        )
    else:
        return JsonResponse({"sucess": False})
