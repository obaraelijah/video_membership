from app import config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse ,RedirectResponse

settings = config.get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))

def redirect(path, cookies:dict={}):
    response = RedirectResponse(path, status_code=302)
    for k, v in cookies.items():
        response.set_cookie(key = k, value=v, httponly=True)
    return response
    

def render(request, template_name, context={}, status_code: int=200 , cookies:dict={}):
    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str,status_code=status_code)
    #print(request.cookiies)
    response.set_cookie(key='darkmode', value=1)
    if len(cookies.keys()) > 0:
        # set httponly cookies
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
            
    # delete cookies
    #for key in request.coookies.keys():
    #    response.delete_cookie(keys)
    return response
