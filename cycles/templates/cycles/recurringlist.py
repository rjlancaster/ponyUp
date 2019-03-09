{% extends "cycles/index.html" %}

{% block content %}
<h1>Current Recurring Bill Categories</h1>
<ul class="list-group mt-3" style="width: 25rem;"></ul>
{% for recurring in recurrings %}
{% if recurring.deletedOn is None %}
<li class="list-group-item">{{ recurring.name }}
    {% csrf_token %}
    <a href="{% url 'cycles:editrecurringForm' recurring.id %}"><button class="btn btn-primary btn-sm">Edit</button></a>
    <a href="{% url 'cycles:deleterecurring' recurring.id %}"><button class="btn btn-danger btn-sm">Delete</button></a>
</li>
{% endif %}
{% endfor %}
<a href="{% url 'cycles:addrecurringForm' %}"><button class="btn btn-primary btn-sm">Add Recurring Category</button></a>
{% endblock %}