from django.shortcuts import render
from apps.authentication.models import CustomUser
from django.http import JsonResponse
from .models import FamilyLink, FamilyNode
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
def tree(request):
    # Get all users
    users = CustomUser.objects.all()
    nodes = FamilyNode.objects.all()
    context = {
        'users': users,
        'nodes': nodes
    }
    return render(request, 'famTree/famTree.html', context)



@csrf_exempt
@login_required(login_url='/')
def tree_save(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body.decode('utf-8'))
            if received_data:
                nodes_data = received_data.get('nodes', [])
                links_data = received_data.get('clinks', [])

                # Delete node and links data when nodes are deleted from the frontend
                existing_nodes = FamilyNode.objects.filter(user=request.user)
                existing_nodes_ids = [node.id for node in existing_nodes]
                received_nodes_ids = [node.get('id') for node in nodes_data]
                nodes_to_delete = set(existing_nodes_ids) - set(received_nodes_ids)
                FamilyNode.objects.filter(id__in=nodes_to_delete).delete()
                FamilyLink.objects.filter(source_node__id__in=nodes_to_delete).delete()
                FamilyLink.objects.filter(target_node__id__in=nodes_to_delete).delete()
                

                # Create nodes
                created_nodes = {}
                for node_data in nodes_data:
                    id_value = node_data.get('id')
                    fid_value = node_data.get('fid')
                    mid_value = node_data.get('mid')
                    pid_value = node_data.get('pids')
                    surname_value = node_data.get('surname')
                    phone_value = node_data.get('phone')
                    email_value = node_data.get('email')
                    birthDate_value = node_data.get('birthDate (eg. 2002-05-20)')
                    special_event_value = node_data.get('special_event')
                    other_comments_value = node_data.get('other_comments')

                    
                    existing_node = FamilyNode.objects.filter(id=id_value).first()
                    if existing_node:
                        # Update existing node
                        # existing_node.pids = node_data.get('pids', [])
                        existing_node.pids = pid_value
                        existing_node.name = node_data.get('name', '')
                        existing_node.gender = node_data.get('gender', '')
                        existing_node.fid = fid_value
                        existing_node.mid = mid_value
                        existing_node.surname = surname_value
                        existing_node.phone = phone_value
                        # existing_node.email = email_value
                        # Checking if the email is empty or has already been set before updating it
                        if email_value != '' and existing_node.email == None and existing_node.email != email_value:
                            existing_node.email = email_value
                        # existing_node.date_of_birth = birthDate_value
                        # Checking if the date of birth is empty or has already been set before updating it
                        if birthDate_value != '' and existing_node.date_of_birth == None and existing_node.date_of_birth != birthDate_value:
                            existing_node.date_of_birth = birthDate_value 
                        existing_node.special_event = special_event_value
                        existing_node.other_comments = other_comments_value
                        existing_node.save()
                        created_nodes[id_value] = existing_node
                    else:
                        # Create new node
                        node = FamilyNode.objects.create(
                            id=id_value,
                            # pids=node_data.get('pids', []),
                            pids=pid_value,
                            name=node_data.get('name', ''),
                            gender=node_data.get('gender', ''),
                            fid=fid_value,
                            mid=mid_value,
                            surname=surname_value,
                            phone=phone_value,
                            email=email_value,
                            date_of_birth=birthDate_value,
                            special_event=special_event_value,
                            user=request.user
                        )
                        
                        created_nodes[id_value] = node

                # Create links
                for link_data in links_data:
                    source_node_id = link_data.get('source')
                    target_node_id = link_data.get('target')
                    source_node = created_nodes.get(source_node_id)
                    target_node = created_nodes.get(target_node_id)
                    if source_node and target_node:
                        FamilyLink.objects.create(
                            source_node=source_node,
                            target_node=target_node
                        )

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Received data is empty'})
        except json.JSONDecodeError as e:
            # Log JSON decoding error
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': 'Error decoding JSON'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': 'Error occurred while saving data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from django.core.serializers import serialize
    
@csrf_exempt
@login_required(login_url='/')
def tree_data(request):
    if request.method == 'GET':
        try:
            # Fetch nodes and clinks associated with the currently authenticated user
            nodes = FamilyNode.objects.filter(user=request.user)
            clinks = FamilyLink.objects.filter(source_node__in=nodes, target_node__in=nodes)

            # Serialize nodes and clinks
            nodes_json = serialize('json', nodes)
            clinks_json = serialize('json', clinks)

            # Return serialized data as JSON response
            data = {
                "nodes": nodes_json,
                "clinks": clinks_json
            }
            return JsonResponse(data, safe=False)
        except Exception as e:
            # Log and handle exceptions gracefully
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
# @csrf_exempt
# def tree_save(request):
#     if request.method == 'POST':
#         try:
#             received_data = json.loads(request.body.decode('utf-8'))
#             if received_data:
#                 tree_data = FamilyTreeData.objects.create(data=received_data)
#                 return JsonResponse({'status': 'success'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Received data is empty'})
#         except json.JSONDecodeError as e:
#             # Log JSON decoding error
#             traceback.print_exc()
#             return JsonResponse({'status': 'error', 'message': 'Error decoding JSON'})
#         except Exception as e:
#             # Log other exceptions
#             traceback.print_exc()
#             return JsonResponse({'status': 'error', 'message': 'Error occurred while saving data'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})