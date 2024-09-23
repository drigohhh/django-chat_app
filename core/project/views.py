import logging

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

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
    log.info(f'mensagem enviada: {request.POST['message']}')

    if not request.POST["message"]:
        log.error("MENSAGEM VAZIA!")
        return Http404("MENSAGEM VAZIA!")

    try:
        message = Message(
            message_text=request.POST["message"],
        )
        message.save()
    except Exception as e:
        log.error(f"ERROR: {e}")

    return HttpResponseRedirect(reverse("index"))
