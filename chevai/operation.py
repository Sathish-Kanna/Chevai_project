from django.db.models import Q

from datetime import datetime

from request.models import Request
from users.models import Profile
from chat.models import Chat


def get_notification(user):
    request_list = list(Request.objects.all())
    return_list = []
    for request in request_list:
        if request.to_service.user.user == user and request.status == 'waiting':
            return_list.append(request)
        if request.from_user == user and (request.status == 'accepted' or request.status == 'rejected'):
            request.message = '\''+str(request.to_service.user.name)+'\' has '\
                                 + str(request.status)+' your request for \''+str(request.to_service.skill)+'\''
            return_list.append(request)
        elif request.from_user == user and request.status == 'conformed' and request.service_date < datetime.today().date():
            request.message = 'You can give your feedback for \'' +str(request.to_service.skill) + '\' by ' \
                              + str(request.to_service.user.name)
            return_list.append(request)

    chat_list = list(Chat.objects.all())
    tst = []
    for chat in chat_list:
        if chat.status == 'waiting' and chat.to_user == user:
            msg = str(chat.from_user.profile.name)+' texted you'
            status = 'message'
            prof = Profile.objects.get(user=chat.from_user)
            pk = chat.pk
            to_id = prof.pk
            name = prof.name
            rqst = {'message': msg, 'status': status, 'pk': pk, 'to_id': to_id, 'name': name}
            if to_id in tst:
                Chat.obj.received_message(chat.pk)
            else:
                tst.append(to_id)
                return_list.append(rqst)

    if len(return_list) < 1:
        notification = {'data': [{'message': 'no notification'}]}
    else:
        notification = {
            'count': len(return_list),
            'data': return_list,
        }
    return notification


def in_search_fun(Service, q_words, category):
    contents = list(Service.objects.all())
    val = [0] * len(contents)
    rate = [0] * len(contents)

    for word in q_words:
        if '1' in category:
            query_cnd = Q(skill__icontains=word)
        elif '2' in category:
            query_cnd = Q(user__name__icontains=word)
        elif '3' in category:
            query_cnd = Q(user__language__icontains=word)
        elif '4' in category:
            query_cnd = Q(user__location__icontains=word)
        else:
            query_cnd = Q(skill__icontains=word) | Q(user__name__icontains=word) | Q(
                user__language__icontains=word) | Q(user__location__icontains=word)

        qry_rst = list(Service.objects.filter(query_cnd))
        for cnt in contents:
            if cnt in qry_rst:
                val[contents.index(cnt)] += 1
                rate[contents.index(cnt)] = int(cnt.rating)
    # init cnt_dict
    cnt_dict = {rate[i]: {contents[i]} for i in range(0, len(rate))}
    for i in range(0, len(rate)):
        cnt_dict[rate[i]].add(contents[i])

    lop = []
    for i in sorted(cnt_dict, reverse=True):
        if i is not 0:
            lop.append(list(cnt_dict[i]))

    flat_list = []
    for sublist in lop:
        for item in sublist:
            flat_list.append(item)

    return flat_list
