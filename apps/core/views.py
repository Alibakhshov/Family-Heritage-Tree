import logging
from django.shortcuts import render, redirect
from .models import PersonalInfo, GalleryImage, Timeline
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from apps.famTree.models import FamilyNode
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TimelineForm
from django.http import JsonResponse
from django.contrib import messages


logger = logging.getLogger(__name__)

############################################### HOME PAGE VIEWS ###############################################

@login_required(login_url='/')
def home(request):
    try:
        if request.user.is_authenticated:
            try:
                personal_info = PersonalInfo.objects.get(user=request.user)
            except PersonalInfo.DoesNotExist:
                logger.exception("PersonalInfo does not exist for the current user.")
                personal_info = None

            try:
                user_family_nodes = FamilyNode.objects.filter(user=request.user).exclude(id__isnull=True).order_by('date_of_birth')
            except FamilyNode.DoesNotExist:
                logger.exception("FamilyNode does not exist for the current user.")
                user_family_nodes = None


            total_members = user_family_nodes.count()
            total_male = user_family_nodes.filter(gender='male').count()
            total_female = user_family_nodes.filter(gender='female').count()

            for node in user_family_nodes:
                try:
                    if node.date_of_birth:
                        date_of_birth_obj = node.date_of_birth
                        today = timezone.now().date()
                        birthday = date_of_birth_obj.replace(year=today.year)
                        if birthday < today:
                            birthday = birthday.replace(year=today.year + 1)
                        node.days_until_birthday = (birthday - today).days
                        node.save()
                except Exception as e:
                    logger.exception("An error occurred in home view birthday calculation: %s", str(e))

            for node in user_family_nodes:
                try:
                    if node.mid == node.id:
                        node.relationship = "Mother"
                    elif node.fid == node.id:
                        node.relationship = "Father"
                    elif node.pids and node.id in node.pids:
                        node.relationship = "Parent"
                    else:
                        node.relationship = "Other"
                    node.save()
                except Exception as e:
                    logger.exception("An error occurred in home view relationship calculation: %s", str(e))

            paginator = Paginator(user_family_nodes, 4)
            page_number = request.GET.get('page')
            try:
                user_family_nodes_page = paginator.page(page_number)
            except PageNotAnInteger:
                user_family_nodes_page = paginator.page(1)
            except EmptyPage:
                user_family_nodes_page = paginator.page(paginator.num_pages)

            context = {
                'user': request.user,
                'personal_info': personal_info,
                'user_family_nodes': user_family_nodes_page,
                'total_members': total_members,
                'total_male': total_male,
                'total_female': total_female,
            }

            return render(request, 'core/index.html', context)
        else:
            return render(request, 'core/index.html')
    except Exception as e:
        logger.exception("An error occurred in home view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')
    
############################################### ABOUT PAGE VIEWS ###############################################

@login_required(login_url='/')
def about(request):
    try:
        personal_info = PersonalInfo.objects.get(user=request.user)
    except PersonalInfo.DoesNotExist:
        logger.exception("PersonalInfo does not exist for the current user.")
        personal_info = None
    
    try:
        if request.method == 'POST':
            if 'background_image' in request.FILES:
                background_image = request.FILES['background_image']
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'background_images'))
                filename = fs.save(background_image.name, background_image)
                personal_info.background_image = os.path.join('background_images', filename)  
                personal_info.save() 
        context = {
            'personal_info': personal_info 
        }
        return render(request, 'core/user-profile/about.html', context)
    except Exception as e:
        logger.exception("An error occurred in about view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')
    
############################################### ACCOUNT SETTINGS VIEWS ###############################################

@login_required(login_url='/')
def edit_profile(request):
    try:
        user = request.user
        personal_info, created = PersonalInfo.objects.get_or_create(user=user)
        
        if request.method == 'POST':
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.first_name = request.POST['name']
            
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                user.avatar = avatar
            
            personal_info.position = request.POST['position']
            
            user.save()
            personal_info.save()
            return redirect('edit_profile')  
        return render(request, 'core/user-profile/account-setting.html', {'personal_info': personal_info})
    except Exception as e:
        logger.exception("An error occurred in edit_profile view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')

@login_required(login_url='/')
def edit_profileInfo(request):
    try:
        user = request.user
        personal_info, created = PersonalInfo.objects.get_or_create(user=user)
        
        if request.method == 'POST':
            personal_info.bio = request.POST['bio']
            personal_info.age = request.POST['age']
            personal_info.address = request.POST['address']
            personal_info.birth_date = request.POST['birth_date']
            personal_info.phone_number = request.POST['phone_number']
            
            personal_info.save()
            return redirect('edit_profileInfo')
        
        return render(request, 'core/user-profile/account-setting.html', {'personal_info': personal_info})
    except Exception as e:
        logger.exception("An error occurred in edit_profileInfo view: %s", str(e))
        return render(request, 'core/user-profile/account-setting.html', {'personal_info': None})

@login_required(login_url='/')
def edit_profileSocial(request):
    try:
        user = request.user
        personal_info, created = PersonalInfo.objects.get_or_create(user=user)
        
        if request.method == 'POST':
            personal_info.instagram = request.POST.get('instagram', '')
            personal_info.facebook = request.POST.get('facebook', '')
            personal_info.twitter = request.POST.get('twitter', '')
            personal_info.linkedin = request.POST.get('linkedin', '')
            personal_info.save()
            return redirect('edit_profileSocial')
        
        return render(request, 'core/user-profile/account-setting.html', {'personal_info': personal_info})
    except Exception as e:
        logger.exception("An error occurred in edit_profileSocial view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')

############################################### GALLERY VIEWS ###############################################

@login_required(login_url='/')
def gallery(request):
    try:
        if request.method == 'POST':
            if 'gallery_image' in request.FILES:
                gallery_image = request.FILES['gallery_image']
                user = request.user
                GalleryImage.objects.create(user=user, image=gallery_image)

        gallery_images = GalleryImage.objects.filter(user=request.user)
        context = {
            'gallery_images': gallery_images
        }
        return render(request, 'core/user-profile/gallery.html', context)
    except Exception as e:
        logger.exception("An error occurred in gallery view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')

@login_required(login_url='/')
def delete_image(request, image_id):
    try:
        image = GalleryImage.objects.get(pk=image_id)
        image.delete()
        return redirect('gallery')
    except Exception as e:
        logger.exception("An error occurred in delete_image view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')
    
############################################### TIMELINE VIEWS ###############################################

@login_required(login_url='/')
def timeline(request):
    try:
        # Retrieve timeline objects for the current user
        timelines = Timeline.objects.filter(user=request.user)
        # Fetching the description
        description = timelines.first().description if timelines else ""
        context = {
            'timelines': timelines,
            'description': description  # Pass the description to the template
        }
        return render(request, 'core/user-profile/timeline.html', context)
    except Exception as e:
        logger.exception("An error occurred in timeline view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')

def add_timeline(request):
    if request.method == 'POST':
        event_title = request.POST.get('event_title')
        event_description = request.POST.get('event_description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        if event_title and event_description and date and time:
            try:
                timeline = Timeline.objects.create(
                    user=request.user,
                    event_title=event_title,
                    event_description=event_description,
                    date=date,
                    time=time
                )
                messages.success(request, 'Timeline record added successfully!')
                return redirect('timeline')
            except Exception as e:
                messages.error(request, f'Failed to add timeline record: {str(e)}')
        else:
            messages.error(request, 'All fields are required!')
    
    return redirect('timeline')

def delete_timeline(request, timeline_id):
    if request.method == 'POST':
        try:
            timeline = Timeline.objects.get(id=timeline_id)
            timeline.delete()
            messages.success(request, 'Timeline record deleted successfully!')
        except Timeline.DoesNotExist:
            messages.error(request, 'Timeline record does not exist!')
    return redirect('timeline')

def edit_timeline(request, timeline_id):
    if request.method == 'POST':
        try:
            timeline = Timeline.objects.get(id=timeline_id)
            form = TimelineForm(request.POST, instance=timeline)
            if form.is_valid():
                form.save()
                messages.success(request, 'Timeline record updated successfully!')
            else:
                messages.error(request, 'Failed to update timeline record!')
        except Timeline.DoesNotExist:
            messages.error(request, 'Timeline record does not exist!')
    return redirect('timeline')

def get_timeline(request, timeline_id):
    try:
        timeline = Timeline.objects.get(id=timeline_id)
        # Assuming Timeline model has event_title, event_description, date, and time fields
        data = {
            'event_title': timeline.event_title,
            'event_description': timeline.event_description,
            'date': timeline.date,
            'time': timeline.time,
        }
        return JsonResponse(data)
    except Timeline.DoesNotExist:
        # Return 404 if the timeline with the provided ID does not exist
        return render(request, 'core/miscellaneous/404.html')
    

############################################## ROOTS VIEWS ###############################################

from apps.famTree.models import FamilyNode
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required(login_url='/')
def roots_list(request):
    try:
        people = FamilyNode.objects.filter(user=request.user)
        return render(request, 'core/roots/roots-list.html', {'people': people})
    except Exception as e:
        logger.exception("An error occurred in roots_list view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')
    
@login_required(login_url='/')
def roots_grid(request):
    try:
        # Fetch FamilyNode objects from the database
        family_nodes = FamilyNode.objects.filter(user=request.user)
        return render(request, 'core/roots/roots-grid.html', {'family_nodes': family_nodes})
    except Exception as e:
        logger.exception("An error occurred in roots_grid view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')


@csrf_exempt
def save_root(request, id):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)

            # Retrieve FamilyNode object corresponding to the provided ID
            root = FamilyNode.objects.get(id=id)

            # Update fields of the FamilyNode object
            root.name = data.get("name", root.name)
            root.email = data.get("email", root.email)
            root.phone = data.get("phone", root.phone)
            # root.age = data.get("age", root.age)
            root.relationship = data.get("relationship", root.relationship)

            # Save the updated object
            root.save()

            # Return success response
            return JsonResponse({"status": "success", "message": "Root updated successfully"})
        
        except FamilyNode.DoesNotExist:
            # Handle case when FamilyNode object with the provided ID does not exist
            return JsonResponse({"status": "error", "message": "Root not found"}, status=404)
        
        except Exception as e:
            # Handle other exceptions
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    # Handle invalid request method
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)



############################################### QUIZ VIEWS ###############################################
    
from django.shortcuts import render
from .models import Question, QuizResult
from django.contrib.auth.decorators import login_required


@login_required
def quiz(request):
    try:
        questions = Question.objects.filter(user=request.user)
        if request.method == 'POST':
            score = 0
            wrong = 0
            total = 0
            for q in questions:
                total += 1
                correct_answer = request.POST.get(str(q.id))
                if correct_answer == q.correct_answer:
                    score += 1
                else:
                    wrong += 1

            # Save the result
            QuizResult.objects.create(
                user=request.user,
                score=score,
                total_questions=total,
                correct_answers=score,
                wrong_answers=wrong
            )

            return render(request, 'core/quiz/result.html', {
                'score': score,
                'total': total,
                'correct': score,
                'wrong': wrong,
                'questions': questions,
            })

        return render(request, 'core/quiz/quiz.html', {'questions': questions})
    except Exception as e:
        logger.exception("An error occurred in quiz view: %s", str(e))
        return render(request, 'core/miscellaneous/404.html')