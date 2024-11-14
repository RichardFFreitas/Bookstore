# from django.http import HttpResponse
# from django.template import loader
# from django.views.decorators.csrf import csrf_exempt

# import git


# @csrf_exempt
# def update(request):
#     if request.method == "POST":
#         '''
#         pass the path of the diectory where your project will be
#         stored on PythonAnywhere in the git.Repo() as parameter.
#         Here the name of my directory is "test.pythonanywhere.com"
#         '''
#         repo = git.Repo('/home/RichardFFreitas/Bookstore')
#         origin = repo.remotes.origin

#         origin.pull()
#         return HttpResponse("Updated code on PythonAnywhere")
#     else:
#         return HttpResponse("Couldn't update the code on PythonAnywhere")


# def hello_world(request):
#   template = loader.get_template('hello_world.html')
#   return HttpResponse(template.render())

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import git
import os

@csrf_exempt
def update(request):
    if request.method == "POST":
        try:
            # Certifique-se de que o caminho corresponde ao local correto do repositório Git
            repo_path = os.getenv("REPO_PATH", "/home/RichardFFreitas/Bookstore")
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            
            # Atualizar o repositório com 'pull'
            origin.pull()
            return HttpResponse("Updated code on PythonAnywhere")
        except git.exc.GitError as e:
            # Tratar erros relacionados ao Git
            return HttpResponse(f"Git error occurred: {e}", status=500)
        except Exception as e:
            # Tratar outros erros
            return HttpResponse(f"An error occurred: {e}", status=500)
    else:
        return HttpResponse("Only POST requests are allowed", status=405)

def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())