{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. automethod:: {{ fullname }}

{% if parameters %}
.. rubric:: {{ _('Parameters') }}

.. autosummary::
   :toctree:
{% for item in parameters %}
   {{ item }}
{%- endfor %}
{% endif %}

{% if attributes %}
.. rubric:: {{ _('Attributes') }}

.. autosummary::
{% for item in attributes %}
   {{ item }}
{%- endfor %}
{% endif %}

{% if exceptions %}
.. rubric:: {{ _('Exceptions') }}

.. autosummary::
{% for item in exceptions %}
   {{ item }}
{%- endfor %}
{% endif %}
