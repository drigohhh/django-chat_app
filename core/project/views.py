import logging

from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader

from .models import Message

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
            message = Message(
                message_text=request.POST["message"],
            )
            message.save()
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
