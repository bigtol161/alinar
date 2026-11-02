import pathlib

p = pathlib.Path('news/views.py')
s = p.read_text()

old = """        if current_city:
            executors = executors.filter(city=current_city)
    return render(request, 'news/executor_list.html', {
        'executors': executors,
        'cities': cities,
        'current_city': current_city,
    })"""
new = """        if current_city:
            executors = executors.filter(city=current_city)
    current_service = None
    service_id = request.GET.get('service')
    if service_id:
        current_service = Service.objects.filter(pk=service_id).first()
        if current_service:
            executors = executors.filter(services=current_service)
    return render(request, 'news/executor_list.html', {
        'executors': executors,
        'cities': cities,
        'current_city': current_city,
        'current_service': current_service,
    })"""

if 'current_service' in s:
    print('уже добавлено')
elif old in s:
    s = s.replace(old, new)
    p.write_text(s)
    print('фильтр по услуге добавлен')
else:
    print('якорь не совпал — пришли: sed -n "102,126p" news/views.py')
