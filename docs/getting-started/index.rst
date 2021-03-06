Getting Started
================

Installation
---------------

You can simply install :code:`pyneg` using :code:`pip` along with all the required dependencies like so:

.. code-block::

    pip install pyneg

However, to function properly, specifically all the components that use ProbLog, the PySDD package must be installed, including the compiled and linked SDD C libraries. For Installation notes on that library please see the  `PySDD <https://github.com/wannesm/PySDD>`_ page. 

Alternatively there is a Docker image available that has everything that the library needs. You can pull the docker image by using 

.. code-block::

    docker pull savente/pyneg:latest

After that has completed successfully you can run all the unit by simply running the container: 

.. code-block::

    docker run savente/pyneg

Alternatively, if you want an interactive shell enviroment that has everything correctly installed you can get one by using

.. code-block::

    docker run -it savente/pyneg /bin/bash


Minimal Working Example
------------------------

.. code-block:: python

    >>> from pyneg.agent.agent_factory import make_linear_concession_agent 
    >>> neg_space = {"first":[0, 1, 2, 3, 4], "second":[5,6,7,8,9]}  
    >>> utilities_a = {"second_5":10,"second_9":-10,"first_0":-5,"first_3":5}  
    >>> utilities_b = {"second_5":-5,"second_7":5,"first_0":10,"first_4":-10}  
    >>> res_a = 0.1  
    >>> res_b = 0.1  
    >>> non_agreement_cost = -10**100   
    >>> agent_a = make_linear_concession_agent("A",neg_space,utilities_a,res_a,non_agreement_cost)  
    >>> agent_b = make_linear_concession_agent("B",neg_space,utilities_b,res_b,non_agreement_cost)  
    >>> agent_a.negotiate(agent_b) 
    True
    >>> agent_a._transcript 
    [(A=>B;OFFER;[first->3, second->5]),
    (B=>A;OFFER;[first->0, second->7]),
    (A=>B;OFFER;[first->1, second->5]),
    (B=>A;OFFER;[first->0, second->6]),
    (A=>B;OFFER;[first->2, second->5]),
    (B=>A;OFFER;[first->0, second->8]),
    (A=>B;OFFER;[first->4, second->5]),
    (B=>A;OFFER;[first->0, second->9]),
    (A=>B;OFFER;[first->3, second->6]),
    (B=>A;OFFER;[first->1, second->7]),
    (A=>B;OFFER;[first->0, second->5]),
    (B=>A;ACCEPT;[first->0, second->5])]
