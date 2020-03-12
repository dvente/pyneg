FROM problog:latest

ENV user sam

WORKDIR /src

RUN useradd  ${user} && \
    chown -R ${user} /src && \
    chmod -R g+s /src

RUN python -m pip install pytest pytest-xdist pytest-cov mypy requests coverage pandas

#COPY --chown=${user} .coveragerc pytest.ini sims/parallel_simulator.py sims/simulate_from_scratch.py sims/simulate_single_neg.py setup.py /src/

COPY --chown=${user} test/ /src/test/
COPY --chown=${user} .coveragerc pytest.ini setup.py test/ /src/

RUN pip install .

USER ${user}

