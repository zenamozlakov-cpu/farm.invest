import json
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .ai import AIError, ask_ai
from .market import STOCKS, get_market
from .models import GameState


def _session(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def _body(request):
    try:
        return json.loads(request.body or b"{}")
    except ValueError:
        return {}


@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")


@require_GET
def market(request):
    return JsonResponse({"stocks": get_market()})


def state(request):
    st, _ = GameState.objects.get_or_create(session_key=_session(request))
    if request.method == "POST":
        d = _body(request)
        try:
            cash = float(d.get("cash", st.cash))
            pos = d.get("positions", {})
            clean = {}
            for t, o in pos.items():
                if t in STOCKS and int(o["q"]) > 0:
                    clean[t] = {"q": int(o["q"]), "avg": float(o["avg"]), "x": float(o.get("x", 0)),
                                "y": float(o.get("y", 0)), "placed": int(bool(o.get("placed", 0)))}
            if cash < 0:
                raise ValueError
        except (ValueError, TypeError, KeyError, AttributeError):
            return JsonResponse({"error": "bad data"}, status=400)
        st.cash, st.positions = cash, clean
        st.save()
    return JsonResponse({"cash": st.cash, "positions": st.positions})


@require_POST
def ai(request):
    key = f"ai_rl_{_session(request)}"
    n = cache.get(key, 0)
    if n >= 20:  # не более 20 вопросов в минуту
        return JsonResponse({"error": "Слишком часто, подождите минуту."}, status=429)
    cache.set(key, n + 1, 60)
    d = _body(request)
    q = str(d.get("question", "")).strip()[:500]
    if not q:
        return JsonResponse({"error": "Пустой вопрос."}, status=400)
    ctx = json.dumps(d.get("context", {}), ensure_ascii=False)[:6000]
    try:
        return JsonResponse({"answer": ask_ai(q, ctx)})
    except AIError as e:
        return JsonResponse({"error": str(e)}, status=502)
